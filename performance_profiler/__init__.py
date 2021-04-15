"""
Performance Profiler & Optimizer
A comprehensive Python profiling toolkit with auto-optimization capabilities.
"""

__version__ = "0.6.0"
__author__ = "Performance Optimizer Team"

from .profiler import PerformanceProfiler
from .memory_profiler import MemoryProfiler
from .line_profiler import LineByLineProfiler
from .optimizer import OptimizerEngine, OptimizationSuggestion
from .comparator import ComparisonEngine, ComparisonResult
from .bottleneck_detector import BottleneckDetector, Bottleneck

__all__ = [
    "PerformanceProfiler",
    "MemoryProfiler",
    "LineByLineProfiler",
    "OptimizerEngine",
    "OptimizationSuggestion",
    "ComparisonEngine",
    "ComparisonResult",
    "BottleneckDetector",
    "Bottleneck",
]
