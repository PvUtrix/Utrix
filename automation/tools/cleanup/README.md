# 🧹 Automated Cleanup System

An intelligent file cleanup system that automatically identifies and manages temporary files, test files, build artifacts, and redundant documentation.

## 🎯 Features

- **🔍 Smart Detection**: Automatically identifies cleanup candidates based on patterns
- **🏷️ File Marking**: Marks files for review instead of immediately removing them
- **📦 Safe Backup**: Creates backups before removing files
- **📊 Detailed Reporting**: Generates comprehensive cleanup reports
- **🔧 Configurable**: Fully customizable cleanup rules via YAML config
- **🎮 Interactive Mode**: Guided cleanup with user confirmation
- **🔗 Git Integration**: Pre-commit and pre-push hooks for automatic cleanup

## 🚀 Quick Start

### 1. Setup Git Hooks (Recommended)
```bash
# Install automatic cleanup hooks
./automation/tools/cleanup/setup_cleanup_hooks.sh
```

### 2. Run Cleanup
```bash
# Interactive cleanup (recommended for first use)
python3 automation/tools/cleanup/cleanup.py

# Or use the full script directly
python3 automation/tools/cleanup/automated_cleanup.py --interactive
```

### 3. Dry Run (See What Would Be Cleaned)
```bash
python3 automation/tools/cleanup/automated_cleanup.py --dry-run
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `python3 automation/tools/cleanup/cleanup.py` | Interactive cleanup menu |
| `python3 automation/tools/cleanup/automated_cleanup.py --dry-run` | Show what would be cleaned |
| `python3 automation/tools/cleanup/automated_cleanup.py --interactive` | Guided cleanup |
| `python3 automation/tools/cleanup/automated_cleanup.py` | Automatic cleanup |
| `./automation/tools/cleanup/setup_cleanup_hooks.sh` | Install git hooks |

## ⚙️ Configuration

Edit `automation/tools/cleanup/cleanup_config.yaml` to customize cleanup rules:

### File Categories

- **Auto Remove**: Files that are automatically removed (test files, build artifacts, etc.)
- **Mark for Review**: Files that are marked for manual review
- **Preserve**: Files that are never touched (README.md, LICENSE, etc.)

### Example Configuration

```yaml
auto_remove:
  test_files:
    - "**/test_*.py"
    - "**/test_*.js"
    - "**/test_output.*"
  
  build_artifacts:
    - "**/node_modules/"
    - "**/__pycache__/"
    - "**/*.zip"

preserve:
  - "README.md"
  - "LICENSE"
  - "requirements.txt"
```

## 🔧 Git Hooks

The system includes git hooks for automatic cleanup:

### Pre-commit Hook
- Runs cleanup before each commit
- Asks for confirmation before cleaning
- Ensures clean commits

### Pre-push Hook
- Checks for cleanup candidates before pushing
- Warns about files that should be cleaned
- Prevents pushing with unnecessary files

## 📊 Cleanup Reports

After each cleanup, the system generates:

- **Console Output**: Real-time cleanup progress
- **Log File**: `logs/cleanup.log` - Detailed operation log
- **Summary Report**: `logs/cleanup_summary.md` - Cleanup statistics and results

## 🛡️ Safety Features

- **Backup System**: Creates backups before removing files
- **Dry Run Mode**: Preview changes without making them
- **Interactive Confirmation**: User approval for all operations
- **Preserve Lists**: Never touches important files
- **Error Handling**: Graceful handling of permission issues

## 📁 File Classification

### Auto-Remove Files
- Test files (`test_*.py`, `*_test.py`)
- Build artifacts (`node_modules/`, `__pycache__/`)
- Temporary files (`.env.old`, `*.tmp`)
- Redundant documentation (`DEPLOYMENT_STATUS.md`)

### Mark for Review
- Multiple config variants (`serverless-*.yml`)
- Documentation duplicates (`README.md.backup`)
- Fix scripts (`fix_*.sh`)

### Preserved Files
- Core files (`README.md`, `LICENSE`, `main.py`)
- Configuration files (`config.yaml`, `.env.example`)
- Essential documentation

## 🎮 Usage Examples

### First-Time Setup
```bash
# 1. Install git hooks
./automation/tools/setup_cleanup_hooks.sh

# 2. Run interactive cleanup
python3 automation/tools/cleanup.py
# Choose option 2 (Interactive cleanup)
```

### Regular Maintenance
```bash
# Quick cleanup check
python3 automation/tools/cleanup/automated_cleanup.py --dry-run

# Automatic cleanup (if you trust the rules)
python3 automation/tools/cleanup/automated_cleanup.py
```

### Custom Cleanup
```bash
# Edit the config file
nano automation/tools/cleanup/cleanup_config.yaml

# Run with custom rules
python3 automation/tools/cleanup/automated_cleanup.py --interactive
```

## 🔍 Troubleshooting

### Common Issues

**"Config file not found"**
```bash
# Ensure config exists
ls automation/tools/cleanup/cleanup_config.yaml
```

**"Permission denied"**
```bash
# Make scripts executable
chmod +x automation/tools/cleanup/cleanup.py
chmod +x automation/tools/cleanup/setup_cleanup_hooks.sh
```

**"Python module not found"**
```bash
# Install required packages
pip install pyyaml
```

### Logs and Debugging

- Check `logs/cleanup.log` for detailed operation logs
- Review `logs/cleanup_summary.md` for cleanup results
- Use `--dry-run` to preview changes safely

## 🎯 Best Practices

1. **Start with Dry Run**: Always preview changes first
2. **Use Interactive Mode**: For important cleanups, use guided mode
3. **Review Config**: Customize rules for your specific needs
4. **Regular Cleanup**: Run cleanup before major commits
5. **Backup Important Files**: The system creates backups, but keep your own too

## 🔄 Integration with Personal System

The cleanup system integrates seamlessly with your personal system:

- **Automated Workflows**: Runs as part of deployment processes
- **Git Integration**: Prevents committing unnecessary files
- **Documentation**: Maintains clean, organized documentation
- **Project Management**: Keeps project directories tidy

## 📈 Future Enhancements

- **Machine Learning**: Learn from user cleanup patterns
- **Cloud Integration**: Clean up cloud storage artifacts
- **Team Collaboration**: Shared cleanup rules for teams
- **Advanced Patterns**: More sophisticated file detection
- **Performance Optimization**: Faster scanning for large repositories

---

*Keep your personal system clean and organized with automated cleanup!* 🧹✨
