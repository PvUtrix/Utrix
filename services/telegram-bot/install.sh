#!/bin/bash

# Personal System Telegram Bot Installation Script

echo "🤖 Installing Personal System Telegram Bot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements-clean.txt

# Check if config file exists
if [ ! -f "config/config.yaml" ]; then
    echo "⚙️ Creating configuration file..."
    cp config/config.yaml.sample config/config.yaml
    echo "📝 Please edit config/config.yaml with your bot token and API keys"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/storage
mkdir -p data/cache
mkdir -p data/backups
mkdir -p data/keys
mkdir -p logs

echo "✅ Installation complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Edit config/config.yaml with your bot token and API keys"
echo "2. Run: python main.py"
echo ""
echo "📖 For detailed setup instructions, see VOICE_SETUP_GUIDE.md"
