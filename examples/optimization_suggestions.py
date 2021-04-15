"""
Auto-optimization suggestions example.
"""

from performance_profiler import OptimizerEngine, MemoryProfiler


# Sample code to analyze
sample_code = """
def inefficient_function(items):
    result = []
    for item in items:
        result.append(item * 2)
    
    text = ""
    for i in range(len(items)):
        text += str(items[i])
    
    # Nested loops
    for i in range(100):
        for j in range(100):
            pass
    
    return result, text

def better_function(items):
    # Using list comprehension
    result = [item * 2 for item in items]
    
    # Using join
    text = ''.join(str(item) for item in items)
    
    return result, text
"""


def demo_code_analysis():
    """Demonstrate code analysis."""
    print("=" * 80)
    print("Code Analysis Demo")
    print("=" * 80)

    optimizer = OptimizerEngine()
    suggestions = optimizer.analyze_code(sample_code)
    optimizer.print_suggestions(suggestions)


def demo_profile_based_suggestions():
    """Demonstrate profile-based suggestions."""
    print("\n\n" + "=" * 80)
    print("Profile-Based Suggestions Demo")
    print("=" * 80)

    # Create sample profile data
    memory_profiler = MemoryProfiler()
    memory_profiler.enable()

    @memory_profiler.profile_memory
    def slow_function():
        """A deliberately slow function."""
        data = [i**2 for i in range(1000000)]
        return sum(data)

    @memory_profiler.profile_memory
    def memory_intensive():
        """Memory intensive function."""
        big_list = [x * 2 for x in range(5000000)]
        return len(big_list)

    # Run functions
    for _ in range(5):
        slow_function()

    memory_intensive()

    # Get suggestions based on profile
    optimizer = OptimizerEngine()
    profile_data = memory_profiler.get_results()
    suggestions = optimizer.suggest_from_profile(profile_data)
    optimizer.print_suggestions(suggestions)


def demo_function_analysis():
    """Demonstrate function analysis."""
    print("\n\n" + "=" * 80)
    print("Function Analysis Demo")
    print("=" * 80)

    def sample_function():
        """Sample function with optimization opportunities."""
        result = ""
        for i in range(100):
            result += str(i)  # String concatenation issue

        data = []
        for x in range(100):
            for y in range(100):  # Nested loops
                data.append(x * y)

        return result, data

    optimizer = OptimizerEngine()
    suggestions = optimizer.analyze_function(sample_function)
    optimizer.print_suggestions(suggestions)

    # Generate report
    print("\n" + optimizer.generate_report(suggestions))


if __name__ == "__main__":
    print("🤖 Auto-Optimization Engine Demo\n")

    demo_code_analysis()
    demo_profile_based_suggestions()
    demo_function_analysis()

    print("\n✨ Demo complete!")
