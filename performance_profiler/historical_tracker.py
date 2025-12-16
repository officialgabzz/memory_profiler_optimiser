"""
Historical performance tracking with SQLite database backend.
"""

import sqlite3
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import functools


class HistoricalTracker:
    """Track performance metrics over time with database persistence."""

    def __init__(self, db_path: str = "performance_history.db"):
        """
        Initialize historical tracker.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS performance_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                function_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                execution_time REAL,
                memory_usage REAL,
                peak_memory REAL,
                calls INTEGER,
                metadata TEXT,
                tags TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bottlenecks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER,
                line_no INTEGER,
                severity TEXT,
                metric_type TEXT,
                metric_value REAL,
                description TEXT,
                FOREIGN KEY (run_id) REFERENCES performance_runs(id)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS optimizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                function_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                before_time REAL,
                after_time REAL,
                before_memory REAL,
                after_memory REAL,
                improvement_percent REAL,
                description TEXT
            )
        """
        )

        # Create indexes
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_function_name 
            ON performance_runs(function_name)
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON performance_runs(timestamp)
        """
        )

        conn.commit()
        conn.close()

    def track(self, func):
        """
        Decorator to track function performance over time.

        Args:
            func: Function to track

        Returns:
            Wrapped function with historical tracking
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import tracemalloc
            import psutil
            import os

            # Start tracking
            if not tracemalloc.is_tracing():
                tracemalloc.start()

            process = psutil.Process(os.getpid())
            mem_before = process.memory_info().rss / 1024 / 1024  # MB

            tracemalloc.reset_peak()
            start_time = time.perf_counter()

            # Execute function
            result = func(*args, **kwargs)

            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            mem_after = process.memory_info().rss / 1024 / 1024  # MB

            # Record metrics
            execution_time = end_time - start_time
            memory_usage = mem_after - mem_before
            peak_memory = peak / 1024 / 1024  # MB

            self.record_run(
                function_name=func.__name__,
                execution_time=execution_time,
                memory_usage=memory_usage,
                peak_memory=peak_memory,
                calls=1,
            )

            return result

        return wrapper

    def record_run(
        self,
        function_name: str,
        execution_time: float,
        memory_usage: float,
        peak_memory: float,
        calls: int = 1,
        metadata: Dict[str, Any] = None,
        tags: List[str] = None,
    ):
        """
        Record a performance run.

        Args:
            function_name: Name of the function
            execution_time: Execution time in seconds
            memory_usage: Memory usage in MB
            peak_memory: Peak memory in MB
            calls: Number of calls
            metadata: Additional metadata
            tags: Tags for categorization
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO performance_runs 
            (function_name, timestamp, execution_time, memory_usage, 
             peak_memory, calls, metadata, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                function_name,
                datetime.now().isoformat(),
                execution_time,
                memory_usage,
                peak_memory,
                calls,
                json.dumps(metadata or {}),
                json.dumps(tags or []),
            ),
        )

        conn.commit()
        conn.close()

    def record_optimization(
        self,
        function_name: str,
        before_time: float,
        after_time: float,
        before_memory: float,
        after_memory: float,
        description: str = "",
    ):
        """
        Record an optimization result.

        Args:
            function_name: Name of the function
            before_time: Time before optimization
            after_time: Time after optimization
            before_memory: Memory before optimization
            after_memory: Memory after optimization
            description: Description of the optimization
        """
        improvement = (
            ((before_time - after_time) / before_time * 100) if before_time > 0 else 0
        )

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO optimizations
            (function_name, timestamp, before_time, after_time, 
             before_memory, after_memory, improvement_percent, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                function_name,
                datetime.now().isoformat(),
                before_time,
                after_time,
                before_memory,
                after_memory,
                improvement,
                description,
            ),
        )

        conn.commit()
        conn.close()

    def get_history(self, function_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get performance history for a function.

        Args:
            function_name: Name of the function
            limit: Maximum number of records to return

        Returns:
            List of performance records
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM performance_runs
            WHERE function_name = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """,
            (function_name, limit),
        )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_trend(
        self, function_name: str, metric: str = "execution_time"
    ) -> Dict[str, Any]:
        """
        Get performance trend for a function.

        Args:
            function_name: Name of the function
            metric: Metric to analyze ("execution_time" or "memory_usage")

        Returns:
            Trend analysis dictionary
        """
        history = self.get_history(function_name, limit=100)

        if not history:
            return {"error": "No data available"}

        values = [record[metric] for record in history if record[metric] is not None]

        if not values:
            return {"error": "No valid data"}

        # Calculate statistics
        avg = sum(values) / len(values)
        min_val = min(values)
        max_val = max(values)

        # Calculate trend (simple linear regression)
        n = len(values)
        if n >= 2:
            x = list(range(n))
            y = values
            x_mean = sum(x) / n
            y_mean = sum(y) / n

            numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
            denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

            slope = numerator / denominator if denominator != 0 else 0
            trend = "improving" if slope < 0 else "degrading" if slope > 0 else "stable"
        else:
            slope = 0
            trend = "insufficient_data"

        return {
            "function_name": function_name,
            "metric": metric,
            "count": len(values),
            "average": avg,
            "min": min_val,
            "max": max_val,
            "trend": trend,
            "slope": slope,
            "latest": values[0] if values else None,
        }

    def get_optimizations(
        self, function_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get recorded optimizations.

        Args:
            function_name: Optional function name filter

        Returns:
            List of optimization records
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if function_name:
            cursor.execute(
                """
                SELECT * FROM optimizations
                WHERE function_name = ?
                ORDER BY timestamp DESC
            """,
                (function_name,),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM optimizations
                ORDER BY timestamp DESC
            """
            )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def print_history(self, function_name: str, limit: int = 10):
        """
        Print performance history.

        Args:
            function_name: Name of the function
            limit: Number of records to show
        """
        history = self.get_history(function_name, limit)

        if not history:
            print(f"No history available for {function_name}")
            return

        print("\n" + "=" * 80)
        print(f"📈 Performance History: {function_name}")
        print("=" * 80)
        print(
            f"\n{'Timestamp':<20} {'Time (s)':<12} {'Memory (MB)':<15} {'Peak (MB)':<12}"
        )
        print("-" * 80)

        for record in history:
            timestamp = record["timestamp"][:19]  # Trim microseconds
            print(
                f"{timestamp:<20} {record['execution_time']:<12.6f} "
                f"{record['memory_usage']:<15.2f} {record['peak_memory']:<12.2f}"
            )

        print("=" * 80)

        # Show trend
        trend = self.get_trend(function_name)
        if "error" not in trend:
            print(f"\n📊 Trend Analysis:")
            print(f"  Average Time: {trend['average']:.6f}s")
            print(f"  Min: {trend['min']:.6f}s, Max: {trend['max']:.6f}s")
            print(f"  Trend: {trend['trend'].upper()}")
            if trend["slope"] != 0:
                direction = "⬇️  improving" if trend["slope"] < 0 else "⬆️  degrading"
                print(f"  Direction: {direction}")

        print("=" * 80)

    def generate_report(self) -> str:
        """
        Generate a comprehensive performance report.

        Returns:
            Report string
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get summary statistics
        cursor.execute("SELECT COUNT(DISTINCT function_name) FROM performance_runs")
        func_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM performance_runs")
        run_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM optimizations")
        opt_count = cursor.fetchone()[0]

        conn.close()

        lines = [
            "HISTORICAL PERFORMANCE REPORT",
            "=" * 60,
            "",
            f"Total Functions Tracked: {func_count}",
            f"Total Performance Runs: {run_count}",
            f"Total Optimizations: {opt_count}",
            "",
            "=" * 60,
        ]

        return "\n".join(lines)

    def clear_history(self, function_name: Optional[str] = None):
        """
        Clear performance history.

        Args:
            function_name: Optional function name to clear (clears all if None)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if function_name:
            cursor.execute(
                "DELETE FROM performance_runs WHERE function_name = ?", (function_name,)
            )
        else:
            cursor.execute("DELETE FROM performance_runs")
            cursor.execute("DELETE FROM bottlenecks")
            cursor.execute("DELETE FROM optimizations")

        conn.commit()
        conn.close()
