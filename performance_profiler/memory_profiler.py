"""
Memory profiling module for tracking memory usage.
"""

import psutil
import os
import functools
from typing import Callable, Any, Dict, List
import tracemalloc


class MemoryProfiler:
    """Memory profiler for tracking memory consumption."""

    def __init__(self):
        self.results = {}
        self._enabled = True
        self._process = psutil.Process(os.getpid())

    def enable(self):
        """Enable memory profiling."""
        self._enabled = True
        tracemalloc.start()

    def disable(self):
        """Disable memory profiling."""
        self._enabled = False
        if tracemalloc.is_tracing():
            tracemalloc.stop()

    def get_current_memory(self) -> float:
        """
        Get current memory usage in MB.

        Returns:
            Current memory usage in megabytes
        """
        return self._process.memory_info().rss / 1024 / 1024

    def profile_memory(self, func: Callable) -> Callable:
        """
        Decorator to profile a function's memory usage.

        Args:
            func: Function to profile

        Returns:
            Wrapped function with memory profiling
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self._enabled:
                return func(*args, **kwargs)

            # Start tracking
            if not tracemalloc.is_tracing():
                tracemalloc.start()

            mem_before = self.get_current_memory()
            tracemalloc.reset_peak()

            # Execute function
            result = func(*args, **kwargs)

            # Get memory stats
            mem_after = self.get_current_memory()
            current, peak = tracemalloc.get_traced_memory()

            mem_diff = mem_after - mem_before
            func_name = func.__name__

            if func_name not in self.results:
                self.results[func_name] = {
                    "calls": 0,
                    "total_memory_allocated": 0,
                    "peak_memory": 0,
                    "avg_memory_per_call": 0,
                    "memory_changes": [],
                }

            self.results[func_name]["calls"] += 1
            self.results[func_name]["total_memory_allocated"] += (
                current / 1024 / 1024
            )  # Convert to MB
            self.results[func_name]["peak_memory"] = max(
                self.results[func_name]["peak_memory"], peak / 1024 / 1024
            )
            self.results[func_name]["memory_changes"].append(mem_diff)
            self.results[func_name]["avg_memory_per_call"] = (
                self.results[func_name]["total_memory_allocated"]
                / self.results[func_name]["calls"]
            )

            return result

        return wrapper

    def get_results(self) -> Dict[str, Any]:
        """
        Get memory profiling results.

        Returns:
            Dictionary of memory statistics
        """
        return self.results

    def print_results(self):
        """Print formatted memory profiling results."""
        if not self.results:
            print("No memory profiling data available.")
            return

        print("\n" + "=" * 70)
        print("💾 Memory Profiling Results")
        print("=" * 70)

        for func_name, stats in self.results.items():
            print(f"\nFunction: {func_name}")
            print(f"  Calls: {stats['calls']}")
            print(f"  Total Memory Allocated: {stats['total_memory_allocated']:.2f} MB")
            print(f"  Peak Memory: {stats['peak_memory']:.2f} MB")
            print(f"  Average Memory per Call: {stats['avg_memory_per_call']:.2f} MB")

            if stats["memory_changes"]:
                avg_change = sum(stats["memory_changes"]) / len(stats["memory_changes"])
                print(f"  Average Memory Change: {avg_change:+.2f} MB")

        print("\n" + "=" * 70)
        print(f"Current Process Memory: {self.get_current_memory():.2f} MB")
        print("=" * 70)

    def reset(self):
        """Reset all memory profiling data."""
        self.results = {}
        if tracemalloc.is_tracing():
            tracemalloc.stop()
            tracemalloc.start()

    def get_memory_info(self) -> Dict[str, float]:
        """
        Get detailed system memory information.

        Returns:
            Dictionary with system memory stats
        """
        mem = psutil.virtual_memory()
        return {
            "total": mem.total / 1024 / 1024,  # MB
            "available": mem.available / 1024 / 1024,
            "used": mem.used / 1024 / 1024,
            "percent": mem.percent,
            "process": self.get_current_memory(),
        }
