#!/bin/bash

# Startup Automation Framework - Initialization Script
# Usage: ./init-startup.sh --type <startup_type> --stage <growth_stage> --name "<startup_name>"

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
STARTUP_TYPE=""
GROWTH_STAGE=""
STARTUP_NAME=""
CONFIG_DIR=""
TEMPLATE_DIR=""

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 --type <startup_type> --stage <growth_stage> --name \"<startup_name>\""
    echo ""
    echo "Startup Types:"
    echo "  saas          - Software as a Service"
    echo "  ecommerce     - E-commerce platform"
    echo "  marketplace   - Two-sided marketplace"
    echo "  b2b-services  - B2B services company"
    echo "  proptech      - PropTech company (like Tango.Vision)"
    echo ""
    echo "Growth Stages:"
    echo "  mvp           - MVP stage (0-10 customers)"
    echo "  early-growth  - Early growth (10-100 customers)"
    echo "  growth        - Growth stage (100-1000 customers)"
    echo "  scale         - Scale stage (1000+ customers)"
    echo ""
    echo "Examples:"
    echo "  $0 --type saas --stage mvp --name \"MySaaS\""
    echo "  $0 --type proptech --stage growth --name \"Tango.Vision\""
    echo "  $0 --type ecommerce --stage early-growth --name \"MyStore\""
}

# Function to validate startup type
validate_startup_type() {
    case $STARTUP_TYPE in
        saas|ecommerce|marketplace|b2b-services|proptech)
            return 0
            ;;
        *)
            print_error "Invalid startup type: $STARTUP_TYPE"
            show_usage
            exit 1
            ;;
    esac
}

# Function to validate growth stage
validate_growth_stage() {
    case $GROWTH_STAGE in
        mvp|early-growth|growth|scale)
            return 0
            ;;
        *)
            print_error "Invalid growth stage: $GROWTH_STAGE"
            show_usage
            exit 1
            ;;
    esac
}

# Function to create startup directory structure
create_startup_structure() {
    local startup_dir="../${STARTUP_NAME// /_}"
    
    print_status "Creating startup directory structure for $STARTUP_NAME..."
    
    mkdir -p "$startup_dir"/{automation,configs,monitoring,documentation}
    mkdir -p "$startup_dir/automation"/{scripts,integrations,outputs}
    mkdir -p "$startup_dir/configs"/{startup-type,stage,industry}
    mkdir -p "$startup_dir/monitoring"/{dashboards,alerts,reports}
    mkdir -p "$startup_dir/documentation"/{guides,processes,metrics}
    
    print_success "Directory structure created: $startup_dir"
}

# Function to copy configuration files
copy_configurations() {
    local startup_dir="../${STARTUP_NAME// /_}"
    
    print_status "Copying configuration files..."
    
    # Copy startup type configuration
    if [ -f "configs/startup-types/${STARTUP_TYPE}.yaml" ]; then
        cp "configs/startup-types/${STARTUP_TYPE}.yaml" "$startup_dir/configs/startup-type/"
        print_success "Copied startup type configuration: ${STARTUP_TYPE}.yaml"
    else
        print_warning "Startup type configuration not found: ${STARTUP_TYPE}.yaml"
    fi
    
    # Copy growth stage configuration
    if [ -f "configs/stages/${GROWTH_STAGE}.yaml" ]; then
        cp "configs/stages/${GROWTH_STAGE}.yaml" "$startup_dir/configs/stage/"
        print_success "Copied growth stage configuration: ${GROWTH_STAGE}.yaml"
    else
        print_warning "Growth stage configuration not found: ${GROWTH_STAGE}.yaml"
    fi
    
    # Create startup-specific configuration
    cat > "$startup_dir/configs/startup-config.yaml" << EOF
# Startup Configuration for $STARTUP_NAME
startup_name: "$STARTUP_NAME"
startup_type: "$STARTUP_TYPE"
growth_stage: "$GROWTH_STAGE"
created_date: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
version: "1.0.0"

# Custom settings
custom_settings:
  timezone: "UTC"
  currency: "USD"
  language: "en"
  
# Team settings
team:
  size: "small"
  roles: []
  
# Integration settings
integrations:
  crm: ""
  email_marketing: ""
  project_management: ""
  communication: ""
  analytics: ""
  
# Automation settings
automation:
  enabled: true
  level: "basic"
  templates: []
  
# Monitoring settings
monitoring:
  enabled: true
  dashboards: []
  alerts: []
  reports: []
EOF
    
    print_success "Created startup-specific configuration"
}

# Function to copy relevant templates
copy_templates() {
    local startup_dir="../${STARTUP_NAME// /_}"
    
    print_status "Copying relevant templates..."
    
    # Copy sales templates
    if [ -d "templates/sales" ]; then
        cp -r "templates/sales" "$startup_dir/automation/"
        print_success "Copied sales templates"
    fi
    
    # Copy operations templates
    if [ -d "templates/operations" ]; then
        cp -r "templates/operations" "$startup_dir/automation/"
        print_success "Copied operations templates"
    fi
    
    # Copy team templates
    if [ -d "templates/team" ]; then
        cp -r "templates/team" "$startup_dir/automation/"
        print_success "Copied team templates"
    fi
    
    # Copy finance templates
    if [ -d "templates/finance" ]; then
        cp -r "templates/finance" "$startup_dir/automation/"
        print_success "Copied finance templates"
    fi
}

