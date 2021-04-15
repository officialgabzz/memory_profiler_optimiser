"""
Bottleneck detection example.
"""

from performance_profiler import BottleneckDetector


detector = BottleneckDetector()


@detector.detect_bottlenecks
def cpu_intensive_function():
    """Function with CPU bottleneck."""
    result = 0
    # This nested loop is a bottleneck
    for i in range(1000):
        for j in range(1000):
            result += i * j
    return result


@detector.detect_bottlenecks
def memory_intensive_function():
    """Function with memory bottleneck."""
    # Large memory allocation
    big_list = [x ** 2 for x in range(5000000)]
    
    # Another memory-intensive operation
    another_list = [x * 3 for x in range(3000000)]
    
    return len(big_list) + len(another_list)


@detector.detect_bottlenecks
def high_frequency_calls():
    """Function with many small operations."""
    data = []
    
    # Many iterations - call frequency bottleneck
    for i in range(20000):
        data.append(i)
        data.append(i * 2)
    
    return sum(data)


@detector.detect_bottlenecks
def mixed_bottlenecks():
    """Function with multiple types of bottlenecks."""
    # Memory bottleneck
    large_data = list(range(2000000))
    
    # Time bottleneck - inefficient processing
    result = []
    for item in large_data:
        if item % 2 == 0:
            result.append(item ** 2)
    
    # More time bottleneck
    for i in range(len(result)):
        result[i] = result[i] + 1
    
    return sum(result)


if __name__ == "__main__":
    print("🔍 Bottleneck Detection Demo\n")
    print("Analyzing various performance bottlenecks...\n")
    
    # Test 1: CPU intensive
    print("=" * 80)
    print("Test 1: CPU Intensive Function")
    print("=" * 80)
    result1 = cpu_intensive_function()
    print(f"Result: {result1}")
    detector.print_bottlenecks()
    
    # Get recommendations
    print("\n📋 Recommendations:")
    for rec in detector.get_recommendations():
        print(f"  {rec}")
    
    detector.reset()
    
    # Test 2: Memory intensive
    print("\n\n" + "=" * 80)
    print("Test 2: Memory Intensive Function")
    print("=" * 80)
    result2 = memory_intensive_function()
    print(f"Result: {result2}")
    detector.print_bottlenecks()
    
    print("\n📋 Recommendations:")
    for rec in detector.get_recommendations():
        print(f"  {rec}")
    
    detector.reset()
    
    # Test 3: High frequency calls
    print("\n\n" + "=" * 80)
    print("Test 3: High Frequency Calls")
    print("=" * 80)
    result3 = high_frequency_calls()
    print(f"Result: {result3}")
    detector.print_bottlenecks()
    
    print("\n📋 Recommendations:")
    for rec in detector.get_recommendations():
        print(f"  {rec}")
    
    detector.reset()
    
    # Test 4: Mixed bottlenecks
    print("\n\n" + "=" * 80)
    print("Test 4: Mixed Bottlenecks")
    print("=" * 80)
    result4 = mixed_bottlenecks()
    print(f"Result: {result4}")
    detector.print_bottlenecks()
    
    # Summary
    summary = detector.get_summary()
    print("\n\n" + "=" * 80)
    print("📊 Summary")
    print("=" * 80)
    print(f"Total bottlenecks: {summary['total']}")
    print(f"By severity: Critical={summary['by_severity']['critical']}, "
          f"High={summary['by_severity']['high']}, "
          f"Medium={summary['by_severity']['medium']}")
    print(f"By type: Time={summary['by_type']['time']}, "
          f"Memory={summary['by_type']['memory']}, "
          f"Calls={summary['by_type']['calls']}")
    
    print("\n📋 Final Recommendations:")
    for rec in detector.get_recommendations():
        print(f"  {rec}")
