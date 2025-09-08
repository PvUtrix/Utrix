#!/bin/bash

# Serverless Runner Script
# Easy command execution from automation directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_help() {
    echo -e "${BLUE}Serverless Management Commands${NC}"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  setup          Initialize databases and setup"
    echo "  monitor        Show database sizes and status"
    echo "  sync           Run data synchronization"
    echo "  lifecycle      Process data lifecycle management"
    echo "  deploy         Deploy serverless functions"
    echo "  alert          Send monitoring alert"
    echo "  report         Generate comprehensive report"
    echo "  archive        Run home server archiving"
    echo "  cleanup        Clean up old archives"
    echo ""
    echo "Voice Commands:"
    echo "  voice-send     Send daily voice message"
    echo "  voice-preview  Preview today's voice content"
    echo "  voice-history  Show voice message history"
    echo "  voice-test     Test ElevenLabs integration"
    echo ""
    echo "CI/CD Commands:"
    echo "  cicd-deploy    Trigger CI/CD deployment"
    echo "  cicd-status    Check deployment status"
    echo "  cicd-logs      Get deployment logs"
    echo "  webhook-test   Test Gitea webhook handling"
    echo "  coolify-list   List Coolify deployments"
    echo ""
    echo "Prosperity Course Commands:"
    echo "  course-status  Show course progress"
    echo "  course-pause   Pause the course"
    echo "  course-resume  Resume the course"
    echo "  course-reset   Reset course progress"
    echo "  course-journal Create journal template for today"
    echo ""
    echo "Examples:"
    echo "  $0 setup --all"
    echo "  $0 monitor --sizes"
    echo "  $0 voice-preview"
    echo "  $0 cicd-deploy"
}

run_setup() {
    echo -e "${GREEN}🚀 Running setup...${NC}"
    python3 multi_tier_setup.py "$@"
}

run_monitor() {
    echo -e "${GREEN}📊 Running monitor...${NC}"
    python3 data_monitor.py "$@"
}

run_sync() {
    echo -e "${GREEN}🔄 Running sync...${NC}"
    python3 data_sync_manager.py "$@"
}

run_lifecycle() {
    echo -e "${GREEN}🔄 Running lifecycle management...${NC}"
    python3 data_lifecycle_manager.py "$@"
}

run_deploy() {
    echo -e "${GREEN}🚀 Running deployment...${NC}"
    ./deploy.sh "$@"
}

run_archive() {
    echo -e "${GREEN}📦 Running archiving...${NC}"
    python3 home_server_archiver.py "$@"
}

run_voice_send() {
    echo -e "${GREEN}🎤 Sending daily voice message...${NC}"
    python3 daily_voice_lambda.py send_daily
}

run_voice_preview() {
    echo -e "${GREEN}🎤 Generating voice preview...${NC}"
    python3 daily_voice_lambda.py preview
}

run_voice_history() {
    echo -e "${GREEN}📚 Getting voice message history...${NC}"
    python3 daily_voice_lambda.py history "$@"
}

run_voice_test() {
    echo -e "${GREEN}🧪 Testing ElevenLabs integration...${NC}"
    python3 elevenlabs_tts.py test
}

run_cicd_deploy() {
    echo -e "${GREEN}🚀 Triggering CI/CD deployment...${NC}"
    python3 cicd_orchestrator.py
}

run_cicd_status() {
    echo -e "${GREEN}📊 Checking deployment status...${NC}"
    python3 coolify_deployer.py status "$@"
}

run_cicd_logs() {
    echo -e "${GREEN}📋 Getting deployment logs...${NC}"
    python3 coolify_deployer.py logs "$@"
}

run_webhook_test() {
    echo -e "${GREEN}🎣 Testing webhook handling...${NC}"
    python3 gitea_webhook_handler.py
}

run_coolify_list() {
    echo -e "${GREEN}📦 Listing Coolify deployments...${NC}"
    python3 coolify_deployer.py list
}

# Prosperity Course Functions
run_course_status() {
    echo -e "${GREEN}🎯 Checking prosperity course status...${NC}"
    python3 ../../automation/scripts/prosperity-course-manager.py status
}

run_course_pause() {
    echo -e "${GREEN}⏸️ Pausing prosperity course...${NC}"
    python3 ../../automation/scripts/prosperity-course-manager.py pause
}

run_course_resume() {
    echo -e "${GREEN}▶️ Resuming prosperity course...${NC}"
    python3 ../../automation/scripts/prosperity-course-manager.py resume
}

run_course_reset() {
    echo -e "${GREEN}🔄 Resetting prosperity course...${NC}"
    python3 ../../automation/scripts/prosperity-course-manager.py reset
}

run_course_journal() {
    echo -e "${GREEN}📝 Creating journal template...${NC}"
    # Get current day from course status
    python3 ../../automation/scripts/prosperity-course-manager.py journal $(python3 -c "
import json
from pathlib import Path
from datetime import datetime
config_path = Path('../../domains/learning/prosperity-course-config.json')
if config_path.exists():
    with open(config_path, 'r') as f:
        config = json.load(f)
    start_date = datetime.strptime(config['start_date'], '%Y-%m-%d')
    current_date = datetime.now()
    days_into_course = (current_date - start_date).days + 1
    if 1 <= days_into_course <= 5:
        print(days_into_course)
    else:
        print(1)
else:
    print(1)
")
}

case "$1" in
    "setup")
        shift
        run_setup "$@"
        ;;
    "monitor")
        shift
        run_monitor "$@"
        ;;
    "sync")
        shift
        run_sync "$@"
        ;;
    "lifecycle")
        shift
        run_lifecycle "$@"
        ;;
    "deploy")
        shift
        run_deploy "$@"
        ;;
    "alert")
        run_monitor --alert
        ;;
    "report")
        run_monitor --report
        ;;
    "archive")
        shift
        run_archive "$@"
        ;;
    "cleanup")
        run_archive --cleanup
        ;;
    "voice-send")
        run_voice_send
        ;;
    "voice-preview")
        run_voice_preview
        ;;
    "voice-history")
        shift
        run_voice_history "$@"
        ;;
    "voice-test")
        run_voice_test
        ;;
    "cicd-deploy")
        run_cicd_deploy
        ;;
    "cicd-status")
        shift
        run_cicd_status "$@"
        ;;
    "cicd-logs")
        shift
        run_cicd_logs "$@"
        ;;
    "webhook-test")
        run_webhook_test
        ;;
    "coolify-list")
        run_coolify_list
        ;;
    "course-status")
        run_course_status
        ;;
    "course-pause")
        run_course_pause
        ;;
    "course-resume")
        run_course_resume
        ;;
    "course-reset")
        run_course_reset
        ;;
    "course-journal")
        run_course_journal
        ;;
    "help"|"-h"|"--help"|"")
        print_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        print_help
        exit 1
        ;;
esac
