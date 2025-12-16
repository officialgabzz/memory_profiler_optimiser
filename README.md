# Performance Profiler & Optimizer 🚀

A comprehensive Python toolkit for profiling and optimizing code performance with intelligent auto-suggestions and historical tracking.

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/yourusername/performance-profiler-optimizer)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ Features

- 💾 **Memory Profiling** - Track memory usage and allocations across your application
- 🔍 **Line-by-Line Analysis** - Detailed performance insights for each line of code
- 💡 **Auto-Optimization Suggestions** - AI-powered recommendations for code improvements
- 📊 **Before/After Comparisons** - Visual performance improvement metrics
- 🎯 **Bottleneck Highlighting** - Automatically identify and prioritize slow code
- 📈 **Historical Tracking** - Monitor performance trends over time with SQLite database

## 📦 Installation

```bash
pip install performance-profiler-optimizer
```

Or install from source:

```bash
git clone https://github.com/yourusername/performance-profiler-optimizer.git
cd performance-profiler-optimizer
pip install -e .
```

## 🚀 Quick Start

### Basic Performance Profiling

```python
from performance_profiler import PerformanceProfiler

profiler = PerformanceProfiler()

@profiler.profile
def my_function():
    return sum(range(1000000))

my_function()
profiler.print_results()
```

### Memory Profiling

```python
from performance_profiler import MemoryProfiler

memory_profiler = MemoryProfiler()
memory_profiler.enable()

@memory_profiler.profile_memory
def memory_intensive_task():
    return [i**2 for i in range(1000000)]

memory_intensive_task()
memory_profiler.print_results()
```

### Line-by-Line Analysis

```python
from performance_profiler import LineByLineProfiler

line_profiler = LineByLineProfiler()

@line_profiler.profile_lines
def complex_function():
    data = [i for i in range(10000)]
    filtered = [x for x in data if x % 2 == 0]
    return sum(filtered)

complex_function()
line_profiler.print_results(top_n=15)
```

### Auto-Optimization Suggestions

```python
from performance_profiler import OptimizerEngine

optimizer = OptimizerEngine()

# Analyze code
code = """
def inefficient():
    result = []
    for i in range(1000):
        result.append(i * 2)
    return result
"""

suggestions = optimizer.analyze_code(code)
optimizer.print_suggestions(suggestions)
```

### Before/After Comparisons

```python
from performance_profiler import ComparisonEngine

comparator = ComparisonEngine()

def before_optimization(n):
    result = ""
    for i in range(n):
        result += str(i)
    return result

def after_optimization(n):
    return ''.join(str(i) for i in range(n))

result = comparator.compare_functions(
    before_func=before_optimization,
    after_func=after_optimization,
    args=(1000,),
    iterations=100
)
comparator.print_comparison(result)
```

### Bottleneck Detection

```python
from performance_profiler import BottleneckDetector

detector = BottleneckDetector()

@detector.detect_bottlenecks
def slow_function():
    result = 0
    for i in range(1000):
        for j in range(1000):
            result += i * j
    return result

slow_function()
detector.print_bottlenecks()
```

### Historical Tracking

```python
from performance_profiler import HistoricalTracker

tracker = HistoricalTracker(db_path="performance.db")

@tracker.track
def monitored_function():
    return sum(range(100000))

# Run multiple times to build history
for _ in range(10):
    monitored_function()

# View history and trends
tracker.print_history("monitored_function", limit=10)
trend = tracker.get_trend("monitored_function", "execution_time")
print(f"Performance trend: {trend['trend']}")
```

## 📖 Documentation

### Module Overview

#### PerformanceProfiler
Basic execution time profiling with call statistics.

#### MemoryProfiler
Track memory allocations, peak usage, and memory changes.

#### LineByLineProfiler
Detailed line-by-line execution analysis with hotspot detection.

#### OptimizerEngine
Pattern-based and AST code analysis for optimization suggestions.

#### ComparisonEngine
Compare before/after optimization metrics with improvement calculations.

#### BottleneckDetector
Detect and classify performance bottlenecks by severity (critical, high, medium).

#### HistoricalTracker
SQLite-backed performance tracking with trend analysis and reporting.

## 📊 Examples

Check the `examples/` directory for comprehensive demonstrations:

- `basic_usage.py` - Simple profiling example
- `memory_profiling.py` - Memory tracking demo
- `line_profiling.py` - Line-by-line analysis
- `optimization_suggestions.py` - Auto-optimization examples
- `before_after_comparison.py` - Comparison demonstrations
- `bottleneck_detection.py` - Bottleneck identification
- `historical_tracking.py` - Historical data tracking

## 🔧 Requirements

- Python 3.7+
- psutil >= 5.8.0

## 📝 Development History

This project was developed incrementally with the following milestones:

- **Jan 2020**: Initial project structure and core profiler
- **Apr 2020**: Memory profiling capabilities
- **Jul 2020**: Line-by-line analysis implementation
- **Oct 2020**: Auto-optimization suggestion engine
- **Jan 2021**: Before/after comparison system
- **Apr 2021**: Bottleneck detection and highlighting
- **Jul 2021**: Historical tracking with database (v1.0.0)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Python's built-in profiling capabilities
- Uses psutil for system-level metrics
- Inspired by various profiling tools in the Python ecosystem

## 📧 Contact

**Author:** Malik Garuba  
**Email:** garubamalik@gmail.com

For questions, issues, or suggestions, please open an issue on GitHub or contact via email.

---

Made with ❤️ by Malik Garuba
