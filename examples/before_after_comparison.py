"""
Before/After comparison examples.
"""

from performance_profiler import ComparisonEngine


def inefficient_string_concat(n):
    """Inefficient string concatenation."""
    result = ""
    for i in range(n):
        result += str(i)
    return result


def efficient_string_concat(n):
    """Efficient string concatenation using join."""
    return ''.join(str(i) for i in range(n))


def inefficient_list_building(n):
    """Inefficient list building with append."""
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result


def efficient_list_building(n):
    """Efficient list building with list comprehension."""
    return [i ** 2 for i in range(n)]


def inefficient_filtering(data):
    """Inefficient filtering with loop."""
    result = []
    for item in data:
        if item % 2 == 0:
            result.append(item)
    return result


def efficient_filtering(data):
    """Efficient filtering with list comprehension."""
    return [item for item in data if item % 2 == 0]


def inefficient_nested_loops(n):
    """Inefficient nested loops."""
    result = []
    for i in range(n):
        for j in range(n):
            result.append(i * j)
    return result


def efficient_nested_loops(n):
    """More efficient using list comprehension."""
    return [i * j for i in range(n) for j in range(n)]


if __name__ == "__main__":
    print("🔬 Before/After Comparison Demo\n")
    
    comparator = ComparisonEngine()
    
    # Test 1: String concatenation
    print("Test 1: String Concatenation")
    result1 = comparator.compare_functions(
        before_func=inefficient_string_concat,
        after_func=efficient_string_concat,
        args=(1000,),
        iterations=100,
        name="String Concatenation"
    )
    comparator.print_comparison(result1)
    
    # Test 2: List building
    print("\n\nTest 2: List Building")
    result2 = comparator.compare_functions(
        before_func=inefficient_list_building,
        after_func=efficient_list_building,
        args=(10000,),
        iterations=100,
        name="List Building"
    )
    comparator.print_comparison(result2)
    
    # Test 3: Filtering
    print("\n\nTest 3: Filtering")
    test_data = list(range(10000))
    result3 = comparator.compare_functions(
        before_func=inefficient_filtering,
        after_func=efficient_filtering,
        args=(test_data,),
        iterations=50,
        name="Data Filtering"
    )
    comparator.print_comparison(result3)
    
    # Test 4: Nested loops
    print("\n\nTest 4: Nested Loops")
    result4 = comparator.compare_functions(
        before_func=inefficient_nested_loops,
        after_func=efficient_nested_loops,
        args=(100,),
        iterations=20,
        name="Nested Loops"
    )
    comparator.print_comparison(result4)
    
    # Generate summary
    print("\n\n")
    print(comparator.generate_summary())
    
    # Export results
    try:
        comparator.export_comparisons('comparison_results.json')
        print("\n📁 Results exported to 'comparison_results.json'")
    except Exception as e:
        print(f"\n⚠️  Could not export results: {e}")
