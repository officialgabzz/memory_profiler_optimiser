"""
Basic usage example for Performance Profiler.
"""

from performance_profiler import PerformanceProfiler
import time


profiler = PerformanceProfiler()


@profiler.profile
def slow_function():
    """A deliberately slow function for testing."""
    time.sleep(0.1)
    return sum(range(1000))


@profiler.profile
def fast_function():
    """A fast function for comparison."""
    return [i * 2 for i in range(100)]


if __name__ == "__main__":
    print("Running performance profiling demo...")
    
    # Run functions multiple times
    for _ in range(5):
        slow_function()
        fast_function()
    
    # Display results
    profiler.print_results()