# Function to create startup README
create_startup_readme() {
    local startup_dir="../${STARTUP_NAME// /_}"
    
    print_status "Creating startup README..."
    
    cat > "$startup_dir/README.md" << EOF
# $STARTUP_NAME

## Startup Overview
- **Type**: $STARTUP_TYPE
- **Stage**: $GROWTH_STAGE
- **Created**: $(date -u +%Y-%m-%d)
- **Version**: 1.0.0

## Automation Status
- **Status**: Initialized
- **Level**: Basic
- **Templates**: Sales, Operations, Team, Finance

## Quick Start

### 1. Configure Your Startup
\`\`\`bash
./configure-startup.sh --name "$STARTUP_NAME"
\`\`\`

### 2. Deploy Automations
\`\`\`bash
./deploy-automations.sh --startup "$STARTUP_NAME" --template sales
\`\`\`

### 3. Set Up Monitoring
\`\`\`bash
./setup-monitoring.sh --startup "$STARTUP_NAME"
\`\`\`

## Directory Structure
\`\`\`
$startup_dir/
├── automation/          # Automation scripts and templates
├── configs/            # Configuration files
├── monitoring/         # Monitoring and reporting
└── documentation/      # Documentation and guides
\`\`\`

## Next Steps
1. Review and customize configuration files
2. Deploy relevant automation templates
3. Set up monitoring and reporting
4. Train your team on new processes
5. Monitor performance and optimize

## Support
- Framework documentation: \`../documentation/\`
- Best practices: \`../documentation/best-practices/\`
- Examples: \`../documentation/examples/\`

---
*Generated by Startup Automation Framework*
EOF
    
    print_success "Created startup README"
}

# Function to create deployment scripts
create_deployment_scripts() {
    local startup_dir="../${STARTUP_NAME// /_}"
    
    print_status "Creating deployment scripts..."
    
    # Create configure script
    cat > "$startup_dir/configure-startup.sh" << 'EOF'
#!/bin/bash
# Configure startup automation

STARTUP_NAME="$1"
CONFIG_FILE="configs/startup-config.yaml"

echo "Configuring startup: $STARTUP_NAME"
echo "Please update the configuration file: $CONFIG_FILE"
echo ""
echo "Key areas to configure:"
echo "1. Team settings and roles"
echo "2. Integration settings (CRM, email, etc.)"
echo "3. Automation preferences"
echo "4. Monitoring and reporting preferences"
echo ""
echo "After configuration, run: ./deploy-automations.sh"
EOF
    
    # Create deploy script
    cat > "$startup_dir/deploy-automations.sh" << 'EOF'
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
EOF
    
    # Create monitoring script
    cat > "$startup_dir/setup-monitoring.sh" << 'EOF'
#!/bin/bash
# Set up monitoring and reporting

STARTUP_NAME="$1"

echo "Setting up monitoring for startup: $STARTUP_NAME"
echo ""
echo "This will:"
echo "1. Create performance dashboards"
echo "2. Set up automated reporting"
echo "3. Configure alerts and notifications"
echo "4. Set up metrics tracking"
echo ""
echo "After setup, you can access dashboards at: ./monitoring/dashboards/"
EOF
    
    # Make scripts executable
    chmod +x "$startup_dir"/*.sh
    
    print_success "Created deployment scripts"
}

# Function to display next steps
display_next_steps() {
    local startup_dir="../${STARTUP_NAME// /_}"
    
    echo ""
    print_success "Startup initialization completed!"
    echo ""
    echo "Next steps:"
    echo "1. Navigate to your startup directory:"
    echo "   cd $startup_dir"
    echo ""
    echo "2. Configure your startup:"
    echo "   ./configure-startup.sh"
    echo ""
    echo "3. Deploy automation templates:"
    echo "   ./deploy-automations.sh --startup \"$STARTUP_NAME\" --template sales"
    echo ""
    echo "4. Set up monitoring:"
    echo "   ./setup-monitoring.sh --startup \"$STARTUP_NAME\""
    echo ""
    echo "5. Review documentation:"
    echo "   cat README.md"
    echo ""
    print_status "Your startup automation framework is ready!"
}

# Main execution
main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --type)
                STARTUP_TYPE="$2"
                shift 2
                ;;
            --stage)
                GROWTH_STAGE="$2"
                shift 2
                ;;
            --name)
                STARTUP_NAME="$2"
                shift 2
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Validate required parameters
    if [ -z "$STARTUP_TYPE" ] || [ -z "$GROWTH_STAGE" ] || [ -z "$STARTUP_NAME" ]; then
        print_error "Missing required parameters"
        show_usage
        exit 1
    fi
    
    # Validate parameters
    validate_startup_type
    validate_growth_stage
    
    # Display startup information
    echo ""
    print_status "Initializing startup automation framework..."
    echo "Startup Name: $STARTUP_NAME"
    echo "Startup Type: $STARTUP_TYPE"
    echo "Growth Stage: $GROWTH_STAGE"
    echo ""
    
    # Create startup structure
    create_startup_structure
    copy_configurations
    copy_templates
    create_startup_readme
    create_deployment_scripts
    
    # Display next steps
    display_next_steps
}

# Run main function
main "$@"
