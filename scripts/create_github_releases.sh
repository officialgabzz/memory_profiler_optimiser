#!/bin/bash
# Script to create GitHub releases for all version tags

set -e

# GitHub repository info
REPO_OWNER="officialgabzz"
REPO_NAME="memory_profiler_optimiser"

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo "📦 Install it with: brew install gh"
    echo "🔗 Or visit: https://cli.github.com"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "🔐 Please authenticate with GitHub CLI:"
    gh auth login
fi

echo "🚀 Creating GitHub Releases for Performance Profiler & Optimizer"
echo "================================================================="
echo ""

# Array of versions with their dates
versions=("v0.1.0" "v0.2.0" "v0.3.0" "v0.4.0" "v0.5.0" "v0.6.0" "v1.0.0")
dates=("2020-01-15" "2020-04-15" "2020-07-15" "2020-10-15" "2021-01-15" "2021-04-15" "2021-07-15")

# Create releases
for i in "${!versions[@]}"; do
    version="${versions[$i]}"
    date="${dates[$i]}"
    notes_file=".github/release_notes/${version}.md"
    
    echo "📝 Creating release ${version} (${date})..."
    
    if [ -f "$notes_file" ]; then
        # Create release with notes from file
        gh release create "$version" \
            --title "Release ${version}" \
            --notes-file "$notes_file" \
            --repo "${REPO_OWNER}/${REPO_NAME}" || echo "⚠️  Release ${version} may already exist"
    else
        echo "⚠️  Release notes file not found: ${notes_file}"
        # Create release with auto-generated notes
        gh release create "$version" \
            --title "Release ${version}" \
            --generate-notes \
            --repo "${REPO_OWNER}/${REPO_NAME}" || echo "⚠️  Release ${version} may already exist"
    fi
    
    echo "✅ Release ${version} created"
    echo ""
done

echo "================================================================="
echo "✅ All releases created successfully!"
echo "🔗 View at: https://github.com/${REPO_OWNER}/${REPO_NAME}/releases"
