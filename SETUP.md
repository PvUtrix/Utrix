# System Setup Guide

## Prerequisites

- Git for version control
- Text editor (VS Code with Cursor recommended)
- Python 3.8+ for automation scripts (optional)

## Initial Setup

### 1. Clone or Download

```bash
git clone <repository-url> my-personal-system
cd my-personal-system
```

### 2. Personalize Core Identity

Edit these files with your information:
- `core/identity/values.md` - Define your core values
- `core/identity/goals.md` - Set your life goals
- `core/identity/strengths.md` - Document your strengths

### 3. Configure Privacy

```bash
# Create local privacy directories
mkdir -p privacy/local/credentials
mkdir -p privacy/local/personal
mkdir -p privacy/local/sensitive

# These directories are gitignored by default
```

### 4. Select Active Domains

Remove or add domains based on your needs:
- Keep relevant domains in `domains/`
- Delete unused domain folders
- Create custom domains as needed

### 5. Set Up Git (Optional)

```bash
git init
git add .
git commit -m "Initial personal system setup"
```

### 6. Configure Backups

Set up automated backups for the `privacy/local/` directory using your preferred backup solution.

## Next Steps

1. Read domain-specific READMEs
2. Set up automation scripts
3. Import existing data
4. Start daily workflows

## Troubleshooting

See [docs/setup/troubleshooting.md](docs/setup/troubleshooting.md) for common issues.
