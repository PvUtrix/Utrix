#!/bin/bash
# Deploy automation templates

STARTUP_NAME="$1"
TEMPLATE="$2"

echo "Deploying automation template: $TEMPLATE"
echo "For startup: $STARTUP_NAME"
echo ""
echo "Available templates:"
echo "- sales: Lead generation, qualification, and sales process"
echo "- operations: Project management and operations"
echo "- team: Team communication and coordination"
echo "- finance: Financial management and reporting"
echo ""
echo "Usage: ./deploy-automations.sh --startup \"$STARTUP_NAME\" --template sales"
