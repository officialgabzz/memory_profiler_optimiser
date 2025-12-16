"""
Historical performance tracking example.
"""

from performance_profiler import HistoricalTracker
import time
import random


# Initialize tracker
tracker = HistoricalTracker(db_path="demo_performance.db")


@tracker.track
def data_processing(size):
    """Simulate data processing."""
    data = [random.random() for _ in range(size)]
    result = sum(data)
    time.sleep(0.001)  # Simulate some work
    return result


@tracker.track
def matrix_operation(n):
    """Simulate matrix operation."""
    matrix = [[i * j for j in range(n)] for i in range(n)]
    time.sleep(0.002)
    return sum(sum(row) for row in matrix)


@tracker.track
def search_operation(items, target):
    """Simulate search operation."""
    for item in items:
        if item == target:
            return True
    return False


def simulate_performance_over_time():
    """Simulate multiple runs to build history."""
    print("=" * 80)
    print("Building Performance History...")
    print("=" * 80)

    # Run data_processing with varying inputs
    print("\n📊 Running data_processing tests...")
    for i in range(15):
        size = 1000 + (i * 100)
        data_processing(size)
        print(f"  Run {i+1}/15 complete (size={size})")

    # Run matrix_operation with varying inputs
    print("\n📊 Running matrix_operation tests...")
    for i in range(10):
        n = 50 + (i * 5)
        matrix_operation(n)
        print(f"  Run {i+1}/10 complete (n={n})")

    # Run search_operation
    print("\n📊 Running search_operation tests...")
    for i in range(12):
        items = list(range(5000 + i * 500))
        target = random.choice(items)
        search_operation(items, target)
        print(f"  Run {i+1}/12 complete")

    print("\n✅ History building complete!")


def demonstrate_tracking():
    """Demonstrate historical tracking features."""
    print("\n\n" + "=" * 80)
    print("🔍 Historical Tracking Demo")
    print("=" * 80)

    # Build history
    simulate_performance_over_time()

    # View history for each function
    print("\n\n" + "=" * 80)
    print("📈 Performance History Reports")
    print("=" * 80)

    for func_name in ["data_processing", "matrix_operation", "search_operation"]:
        tracker.print_history(func_name, limit=10)
        print()

    # Show trend analysis
    print("\n" + "=" * 80)
    print("📊 Trend Analysis")
    print("=" * 80)

    for func_name in ["data_processing", "matrix_operation", "search_operation"]:
        print(f"\n{func_name}:")

        # Time trend
        time_trend = tracker.get_trend(func_name, "execution_time")
        if "error" not in time_trend:
            print(f"  ⏱️  Time Trend: {time_trend['trend']}")
            print(f"     Average: {time_trend['average']:.6f}s")
            print(f"     Range: {time_trend['min']:.6f}s - {time_trend['max']:.6f}s")

        # Memory trend
        mem_trend = tracker.get_trend(func_name, "memory_usage")
        if "error" not in mem_trend:
            print(f"  💾 Memory Trend: {mem_trend['trend']}")
            print(f"     Average: {mem_trend['average']:.2f} MB")

    # Record some optimizations
    print("\n\n" + "=" * 80)
    print("📝 Recording Optimizations")
    print("=" * 80)

    tracker.record_optimization(
        function_name="data_processing",
        before_time=0.050,
        after_time=0.030,
        before_memory=15.5,
        after_memory=10.2,
        description="Optimized list comprehension and reduced allocations",
    )

    tracker.record_optimization(
        function_name="matrix_operation",
        before_time=0.120,
        after_time=0.075,
        before_memory=25.0,
        after_memory=18.5,
        description="Switched to NumPy arrays for better performance",
    )

    print("✅ Optimizations recorded!")

    # Show optimizations
    print("\n" + "=" * 80)
    print("🎯 Optimization History")
    print("=" * 80)

    optimizations = tracker.get_optimizations()
    for opt in optimizations:
        print(f"\nFunction: {opt['function_name']}")
        print(f"  Date: {opt['timestamp'][:19]}")
        print(
            f"  Time: {opt['before_time']:.6f}s → {opt['after_time']:.6f}s "
            f"({opt['improvement_percent']:+.1f}%)"
        )
        print(f"  Memory: {opt['before_memory']:.2f}MB → {opt['after_memory']:.2f}MB")
        print(f"  Description: {opt['description']}")

    # Generate overall report
    print("\n\n")
    print(tracker.generate_report())


if __name__ == "__main__":
    print("🚀 Historical Performance Tracking Demo\n")

    # Clear any existing history for demo
    tracker.clear_history()

    # Run demonstration
    demonstrate_tracking()

    print("\n" + "=" * 80)
    print("✨ Demo Complete!")
    print("=" * 80)
    print("\nDatabase saved to: demo_performance.db")
    print("You can query this database to analyze performance over time.")
