# Startup Automation Framework - Structure

## Location
The startup automation framework is now consolidated in:
```
domains/my-startups/automation-framework/
```

This aligns with your existing personal startup management structure in `domains/my-startups/`.

## Directory Structure

```
domains/my-startups/
├── automation-framework/      # Reusable automation system
│   ├── templates/            # Automation templates
│   │   ├── sales/           # Sales automation
│   │   ├── operations/      # Operations automation
│   │   ├── team/            # Team management
│   │   └── finance/         # Financial automation
│   ├── configs/             # Configuration files
│   │   ├── startup-types/   # PropTech, SaaS, etc.
│   │   └── stages/          # MVP, Growth, Scale
│   ├── deployment/          # Deployment scripts
│   │   └── setup/           # Setup and configuration
│   └── documentation/       # Guides and best practices
├── co-founders/             # Co-founder agreements
├── ideas/                   # Startup ideas
├── operations/              # Operations templates
├── shared/                  # Shared documents
└── smart-contracts/         # Blockchain contracts
```

## How It Works

### 1. Framework Location
- **Framework**: `domains/my-startups/automation-framework/`
- **Active Startups**: `domains/my-startups/StartupName/` (directly within my-startups)
- **Templates**: Shared across all startups
- **Configurations**: Startup-type and stage-specific

### 2. Startup Creation
When you create a new startup, it goes into:
```
domains/my-startups/StartupName/
├── automation/              # Deployed automations
├── configs/                # Startup-specific config
├── monitoring/             # Dashboards and reports
└── documentation/          # Startup documentation
```

### 3. Automation Deployment
The framework deploys automations from templates to your active startups:
```bash
# From framework directory
cd domains/my-startups/automation-framework

# Deploy to active startup
./deployment/setup/deploy-automations.sh --startup "Tango.Vision" --template sales
```

## Benefits of This Structure

### 1. **Consolidated Management**
- All startup-related content in one domain
- Clear separation between framework and active startups
- Easy to manage multiple ventures

### 2. **Reusable Framework**
- Templates shared across all startups
- Consistent processes and best practices
- Easy to add new startup types

### 3. **Scalable Organization**
- Framework grows with your portfolio
- Each startup gets its own automation instance
- Easy to compare and optimize across startups

### 4. **Personal System Integration**
- Fits naturally with your existing domain structure
- Aligns with your personal knowledge management
- Maintains consistency across your system

## Usage Examples

### For Tango.Vision
```bash
# Navigate to framework
cd domains/my-startups/automation-framework

# Initialize Tango.Vision
./deployment/setup/init-startup.sh --type proptech --stage growth --name "Tango.Vision"

# Deploy automations
./deployment/setup/deploy-automations.sh --startup "Tango.Vision" --template sales
./deployment/setup/deploy-automations.sh --startup "Tango.Vision" --template operations

# Result: Tango.Vision automation in domains/my-startups/Tango.Vision/
```

### For Future Startups
```bash
# SaaS Startup
./deployment/setup/init-startup.sh --type saas --stage mvp --name "MySaaS"
# Creates: domains/my-startups/MySaaS/

# E-commerce Startup
./deployment/setup/init-startup.sh --type ecommerce --stage early-growth --name "MyStore"
# Creates: domains/my-startups/MyStore/
```

## Integration with Existing Structure

### Your Current `domains/my-startups/` Structure
- ✅ **Tango.Vision/**: Active startup with automation framework
- ✅ **co-founders/**: Co-founder agreements and templates
- ✅ **ideas/**: Startup ideas and validation
- ✅ **operations/**: Operations templates and processes
- ✅ **shared/**: Shared documents and resources
- ✅ **smart-contracts/**: Blockchain-based agreements

### New Addition
- ✅ **automation-framework/**: Reusable automation system

## Next Steps

### 1. **Initialize Tango.Vision**
```bash
cd domains/my-startups/automation-framework
./deployment/setup/init-startup.sh --type proptech --stage growth --name "Tango.Vision"
```

### 2. **Deploy Automations**
```bash
cd ../Tango.Vision
./deploy-automations.sh --startup "Tango.Vision" --template sales
./deploy-automations.sh --startup "Tango.Vision" --template operations
```

### 3. **Set Up Monitoring**
```bash
./setup-monitoring.sh --startup "Tango.Vision"
```

### 4. **Future Startups**
Use the same framework for all future startups, keeping everything organized in your `domains/my-startups/` structure.

---

**This structure gives you a professional, scalable system for managing automation across all your startups while maintaining consistency with your personal knowledge management system.**
