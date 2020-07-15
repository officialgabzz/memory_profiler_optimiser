"""
Line-by-line profiling example.
"""

from performance_profiler import LineByLineProfiler


line_profiler = LineByLineProfiler()


@line_profiler.profile_lines
def fibonacci(n):
    """Calculate fibonacci numbers (inefficient version)."""
    if n <= 1:
        return n
    else:
        a, b = 0, 1
        for i in range(2, n + 1):
            a, b = b, a + b
        return b


@line_profiler.profile_lines
def process_data():
    """Process some data with multiple operations."""
    data = []

    # Build list
    for i in range(1000):
        data.append(i**2)

    # Filter data
    filtered = [x for x in data if x % 2 == 0]

    # Calculate sum
    total = sum(filtered)

    # Calculate average
    avg = total / len(filtered) if filtered else 0

    return avg


@line_profiler.profile_lines
def nested_loops():
    """Function with nested loops."""
    result = 0
    for i in range(100):
        for j in range(100):
            result += i * j
    return result


if __name__ == "__main__":
    print("Running line-by-line profiling demo...\n")

    # Run profiled functions
    fib_result = fibonacci(30)
    print(f"Fibonacci(30) = {fib_result}")

    avg_result = process_data()
    print(f"Average = {avg_result}")

    nested_result = nested_loops()
    print(f"Nested loops result = {nested_result}")

    # Display results
    line_profiler.print_results(top_n=15)

    # Show hotspots
    print("\n🎯 Performance Hotspots (>5% time):")
    print("=" * 90)
    hotspots = line_profiler.get_hotspots(threshold=5.0)
    for func, line, percent, code in hotspots[:10]:
        print(f"{func}:{line} ({percent:.1f}%) - {code[:60]}")
