# 🏥 System Health Dashboard

## Purpose
A comprehensive monitoring tool that provides real-time overview of all Personal System components, including uptimes, health status, resource usage, and system metrics.

## Quick Start
```bash
# Start interactive dashboard (refreshes every 30 seconds)
python3 automation/tools/system_health_dashboard/main.py --dashboard

# Generate one-time report
python3 automation/tools/system_health_dashboard/main.py --report

# Save report to file
python3 automation/tools/system_health_dashboard/main.py --save health_report.txt

# Output metrics in JSON format
python3 automation/tools/system_health_dashboard/main.py --json

# Custom refresh interval (60 seconds)
python3 automation/tools/system_health_dashboard/main.py --dashboard --refresh 60
```

## Features

### 📊 Real-Time Monitoring
- **Component Status**: Track all system components (core apps, project apps, automation tools, serverless functions, external services)
- **Health Scores**: Individual health scores (0-100) for each component
- **Resource Usage**: CPU, memory, and disk usage monitoring
- **Network Status**: Internet connectivity checks
- **Process Monitoring**: PID tracking and process health

### 🎯 Component Categories
- **Core Apps**: PersonalSystemBot, PersonalSystemAPI
- **Project Apps**: HabitTracker, PresentationAnalyzer
- **Automation Tools**: TaskManager, DailySummary, CleanupTool, CodeQualityChecker, LabAnalyzer, ReminderSystem
- **Serverless Functions**: DailySummaryLambda, DailyVoiceLambda, VoiceTranscription
- **External Services**: TelegramAPI, Supabase, ElevenLabs, OpenAI
- **Containers**: GitServer, CoolifyDeployer

### 🎛️ Dashboard Features
- **Interactive Mode**: Real-time dashboard with auto-refresh
- **Health Scoring**: Overall system health score calculation
- **Recommendations**: Automated recommendations based on current status
- **History Tracking**: Metrics history for trend analysis
- **Multiple Output Formats**: Console, file, JSON

## Configuration

### Component Definitions
Edit `config.yaml` to customize component monitoring:

```yaml
components:
  core_apps:
    - name: "YourComponent"
      type: "core_app"
      port: 8080
      process_name: "python"
      start_script: "start_your_component.sh"
      dependencies: ["REQUIRED_ENV_VAR"]
      description: "Component description"
```

### Monitoring Settings
```yaml
monitoring:
  check_ports: true          # Check if ports are open
  check_processes: true      # Check if processes are running
  check_services: true       # Check service health
  check_disk_space: true     # Monitor disk usage
  check_memory: true         # Monitor memory usage
  check_network: true        # Check network connectivity
```

### Alert Thresholds
```yaml
alerts:
  critical_threshold: 80     # Health score for critical alerts
  warning_threshold: 60      # Health score for warning alerts
```

## Usage Examples

### Interactive Dashboard
```bash
# Start dashboard with default settings
python3 automation/tools/system_health_dashboard/main.py --dashboard

# Custom refresh interval
python3 automation/tools/system_health_dashboard/main.py --dashboard --refresh 10
```

### One-Time Reports
```bash
# Generate and display report
python3 automation/tools/system_health_dashboard/main.py --report

# Save report with timestamp
python3 automation/tools/system_health_dashboard/main.py --save

# Save with custom filename
python3 automation/tools/system_health_dashboard/main.py --save my_report.txt
```

### JSON Output
```bash
# Get metrics in JSON format for scripting
python3 automation/tools/system_health_dashboard/main.py --json
```

### Custom Configuration
```bash
# Use custom config file
python3 automation/tools/system_health_dashboard/main.py --config my_config.yaml --dashboard
```

## Health Score Calculation

### Component Health Scores
- **100**: Perfect health (all checks pass)
- **90-99**: Excellent (minor issues)
- **70-89**: Good (some warnings)
- **50-69**: Fair (multiple issues)
- **0-49**: Poor (critical issues)

### Overall System Score
- Based on healthy component ratio
- Weighted by component importance
- Penalties for high resource usage
- Network connectivity factor

## Output Examples

