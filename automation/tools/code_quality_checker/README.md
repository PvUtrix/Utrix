# Code Quality Checker

## Purpose
A comprehensive tool for checking and improving code quality across the personal system, ensuring adherence to development standards.

## Quick Start
```bash
# Run quality check on all Python files
python3 automation/tools/code_quality_checker/main.py --check-all

# Check specific directory
python3 automation/tools/code_quality_checker/main.py --path automation/scripts

# Fix common issues automatically
python3 automation/tools/code_quality_checker/main.py --fix
```

## Configuration
Edit `code_quality_config.yaml` to customize quality checks:
- Type hint requirements
- Docstring standards
- Logging requirements
- Error handling patterns

## Usage Examples
```bash
# Check for missing type hints
python3 automation/tools/code_quality_checker/main.py --check-type-hints

# Check for missing docstrings
python3 automation/tools/code_quality_checker/main.py --check-docstrings

# Check logging usage
python3 automation/tools/code_quality_checker/main.py --check-logging
```

## Troubleshooting
- **Import errors**: Ensure all dependencies are installed
- **Permission errors**: Run with appropriate file permissions
- **Large codebases**: Use --path to check specific directories

## Integration
This tool integrates with the broader system:
- Uses system logging configuration
- Follows automation tool standards
- Generates reports in `automation/outputs/`
- Integrates with CI/CD pipelines
