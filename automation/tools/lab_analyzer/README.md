# Lab Analyzer

## Purpose
Advanced laboratory result analysis tool for processing, interpreting, and tracking health lab data with intelligent insights and trend analysis.

## Quick Start
```bash
# Analyze lab results
python3 automation/tools/lab_analyzer/main.py --input lab_results.json

# Generate analysis report
python3 automation/tools/lab_analyzer/analyze_results.py --format html
```

## Configuration
Edit `lab_analyzer_config.yaml` to customize analysis parameters:
- Reference ranges for different tests
- Alert thresholds for abnormal values
- Trend analysis settings
- Report generation options

## Usage Examples
```bash
# Basic analysis
python3 automation/tools/lab_analyzer/main.py --input data/lab_results.json --output reports/

# Advanced analysis with trends
python3 automation/tools/lab_analyzer/main.py --input data/lab_results.json --trends --output reports/

# Generate HTML report
python3 automation/tools/lab_analyzer/analyze_results.py --format html --output reports/lab_analysis.html
```

## Troubleshooting
- **File format errors**: Ensure lab results are in supported format (JSON, CSV)
- **Missing data**: Check that all required fields are present
- **Permission errors**: Ensure write access to output directory

## Integration
This tool integrates with the broader system:
- Uses health domain data structure
- Generates reports in `domains/health/`
- Integrates with health tracking workflows
- Supports automated analysis scheduling
