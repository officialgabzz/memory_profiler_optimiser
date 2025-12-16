#!/bin/bash
# Script to build and publish package to PyPI

set -e

echo "🚀 Publishing Performance Profiler & Optimizer to PyPI"
echo "=================================================="

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info

# Install/upgrade build tools
echo "📦 Installing build tools..."
python3 -m pip install --upgrade pip build twine

# Build the package
echo "🔨 Building package..."
python3 -m build

# Check the distribution
echo "🔍 Checking distribution..."
twine check dist/*

# Upload to TestPyPI first (optional)
read -p "Upload to TestPyPI first? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "📤 Uploading to TestPyPI..."
    twine upload --repository testpypi dist/*
    echo "✅ Uploaded to TestPyPI"
    echo "🔗 View at: https://test.pypi.org/project/performance-profiler-optimizer/"
    echo ""
    read -p "Continue with PyPI upload? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 0
    fi
fi

# Upload to PyPI
echo "📤 Uploading to PyPI..."
twine upload dist/*

echo ""
echo "✅ Successfully published to PyPI!"
echo "🔗 View at: https://pypi.org/project/performance-profiler-optimizer/"
echo ""
echo "Install with: pip install performance-profiler-optimizer"
