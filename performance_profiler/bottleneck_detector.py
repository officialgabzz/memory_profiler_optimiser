"""
Bottleneck detection and highlighting system.
"""

import time
import sys
import functools
from typing import Dict, Any, List, Tuple, Callable
from collections import defaultdict
import tracemalloc


class Bottleneck:
    """Represents a performance bottleneck."""

    def __init__(
        self,
        location: str,
        line_no: int,
        severity: str,
        metric_type: str,
        metric_value: float,
        description: str,
    ):
        self.location = location
        self.line_no = line_no
        self.severity = severity  # "critical", "high", "medium", "low"
        self.metric_type = metric_type  # "time", "memory", "calls"
        self.metric_value = metric_value
        self.description = description

    def __repr__(self):
        return f"<Bottleneck {self.severity} at {self.location}:{self.line_no}>"


class BottleneckDetector:
    """Detects and highlights performance bottlenecks."""

    def __init__(self):
        self.bottlenecks = []
        self._line_times = defaultdict(float)
        self._line_calls = defaultdict(int)
        self._line_memory = defaultdict(float)
        self._enabled = True
        self._trace_start_time = {}

    def enable(self):
        """Enable bottleneck detection."""
        self._enabled = True

    def disable(self):
        """Disable bottleneck detection."""
        self._enabled = False

    def _trace_calls(self, frame, event, arg):
        """Trace function calls for bottleneck detection."""
        if not self._enabled:
            return

        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        key = (filename, lineno)

        if event == "call":
            self._trace_start_time[key] = time.perf_counter()
            self._line_calls[key] += 1
        elif event == "return":
            if key in self._trace_start_time:
                elapsed = time.perf_counter() - self._trace_start_time[key]
                self._line_times[key] += elapsed

        return self._trace_calls

    def detect_bottlenecks(self, func: Callable) -> Callable:
        """
        Decorator to detect bottlenecks in a function.

        Args:
            func: Function to analyze

        Returns:
            Wrapped function with bottleneck detection
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self._enabled:
                return func(*args, **kwargs)

            # Reset tracking
            self._line_times.clear()
            self._line_calls.clear()
            self._line_memory.clear()
            self._trace_start_time.clear()

            # Start memory tracking
            if not tracemalloc.is_tracing():
                tracemalloc.start()

            tracemalloc.reset_peak()
            snapshot_before = tracemalloc.take_snapshot()

            # Enable tracing
            sys.settrace(self._trace_calls)
            start_time = time.perf_counter()

            try:
                result = func(*args, **kwargs)
            finally:
                sys.settrace(None)

            end_time = time.perf_counter()
            total_time = end_time - start_time

            snapshot_after = tracemalloc.take_snapshot()
            top_stats = snapshot_after.compare_to(snapshot_before, "lineno")

            # Collect memory stats by line
            for stat in top_stats:
                if stat.traceback:
                    tb = stat.traceback[0]
                    key = (tb.filename, tb.lineno)
                    self._line_memory[key] = stat.size_diff / 1024 / 1024  # MB

            # Analyze and identify bottlenecks
            self._analyze_bottlenecks(func.__code__.co_filename, total_time)

            return result

        return wrapper

    def _analyze_bottlenecks(self, filename: str, total_time: float):
        """
        Analyze collected data to identify bottlenecks.

        Args:
            filename: Source file being analyzed
            total_time: Total execution time
        """
        # Time-based bottlenecks
        for (fname, lineno), elapsed in self._line_times.items():
            if fname != filename:
                continue

            time_percent = (elapsed / total_time * 100) if total_time > 0 else 0

            # Classify severity
            if time_percent > 30:
                severity = "critical"
            elif time_percent > 15:
                severity = "high"
            elif time_percent > 5:
                severity = "medium"
            else:
                continue  # Skip low impact

            self.bottlenecks.append(
                Bottleneck(
                    location=fname,
                    line_no=lineno,
                    severity=severity,
                    metric_type="time",
                    metric_value=elapsed,
                    description=f"{time_percent:.1f}% of total execution time",
                )
            )

        # Memory-based bottlenecks
        for (fname, lineno), memory_mb in self._line_memory.items():
            if fname != filename or memory_mb < 0:
                continue

            # Classify by memory size
            if memory_mb > 100:
                severity = "critical"
            elif memory_mb > 50:
                severity = "high"
            elif memory_mb > 10:
                severity = "medium"
            else:
                continue

            self.bottlenecks.append(
                Bottleneck(
                    location=fname,
                    line_no=lineno,
                    severity=severity,
                    metric_type="memory",
                    metric_value=memory_mb,
                    description=f"Allocated {memory_mb:.2f} MB",
                )
            )

        # Call frequency bottlenecks
        for (fname, lineno), calls in self._line_calls.items():
            if fname != filename:
                continue

            if calls > 10000:
                severity = "critical"
            elif calls > 5000:
                severity = "high"
            elif calls > 1000:
                severity = "medium"
            else:
                continue

            self.bottlenecks.append(
                Bottleneck(
                    location=fname,
                    line_no=lineno,
                    severity=severity,
                    metric_type="calls",
                    metric_value=calls,
                    description=f"Called {calls} times",
                )
            )

    def get_bottlenecks(self, severity: str = None) -> List[Bottleneck]:
        """
        Get detected bottlenecks, optionally filtered by severity.

        Args:
            severity: Filter by severity level

        Returns:
            List of bottlenecks
        """
        if severity:
            return [b for b in self.bottlenecks if b.severity == severity]
        return self.bottlenecks

    def print_bottlenecks(self):
        """Print highlighted bottlenecks."""
        if not self.bottlenecks:
            print("✅ No significant bottlenecks detected!")
            return

        print("\n" + "=" * 80)
        print("🎯 Bottleneck Detection Results")
        print("=" * 80)

        # Group by severity
        critical = [b for b in self.bottlenecks if b.severity == "critical"]
        high = [b for b in self.bottlenecks if b.severity == "high"]
        medium = [b for b in self.bottlenecks if b.severity == "medium"]

        for category, items, emoji in [
            ("🔴 CRITICAL BOTTLENECKS", critical, "🔴"),
            ("🟠 HIGH PRIORITY", high, "🟠"),
            ("🟡 MEDIUM PRIORITY", medium, "🟡"),
        ]:
            if items:
                print(f"\n{category}:")
                print("-" * 80)

                # Group by type
                time_items = [i for i in items if i.metric_type == "time"]
                memory_items = [i for i in items if i.metric_type == "memory"]
                call_items = [i for i in items if i.metric_type == "calls"]

                if time_items:
                    print(f"\n  ⏱️  Time Bottlenecks:")
                    for item in sorted(
                        time_items, key=lambda x: x.metric_value, reverse=True
                    ):
                        print(f"     {emoji} Line {item.line_no}: {item.description}")
                        print(f"        Time: {item.metric_value:.4f}s")

                if memory_items:
                    print(f"\n  💾 Memory Bottlenecks:")
                    for item in sorted(
                        memory_items, key=lambda x: x.metric_value, reverse=True
                    ):
                        print(f"     {emoji} Line {item.line_no}: {item.description}")

                if call_items:
                    print(f"\n  🔄 Call Frequency Bottlenecks:")
                    for item in sorted(
                        call_items, key=lambda x: x.metric_value, reverse=True
                    ):
                        print(f"     {emoji} Line {item.line_no}: {item.description}")

        print("\n" + "=" * 80)
        print(f"Total bottlenecks found: {len(self.bottlenecks)}")
        print(f"  Critical: {len(critical)}, High: {len(high)}, Medium: {len(medium)}")
        print("=" * 80)

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of detected bottlenecks.

        Returns:
            Dictionary with bottleneck statistics
        """
        summary = {
            "total": len(self.bottlenecks),
            "by_severity": {
                "critical": len(
                    [b for b in self.bottlenecks if b.severity == "critical"]
                ),
                "high": len([b for b in self.bottlenecks if b.severity == "high"]),
                "medium": len([b for b in self.bottlenecks if b.severity == "medium"]),
            },
            "by_type": {
                "time": len([b for b in self.bottlenecks if b.metric_type == "time"]),
                "memory": len(
                    [b for b in self.bottlenecks if b.metric_type == "memory"]
                ),
                "calls": len([b for b in self.bottlenecks if b.metric_type == "calls"]),
            },
        }
        return summary

    def get_recommendations(self) -> List[str]:
        """
        Get optimization recommendations based on bottlenecks.

        Returns:
            List of recommendations
        """
        recommendations = []

        critical_time = [
            b
            for b in self.bottlenecks
            if b.severity == "critical" and b.metric_type == "time"
        ]
        if critical_time:
            recommendations.append(
                "⚠️  Critical time bottlenecks detected. Consider algorithm optimization or caching."
            )

        critical_memory = [
            b
            for b in self.bottlenecks
            if b.severity == "critical" and b.metric_type == "memory"
        ]
        if critical_memory:
            recommendations.append(
                "⚠️  Critical memory usage detected. Consider using generators or processing in chunks."
            )

        high_calls = [
            b
            for b in self.bottlenecks
            if b.metric_type == "calls" and b.metric_value > 5000
        ]
        if high_calls:
            recommendations.append(
                "⚠️  High call frequency detected. Consider loop optimization or vectorization."
            )

        return recommendations

    def reset(self):
        """Reset all detection data."""
        self.bottlenecks = []
        self._line_times.clear()
        self._line_calls.clear()
        self._line_memory.clear()
        self._trace_start_time.clear()
