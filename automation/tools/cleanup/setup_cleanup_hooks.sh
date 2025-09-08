#!/bin/bash
# 🔧 Setup Automated Cleanup Git Hooks

echo "🔧 Setting up automated cleanup git hooks..."

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# 🧹 Pre-commit cleanup hook

echo "🧹 Running pre-commit cleanup..."

# Run cleanup in dry-run mode first
python3 automation/tools/cleanup/automated_cleanup.py --dry-run

# Ask user if they want to proceed with cleanup
echo ""
read -p "❓ Proceed with cleanup before commit? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Running cleanup..."
    python3 automation/tools/cleanup/automated_cleanup.py --interactive
    echo "✅ Cleanup completed. Proceeding with commit..."
else
    echo "⏭️  Skipping cleanup. Proceeding with commit..."
fi
EOF

# Create pre-push hook
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
# 🧹 Pre-push cleanup hook

echo "🧹 Running pre-push cleanup check..."

# Run cleanup in dry-run mode
python3 automation/tools/cleanup/automated_cleanup.py --dry-run

# Check if there are files that should be cleaned
if python3 automation/tools/cleanup/automated_cleanup.py --dry-run 2>/dev/null | grep -q "Would remove\|Would mark"; then
    echo ""
    echo "⚠️  Warning: There are files that should be cleaned up."
    echo "Run 'python3 automation/tools/cleanup/automated_cleanup.py --interactive' to clean them."
    echo ""
    read -p "❓ Continue with push anyway? (y/N): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Push cancelled. Please clean up files first."
        exit 1
    fi
fi

echo "✅ Push proceeding..."
EOF

# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push

echo "✅ Git hooks installed successfully!"
echo ""
echo "📋 Available cleanup commands:"
echo "  🧹 python3 automation/tools/cleanup/cleanup.py                    # Interactive menu"
echo "  🔍 python3 automation/tools/cleanup/automated_cleanup.py --dry-run # Preview changes"
echo "  🎯 python3 automation/tools/cleanup/automated_cleanup.py --interactive # Guided cleanup"
echo "  🔧 ./automation/tools/cleanup/setup_cleanup_hooks.sh              # Install git hooks"
echo ""
echo "🔧 Hooks installed:"
echo "  📝 pre-commit: Runs cleanup before commits"
echo "  🚀 pre-push: Checks for cleanup candidates before push"
echo ""
echo "💡 Tip: Edit automation/tools/cleanup/cleanup_config.yaml to customize cleanup rules"
