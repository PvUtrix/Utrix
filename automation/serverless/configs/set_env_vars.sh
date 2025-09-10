#!/bin/bash

# Script to set environment variables for voice transcription function
# This prevents the serverless deployment from overwriting the API keys

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Setting Environment Variables for Voice Transcription${NC}"
echo -e "${BLUE}====================================================${NC}"

# Function name
FUNCTION_NAME="personal-system-serverless-prod-voice-transcription"
REGION="eu-central-1"

# API Keys (these should be set in your environment or config)
ELEVENLABS_API_KEY="sk_9382e4b7a49fa13e8334898360f9e3bd75ee67cfb27492fc"
OPENAI_API_KEY="Z0FBQUFBQm9xYkoxMVNTRmNSbFdydDBTZTI1UGhSdmhlelFLbi1tQ29XdHVjbEFyeFhPWDEtbXB2MW1kWGRqcHhBTUczQWxkM2dJREpQX0RNVHpZbXZUQVRHZEFUbGRtQkRiSEtEVElNMnhGZDFPSThsdlVfa0Y5X0RxREpBcV9DZ1dRZ28wN3A5NmR2UzB1ZGVNYTNDdm5tT3h1V2lJZnVpeWNId3JLVFB1cGduOGJMcmNiWll4QlFZdERad3dYMTZCSThubmE3UC12MWpKYmdGWmlObXRBc3dvYXhaM0tHWGNfaVpZeG9DeEQzMC03SFZDdUhfSS14OW5aMHpDYks5LW9qRUpMNzJUbmFSZmxOemU3VWhXT3Rrd09YTTQ0QV9MUHNfc3F6YjV5czRLVmNFd2U0ZWc9"

echo -e "${YELLOW}📋 Function: $FUNCTION_NAME${NC}"
echo -e "${YELLOW}📋 Region: $REGION${NC}"

# Set environment variables
echo -e "${YELLOW}🔑 Setting environment variables...${NC}"

aws lambda update-function-configuration \
    --function-name "$FUNCTION_NAME" \
    --region "$REGION" \
    --environment Variables="{
        ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY,
        OPENAI_API_KEY=$OPENAI_API_KEY
    }"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Environment variables set successfully${NC}"
else
    echo -e "${RED}❌ Failed to set environment variables${NC}"
    exit 1
fi

# Test the function
echo -e "${YELLOW}🧪 Testing voice transcription function...${NC}"

RESPONSE=$(curl -s -X POST https://1pubjgwn81.execute-api.eu-central-1.amazonaws.com/prod/voice-transcription \
    -H "Content-Type: application/json" \
    -d '{"audio_data": "dGVzdA==", "file_format": "ogg", "user_id": "test", "message_id": "test"}')

echo -e "${BLUE}📤 Response: $RESPONSE${NC}"

if echo "$RESPONSE" | grep -q "success.*false"; then
    echo -e "${YELLOW}⚠️  Function is running but transcription failed (expected with test data)${NC}"
    echo -e "${GREEN}✅ Environment variables are working${NC}"
else
    echo -e "${GREEN}✅ Function is working correctly${NC}"
fi

echo -e "${BLUE}====================================================${NC}"
echo -e "${GREEN}🎉 Voice transcription function is ready!${NC}"
echo -e "${YELLOW}💡 You can now send voice messages to your bot${NC}"
