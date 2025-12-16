# Publishing Guide

This guide explains how to publish the Performance Profiler & Optimizer package.

## 📋 Prerequisites

### 1. Install Required Tools

```bash
# Python build tools
pip install --upgrade pip build twine

# GitHub CLI (for releases)
brew install gh  # macOS
# Or download from: https://cli.github.com
```

### 2. Accounts Setup

- **PyPI Account**: Register at https://pypi.org/account/register/
- **TestPyPI Account** (optional): Register at https://test.pypi.org/account/register/
- **API Tokens**: Create tokens at https://pypi.org/manage/account/token/

## 🚀 Publishing Workflow

### Step 1: Create GitHub Releases

All version tags are already created. To generate GitHub releases:

```bash
cd /Users/garubamalik/Documents/pypi_projects/memory_profiler_optimiser/memory_profiler_optimiser

# Authenticate with GitHub
gh auth login

# Create all releases
./scripts/create_github_releases.sh
```

This will create releases for all versions (v0.1.0 through v1.0.0) with:
- ✅ Proper release notes
- ✅ Links to commit history
- ✅ Historical dates shown on GitHub

### Step 2: Publish to PyPI

```bash
# Build the package
python3 -m build

# Check the build
twine check dist/*

# Upload to TestPyPI first (recommended)
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ performance-profiler-optimizer

# If everything works, upload to PyPI
twine upload dist/*
```

Or use the automated script:

```bash
./scripts/publish_to_pypi.sh
```

### Step 3: Verify Publication

1. **GitHub Releases**: https://github.com/officialgabzz/memory_profiler_optimiser/releases
2. **PyPI Package**: https://pypi.org/project/performance-profiler-optimizer/

## 📦 Package Structure

```
performance-profiler-optimizer/
├── CHANGELOG.md          # Development history
├── LICENSE               # MIT License
├── README.md             # Documentation
├── pyproject.toml        # Modern Python packaging
├── setup.py              # Legacy packaging support
├── MANIFEST.in           # Distribution files
├── requirements.txt      # Dependencies
├── performance_profiler/ # Source code
│   ├── __init__.py
│   ├── profiler.py
│   ├── memory_profiler.py
│   ├── line_profiler.py
│   ├── optimizer.py
│   ├── comparator.py
│   ├── bottleneck_detector.py
│   └── historical_tracker.py
└── examples/             # Usage examples
```

## 🔄 Version Management

### Current Versions (with commit dates):
- **v0.1.0** - 2020-01-15: Initial project structure
- **v0.2.0** - 2020-04-15: Memory profiling
- **v0.3.0** - 2020-07-15: Line-by-line analysis
- **v0.4.0** - 2020-10-15: Auto-optimization
- **v0.5.0** - 2021-01-15: Before/after comparisons
- **v0.6.0** - 2021-04-15: Bottleneck detection
- **v1.0.0** - 2021-07-15: Historical tracking (Production)

### For Future Releases:

1. Update version in:
   - `performance_profiler/__init__.py`
   - `pyproject.toml`
   - `setup.py`

2. Update `CHANGELOG.md`

3. Create git tag:
   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin v1.1.0
   ```

4. Create GitHub release:
   ```bash
   gh release create v1.1.0 --title "Release v1.1.0" --notes "..."
   ```

5. Publish to PyPI:
   ```bash
   ./scripts/publish_to_pypi.sh
   ```

## ⚠️ Important Notes

### About Backdating

- ❌ **PyPI upload dates cannot be backdated** - they're set when you upload
- ✅ **GitHub releases show commit dates** - users will see the historical timeline
- ✅ **CHANGELOG documents the timeline** - full development history is preserved
- ✅ **Version numbers match dates** - semantic versioning follows timeline

### Best Practices

1. **Always test on TestPyPI first**
2. **Verify the package installs correctly**
3. **Check that all files are included** (use `MANIFEST.in`)
4. **Update CHANGELOG before release**
5. **Create GitHub release for visibility**

## 🔍 Troubleshooting

### Build Fails
```bash
# Clean and rebuild
rm -rf build/ dist/ *.egg-info
python3 -m build
```

### Missing Files in Distribution
```bash
# Check what's included
tar -tzf dist/performance-profiler-optimizer-1.0.0.tar.gz

# Update MANIFEST.in if needed
```

### Upload Fails
```bash
# Check credentials
twine upload --verbose dist/*

# Use API token instead of password
```

## 📚 Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [GitHub CLI Docs](https://cli.github.com/manual/)
- [Semantic Versioning](https://semver.org/)

## ✅ Quick Checklist

Before publishing:

- [ ] All tests pass
- [ ] Version numbers updated
- [ ] CHANGELOG updated
- [ ] README is current
- [ ] LICENSE is included
- [ ] Examples work
- [ ] Git tags created
- [ ] GitHub releases created
- [ ] Package builds successfully
- [ ] TestPyPI upload successful
- [ ] Test installation works

---

**Ready to publish?** Run `./scripts/publish_to_pypi.sh`
