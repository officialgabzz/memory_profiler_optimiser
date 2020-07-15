"""
Core profiler module for performance analysis.
"""

import time
import functools
from typing import Callable, Any, Dict


class PerformanceProfiler:
    """Main profiler class for tracking code performance."""

    def __init__(self):
        self.results = {}
        self._enabled = True

    def enable(self):
        """Enable profiling."""
        self._enabled = True

    def disable(self):
        """Disable profiling."""
        self._enabled = False

    def profile(self, func: Callable) -> Callable:
        """
        Decorator to profile a function's execution.

        Args:
            func: Function to profile

        Returns:
            Wrapped function with profiling capabilities
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self._enabled:
                return func(*args, **kwargs)

            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()

            execution_time = end_time - start_time
            func_name = func.__name__

            if func_name not in self.results:
                self.results[func_name] = {
                    "calls": 0,
                    "total_time": 0,
                    "min_time": float("inf"),
                    "max_time": 0,
                }

            self.results[func_name]["calls"] += 1
            self.results[func_name]["total_time"] += execution_time
            self.results[func_name]["min_time"] = min(
                self.results[func_name]["min_time"], execution_time
            )
            self.results[func_name]["max_time"] = max(
                self.results[func_name]["max_time"], execution_time
            )

            return result

        return wrapper

    def get_results(self) -> Dict[str, Any]:
        """
        Get profiling results.

        Returns:
            Dictionary of profiling statistics
        """
        return self.results

    def print_results(self):
        """Print formatted profiling results."""
        if not self.results:
            print("No profiling data available.")
            return

        print("\n" + "=" * 70)
        print("Performance Profiling Results")
        print("=" * 70)

        for func_name, stats in self.results.items():
            avg_time = stats["total_time"] / stats["calls"]
            print(f"\nFunction: {func_name}")
            print(f"  Calls: {stats['calls']}")
            print(f"  Total Time: {stats['total_time']:.6f}s")
            print(f"  Average Time: {avg_time:.6f}s")
            print(f"  Min Time: {stats['min_time']:.6f}s")
            print(f"  Max Time: {stats['max_time']:.6f}s")

        print("\n" + "=" * 70)

    def reset(self):
        """Reset all profiling data."""
        self.results = {}
