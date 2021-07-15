"""
Setup configuration for Performance Profiler & Optimizer.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="performance-profiler-optimizer",
    version="1.0.0",
    author="Performance Optimizer Team",
    author_email="team@perfoptimizer.dev",
    description="A comprehensive Python profiling toolkit with auto-optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/performance-profiler-optimizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "psutil>=5.8.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "black>=21.0", "flake8>=3.9"],
    },
)
