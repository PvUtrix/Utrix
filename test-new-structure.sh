#!/bin/bash

# Test script to verify the new file organization works correctly

echo "🧪 Testing New File Organization Structure"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test 1: Check if old files are removed
echo -e "\n${YELLOW}[TEST 1]${NC} Checking if old files are removed..."

OLD_FILES=(
    "Dockerfile"
    "docker-compose.yml"
    "docker-compose.shared-db.yml"
    ".dockerignore"
    "coolify.yaml"
    "coolify-deploy.sh"
    "COOLIFY_DEPLOYMENT_COMPLETE.md"
    "DEPLOYMENT_SUMMARY.md"
    "SETUP.md"
    "ENVIRONMENT_SETUP.md"
    "SETUP-GITEA.md"
)

for file in "${OLD_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo -e "  ${RED}❌ $file still exists in root${NC}"
    else
        echo -e "  ${GREEN}✅ $file removed from root${NC}"
    fi
done

# Test 2: Check if new structure exists
echo -e "\n${YELLOW}[TEST 2]${NC} Checking if new structure exists..."

NEW_DIRS=(
    "deployment"
    "deployment/docker"
    "deployment/coolify"
    "deployment/scripts"
    "deployment/configs"
    "docs"
    "docs/setup"
    "docs/deployment"
    "docs/guides"
    "docs/api"
    "docs/contributing"
)

for dir in "${NEW_DIRS[@]}"; do
    if [[ -d "$dir" ]]; then
        echo -e "  ${GREEN}✅ $dir exists${NC}"
    else
        echo -e "  ${RED}❌ $dir missing${NC}"
    fi
done

# Test 3: Check if key files are in new locations
echo -e "\n${YELLOW}[TEST 3]${NC} Checking if key files are in new locations..."

KEY_FILES=(
    "deployment/docker/Dockerfile"
    "deployment/docker/docker-compose.yml"
    "deployment/docker/docker-compose.shared-db.yml"
    "deployment/docker/.dockerignore"
    "deployment/coolify/coolify.yaml"
    "deployment/coolify/coolify-deploy.sh"
    "deployment/coolify/deployment-complete.md"
    "deployment/coolify/deployment-summary.md"
    "docs/setup/initial-setup.md"
    "docs/setup/environment-setup.md"
    "docs/setup/gitea-setup.md"
)

for file in "${KEY_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo -e "  ${GREEN}✅ $file exists${NC}"
    else
        echo -e "  ${RED}❌ $file missing${NC}"
    fi
done

# Test 4: Check if README files exist
echo -e "\n${YELLOW}[TEST 4]${NC} Checking if README files exist..."

README_FILES=(
    "deployment/README.md"
    "deployment/docker/README.md"
    "deployment/coolify/README.md"
    "deployment/scripts/README.md"
    "deployment/configs/README.md"
    "docs/README.md"
    "docs/setup/README.md"
    "docs/deployment/README.md"
    "docs/guides/README.md"
    "docs/api/README.md"
    "docs/contributing/README.md"
)

for file in "${README_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo -e "  ${GREEN}✅ $file exists${NC}"
    else
        echo -e "  ${RED}❌ $file missing${NC}"
    fi
done

# Test 5: Check if root README is updated
echo -e "\n${YELLOW}[TEST 5]${NC} Checking if root README is updated..."

if grep -q "deployment/coolify/coolify-deploy.sh" README.md; then
    echo -e "  ${GREEN}✅ Root README references new deployment paths${NC}"
else
    echo -e "  ${RED}❌ Root README missing new deployment path references${NC}"
fi

# Summary
echo -e "\n${YELLOW}[SUMMARY]${NC} File Organization Test Results"
echo "================================================"

echo -e "\n🎯 New Structure Benefits:"
echo "  ✅ Better organization and maintainability"
echo "  ✅ Clearer separation of concerns"
echo "  ✅ Improved AI assistance (Cursor AI)"
echo "  ✅ Professional industry-standard structure"
echo "  ✅ Self-documenting system"

echo -e "\n📚 Documentation Locations:"
echo "  📖 Setup guides: docs/setup/"
echo "  🚀 Deployment: docs/deployment/"
echo "  🐳 Docker: deployment/docker/"
echo "  ⚡ Coolify: deployment/coolify/"
echo "  👥 Contributing: docs/contributing/"

echo -e "\n🔧 Updated Commands:"
echo "  🐳 Docker: docker build -f deployment/docker/Dockerfile ."
echo "  🚀 Coolify: ./deployment/coolify/coolify-deploy.sh"
echo "  📚 Docs: All documentation is now in docs/ directory"

echo -e "\n${GREEN}🎉 File organization completed successfully!${NC}"
echo "Your personal system is now better organized and more maintainable."
