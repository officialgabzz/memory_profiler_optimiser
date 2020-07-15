"""
Line-by-line profiler for detailed code analysis.
"""

import sys
import time
import linecache
import functools
from typing import Callable, Dict, Any, List, Tuple
import tracemalloc
from collections import defaultdict


class LineByLineProfiler:
    """Profile code execution line by line."""

    def __init__(self):
        self.results = {}
        self._enabled = True
        self._line_stats = defaultdict(
            lambda: {"hits": 0, "total_time": 0, "memory_increment": 0}
        )

    def enable(self):
        """Enable line-by-line profiling."""
        self._enabled = True

    def disable(self):
        """Disable line-by-line profiling."""
        self._enabled = False

    def _trace_lines(self, frame, event, arg):
        """Trace function for line-by-line execution."""
        if event != "line":
            return self._trace_lines

        # Get file and line info
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        key = (filename, lineno)

        # Track line execution
        self._line_stats[key]["hits"] += 1
        self._line_stats[key]["line_no"] = lineno
        self._line_stats[key]["filename"] = filename

        return self._trace_lines

    def profile_lines(self, func: Callable) -> Callable:
        """
        Decorator for line-by-line profiling.

        Args:
            func: Function to profile

        Returns:
            Wrapped function with line-level profiling
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self._enabled:
                return func(*args, **kwargs)

            func_name = func.__name__
            filename = func.__code__.co_filename

            # Start memory tracking
            if not tracemalloc.is_tracing():
                tracemalloc.start()

            # Reset line stats for this run
            self._line_stats.clear()

            # Set up tracing
            sys.settrace(self._trace_lines)
            start_time = time.perf_counter()
            snapshot_before = tracemalloc.take_snapshot()

            try:
                result = func(*args, **kwargs)
            finally:
                sys.settrace(None)

            end_time = time.perf_counter()
            snapshot_after = tracemalloc.take_snapshot()

            # Calculate statistics
            total_time = end_time - start_time
            top_stats = snapshot_after.compare_to(snapshot_before, "lineno")

            # Store results
            if func_name not in self.results:
                self.results[func_name] = []

            # Collect line data
            line_data = []
            for key, stats in self._line_stats.items():
                fname, lineno = key
                if fname == filename:
                    line_code = linecache.getline(fname, lineno).strip()
                    line_data.append(
                        {
                            "line_no": lineno,
                            "code": line_code,
                            "hits": stats["hits"],
                            "time_percent": (
                                (
                                    stats["hits"]
                                    / sum(s["hits"] for s in self._line_stats.values())
                                    * 100
                                )
                                if self._line_stats
                                else 0
                            ),
                        }
                    )

            # Add memory info from tracemalloc
            memory_by_line = {}
            for stat in top_stats[:20]:  # Top 20 memory consumers
                memory_by_line[stat.traceback[0].lineno] = stat.size_diff / 1024  # KB

            # Merge memory info
            for line in line_data:
                line["memory_kb"] = memory_by_line.get(line["line_no"], 0)

            self.results[func_name].append(
                {
                    "total_time": total_time,
                    "filename": filename,
                    "lines": sorted(line_data, key=lambda x: x["line_no"]),
                }
            )

            return result

        return wrapper

    def get_results(self) -> Dict[str, Any]:
        """Get line-by-line profiling results."""
        return self.results

    def print_results(self, top_n: int = 20):
        """
        Print formatted line-by-line analysis.

        Args:
            top_n: Number of top lines to show
        """
        if not self.results:
            print("No line-by-line profiling data available.")
            return

        print("\n" + "=" * 90)
        print("🔍 Line-by-Line Analysis")
        print("=" * 90)

        for func_name, runs in self.results.items():
            for idx, run in enumerate(runs):
                print(f"\nFunction: {func_name} (Run {idx + 1})")
                print(f"Total Time: {run['total_time']:.6f}s")
                print(f"File: {run['filename']}")
                print(
                    "\n{:<6} {:<8} {:<10} {:<12} {}".format(
                        "Line", "Hits", "Time %", "Memory (KB)", "Code"
                    )
                )
                print("-" * 90)

                # Sort by hits (most executed lines first)
                sorted_lines = sorted(
                    run["lines"], key=lambda x: x["hits"], reverse=True
                )

                for line in sorted_lines[:top_n]:
                    print(
                        "{:<6} {:<8} {:<10.2f} {:<12.2f} {}".format(
                            line["line_no"],
                            line["hits"],
                            line["time_percent"],
                            line["memory_kb"],
                            line["code"][:50],  # Truncate long lines
                        )
                    )

        print("\n" + "=" * 90)

    def get_hotspots(self, threshold: float = 5.0) -> List[Tuple[str, int, float]]:
        """
        Identify performance hotspots.

        Args:
            threshold: Minimum time percentage to be considered a hotspot

        Returns:
            List of (function_name, line_no, time_percent) tuples
        """
        hotspots = []
        for func_name, runs in self.results.items():
            for run in runs:
                for line in run["lines"]:
                    if line["time_percent"] >= threshold:
                        hotspots.append(
                            (
                                func_name,
                                line["line_no"],
                                line["time_percent"],
                                line["code"],
                            )
                        )

        return sorted(hotspots, key=lambda x: x[2], reverse=True)

    def reset(self):
        """Reset all profiling data."""
        self.results = {}
        self._line_stats.clear()
