"""
Before/After comparison module for tracking optimization improvements.
"""

import time
import json
from typing import Dict, Any, List, Callable, Tuple
from datetime import datetime
import tracemalloc


class ComparisonResult:
    """Stores comparison results between before and after states."""

    def __init__(self, name: str):
        self.name = name
        self.before = {}
        self.after = {}
        self.improvements = {}
        self.timestamp = datetime.now().isoformat()

    def calculate_improvements(self):
        """Calculate improvement percentages."""
        # Time improvements
        if "time" in self.before and "time" in self.after:
            time_diff = self.before["time"] - self.after["time"]
            self.improvements["time_saved"] = time_diff
            self.improvements["time_improvement_percent"] = (
                (time_diff / self.before["time"] * 100)
                if self.before["time"] > 0
                else 0
            )

        # Memory improvements
        if "memory" in self.before and "memory" in self.after:
            mem_diff = self.before["memory"] - self.after["memory"]
            self.improvements["memory_saved"] = mem_diff
            self.improvements["memory_improvement_percent"] = (
                (mem_diff / self.before["memory"] * 100)
                if self.before["memory"] > 0
                else 0
            )

        # Call count improvements
        if "calls" in self.before and "calls" in self.after:
            call_diff = self.before["calls"] - self.after["calls"]
            self.improvements["calls_reduced"] = call_diff

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "timestamp": self.timestamp,
            "before": self.before,
            "after": self.after,
            "improvements": self.improvements,
        }


class ComparisonEngine:
    """Engine for comparing before/after optimization results."""

    def __init__(self):
        self.comparisons = []

    def compare_functions(
        self,
        before_func: Callable,
        after_func: Callable,
        args: tuple = (),
        kwargs: dict = None,
        iterations: int = 10,
        name: str = None,
    ) -> ComparisonResult:
        """
        Compare two function versions.

        Args:
            before_func: Original function
            after_func: Optimized function
            args: Function arguments
            kwargs: Function keyword arguments
            iterations: Number of times to run each function
            name: Name for this comparison

        Returns:
            ComparisonResult object
        """
        kwargs = kwargs or {}
        name = name or f"{before_func.__name__}_vs_{after_func.__name__}"

        result = ComparisonResult(name)

        # Profile 'before' function
        before_stats = self._profile_function(before_func, args, kwargs, iterations)
        result.before = before_stats

        # Profile 'after' function
        after_stats = self._profile_function(after_func, args, kwargs, iterations)
        result.after = after_stats

        # Calculate improvements
        result.calculate_improvements()

        self.comparisons.append(result)
        return result

    def _profile_function(
        self, func: Callable, args: tuple, kwargs: dict, iterations: int
    ) -> Dict[str, Any]:
        """
        Profile a single function.

        Args:
            func: Function to profile
            args: Function arguments
            kwargs: Function keyword arguments
            iterations: Number of iterations

        Returns:
            Dictionary with profiling stats
        """
        times = []
        memories = []

        if not tracemalloc.is_tracing():
            tracemalloc.start()

        for _ in range(iterations):
            tracemalloc.reset_peak()

            start_time = time.perf_counter()
            func(*args, **kwargs)
            end_time = time.perf_counter()

            current, peak = tracemalloc.get_traced_memory()

            times.append(end_time - start_time)
            memories.append(peak / 1024 / 1024)  # Convert to MB

        avg_time = sum(times) / len(times)
        avg_memory = sum(memories) / len(memories)

        return {
            "time": avg_time,
            "memory": avg_memory,
            "min_time": min(times),
            "max_time": max(times),
            "iterations": iterations,
            "function_name": func.__name__,
        }

    def print_comparison(self, result: ComparisonResult):
        """
        Print a formatted comparison.

        Args:
            result: ComparisonResult to print
        """
        print("\n" + "=" * 80)
        print(f"📊 Before/After Comparison: {result.name}")
        print("=" * 80)

        # Time comparison
        if "time" in result.before and "time" in result.after:
            print(f"\n⏱️  EXECUTION TIME:")
            print(f"   Before:  {result.before['time']:.6f}s")
            print(f"   After:   {result.after['time']:.6f}s")

            time_improvement = result.improvements.get("time_improvement_percent", 0)
            arrow = "🔴" if time_improvement < 0 else "🟢"
            print(f"   {arrow} Change:  {time_improvement:+.2f}%")

            if time_improvement > 0:
                print(
                    f"   Saved:   {result.improvements['time_saved']:.6f}s per execution"
                )

        # Memory comparison
        if "memory" in result.before and "memory" in result.after:
            print(f"\n💾 MEMORY USAGE:")
            print(f"   Before:  {result.before['memory']:.2f} MB")
            print(f"   After:   {result.after['memory']:.2f} MB")

            mem_improvement = result.improvements.get("memory_improvement_percent", 0)
            arrow = "🔴" if mem_improvement < 0 else "🟢"
            print(f"   {arrow} Change:  {mem_improvement:+.2f}%")

            if mem_improvement > 0:
                print(f"   Saved:   {result.improvements['memory_saved']:.2f} MB")

        # Overall verdict
        print(f"\n📈 VERDICT:")
        time_imp = result.improvements.get("time_improvement_percent", 0)
        mem_imp = result.improvements.get("memory_improvement_percent", 0)

        if time_imp > 10 or mem_imp > 10:
            print("   ✅ Significant improvement! Optimization successful.")
        elif time_imp > 0 or mem_imp > 0:
            print("   ✅ Minor improvement. Consider further optimization.")
        else:
            print("   ⚠️  No improvement or regression. Review changes.")

        print("=" * 80)

    def get_all_comparisons(self) -> List[ComparisonResult]:
        """Get all comparison results."""
        return self.comparisons

    def export_comparisons(self, filepath: str):
        """
        Export comparison results to JSON file.

        Args:
            filepath: Path to save JSON file
        """
        data = [comp.to_dict() for comp in self.comparisons]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def generate_summary(self) -> str:
        """
        Generate a summary of all comparisons.

        Returns:
            Summary string
        """
        if not self.comparisons:
            return "No comparisons available."

        lines = ["OPTIMIZATION SUMMARY", "=" * 60, ""]

        total_time_saved = 0
        total_memory_saved = 0
        improvements_count = 0

        for comp in self.comparisons:
            time_imp = comp.improvements.get("time_improvement_percent", 0)
            mem_imp = comp.improvements.get("memory_improvement_percent", 0)

            if time_imp > 0 or mem_imp > 0:
                improvements_count += 1

            if "time_saved" in comp.improvements:
                total_time_saved += comp.improvements["time_saved"]
            if "memory_saved" in comp.improvements:
                total_memory_saved += comp.improvements["memory_saved"]

            lines.append(f"✓ {comp.name}")
            if time_imp != 0:
                lines.append(f"  Time: {time_imp:+.2f}%")
            if mem_imp != 0:
                lines.append(f"  Memory: {mem_imp:+.2f}%")
            lines.append("")

        lines.append("=" * 60)
        lines.append(f"Total comparisons: {len(self.comparisons)}")
        lines.append(f"Successful optimizations: {improvements_count}")
        lines.append(f"Total time saved: {total_time_saved:.4f}s")
        lines.append(f"Total memory saved: {total_memory_saved:.2f}MB")

        return "\n".join(lines)

    def reset(self):
        """Reset all comparison data."""
        self.comparisons = []