### Dashboard Report
```
🏥 PERSONAL SYSTEM HEALTH DASHBOARD
============================================================
📊 System Overview
============================================================
🕐 Last Updated: 2024-01-15 14:30:25
⏱️  System Uptime: 2 days, 5:30:15
🌐 Network Status: ✅ Connected

📈 Overall Health Score: 87/100
💾 Memory Usage: 45.2%
🖥️  CPU Usage: 12.8%
💿 Disk Usage: 67.3%

📊 Component Status Summary
============================================================
Total Components: 15
✅ Healthy: 12
⚠️  Warning: 2
🔴 Critical: 1
🟢 Running: 13

🔧 Component Details
============================================================

📁 Core Apps:
----------------------------------------
✅ PersonalSystemBot     Health:  95/100 Port: None PID: 1234 RAM: 2.1% CPU: 0.5%
✅ PersonalSystemAPI     Health:  90/100 Port: 8000 PID: 1235 RAM: 1.8% CPU: 0.3%

📁 Project Apps:
----------------------------------------
✅ HabitTracker          Health:  95/100 Port: 5000 PID: 1236 RAM: 1.2% CPU: 0.1%
⚠️  PresentationAnalyzer Health:  75/100 Port: None PID: None RAM: 0.0% CPU: 0.0%
    ⚠️  Process not running

💡 Recommendations
============================================================
1. ⚠️  1 components have warnings that should be addressed
2. 🎉 All systems are running smoothly!
```

## Integration

### With Telegram Bot
The dashboard can be integrated with the Telegram bot for remote monitoring:

```python
# In telegram bot handlers
from automation.tools.system_health_dashboard.main import SystemHealthDashboard

dashboard = SystemHealthDashboard()
report = dashboard.generate_dashboard_report()
await update.message.reply_text(f"```\n{report}\n```", parse_mode='Markdown')
```

### With Automation Scripts
Use in automation scripts for health checks:

```bash
#!/bin/bash
# Check system health before running critical operations
python3 automation/tools/system_health_dashboard/main.py --json > /tmp/health.json
HEALTH_SCORE=$(jq '.health_score' /tmp/health.json)

if [ "$HEALTH_SCORE" -lt 70 ]; then
    echo "System health is poor ($HEALTH_SCORE/100). Aborting operation."
    exit 1
fi
```

### With Cron Jobs
Set up automated health monitoring:

```bash
# Add to crontab for hourly health reports
0 * * * * cd /path/to/personal-system && python3 automation/tools/system_health_dashboard/main.py --save hourly_health_$(date +\%Y\%m\%d_\%H).txt
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x automation/tools/system_health_dashboard/main.py
   ```

2. **Missing Dependencies**
   ```bash
   pip install psutil requests pyyaml
   ```

3. **Configuration Errors**
   - Check YAML syntax in config.yaml
   - Verify component definitions
   - Ensure environment variables are set

4. **Process Detection Issues**
   - Verify process names in config
   - Check if processes are actually running
   - Use `ps aux | grep python` to verify

### Debug Mode
```bash
# Enable debug logging
export PYTHONPATH=/path/to/personal-system
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from automation.tools.system_health_dashboard.main import SystemHealthDashboard
dashboard = SystemHealthDashboard()
dashboard.generate_dashboard_report()
"
```

## Dependencies

### Required Python Packages
- `psutil` - System and process monitoring
- `requests` - HTTP requests for external service checks
- `pyyaml` - Configuration file parsing

### System Requirements
- Python 3.8+
- Access to system processes (psutil)
- Network connectivity for external service checks
- Read access to configuration files

## Future Enhancements

### Planned Features
- **Web Dashboard**: Browser-based dashboard interface
- **Alert Notifications**: Email/SMS alerts for critical issues
- **Historical Trends**: Long-term health trend analysis
- **Performance Metrics**: Response time and throughput monitoring
- **Auto-Recovery**: Automatic restart of failed components
- **Integration APIs**: REST API for external monitoring tools

### Custom Metrics
- Add custom health check functions
- Monitor application-specific metrics
- Integration with external monitoring services
- Custom alert rules and thresholds

---

*The System Health Dashboard provides comprehensive monitoring for your Personal System, ensuring all components are running smoothly and helping you maintain optimal system performance.* 🏥✨
