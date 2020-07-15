"""
Memory profiling example demonstrating memory tracking capabilities.
"""

from performance_profiler import MemoryProfiler


memory_profiler = MemoryProfiler()
memory_profiler.enable()


@memory_profiler.profile_memory
def create_large_list():
    """Create a large list consuming significant memory."""
    return [i**2 for i in range(1000000)]


@memory_profiler.profile_memory
def create_dict():
    """Create a large dictionary."""
    return {i: str(i) * 10 for i in range(100000)}


@memory_profiler.profile_memory
def memory_intensive_operation():
    """Perform multiple memory-intensive operations."""
    data1 = create_large_list()
    data2 = create_dict()
    return len(data1) + len(data2)


if __name__ == "__main__":
    print("Running memory profiling demo...")
    print("\nInitial memory info:")
    info = memory_profiler.get_memory_info()
    print(f"  Process Memory: {info['process']:.2f} MB")
    print(f"  System Memory Used: {info['percent']:.1f}%")

    # Run memory-intensive functions
    for _ in range(3):
        result = memory_intensive_operation()

    # Display results
    memory_profiler.print_results()
