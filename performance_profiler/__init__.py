"""
Performance Profiler & Optimizer
A comprehensive Python profiling toolkit with auto-optimization capabilities.
"""

__version__ = "0.2.0"
__author__ = "Performance Optimizer Team"

from .profiler import PerformanceProfiler
from .memory_profiler import MemoryProfiler

__all__ = ["PerformanceProfiler", "MemoryProfiler"]
