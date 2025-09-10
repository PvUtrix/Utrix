#!/bin/bash

# Voice Transcription Serverless Function Deployment Script

set -e

echo "🚀 Deploying Voice Transcription Serverless Function..."

# Check if we're in the right directory
if [ ! -f "voice_transcription.py" ]; then
    echo "❌ Error: voice_transcription.py not found. Please run this script from the voice function directory."
    exit 1
fi

# Function to deploy to AWS Lambda
deploy_lambda() {
    echo "📦 Preparing Lambda deployment package..."
    
    # Create deployment directory
    mkdir -p lambda_deploy
    cd lambda_deploy
    
    # Copy function code
    cp ../voice_transcription.py .
    cp ../requirements.txt .
    
    # Install dependencies
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt -t .
    
    # Create deployment package
    echo "📦 Creating deployment package..."
    zip -r voice-transcription.zip .
    
    echo "✅ Lambda deployment package created: voice-transcription.zip"
    echo "📋 Next steps:"
    echo "1. Upload voice-transcription.zip to AWS Lambda"
    echo "2. Set environment variable: OPENAI_API_KEY"
    echo "3. Set timeout to 30 seconds"
    echo "4. Set memory to 512MB"
    echo "5. Create API Gateway endpoint"
    
    cd ..
}

# Function to deploy to Vercel
deploy_vercel() {
    echo "📦 Preparing Vercel deployment..."
    
    # Create vercel.json if it doesn't exist
    if [ ! -f "vercel.json" ]; then
        cat > vercel.json << EOF
{
  "functions": {
    "voice_transcription.py": {
      "runtime": "python3.9"
    }
  },
  "env": {
    "OPENAI_API_KEY": "@openai_api_key"
  }
}
EOF
    fi
    
    echo "✅ Vercel configuration created"
    echo "📋 Next steps:"
    echo "1. Run: vercel --prod"
    echo "2. Set environment variable: OPENAI_API_KEY"
    echo "3. Update bot config with the deployment URL"
}

# Main deployment logic
echo "Choose deployment target:"
echo "1) AWS Lambda"
echo "2) Vercel"
echo "3) Both"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        deploy_lambda
        ;;
    2)
        deploy_vercel
        ;;
    3)
        deploy_lambda
        echo ""
        deploy_vercel
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment preparation complete!"
echo "📝 Don't forget to:"
echo "   - Set OPENAI_API_KEY environment variable"
echo "   - Update your bot's config.yaml with the function URL"
echo "   - Test the function with a sample audio file"

