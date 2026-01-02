#!/bin/bash

# Test script for Imagine.art Text-to-Video API endpoint
# Usage: ./test_imagine.sh [API_BASE_URL]

# Configuration
API_BASE_URL="${1:-http://localhost:8000}"
IMAGINE_ENDPOINT="$API_BASE_URL/v1/imagine-text-to-video/generations"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "================================================================================"
echo "                Imagine.art Text-to-Video API Test Script"
echo "================================================================================"
echo ""

# Check if jq is available (for JSON parsing)
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️  Warning: 'jq' command not found. Install it for better JSON parsing${NC}"
    echo "   You can install it with: sudo apt-get install jq (Ubuntu/Debian)"
    echo "                          or: brew install jq (macOS)"
    echo ""
fi

# Test 1: Basic text-to-video generation
echo "Test 1: Basic Text-to-Video Generation"
echo "--------------------------------------------------------------------------------"

PAYLOAD='{
  "prompt": "A majestic eagle soaring through mountain peaks at sunset, cinematic camera movement",
  "aspect_ratio": "16:9",
  "duration": 12,
  "resolution": "1080p",
  "style_id": 60503,
  "is_enhance": true
}'

echo "📝 Request Payload:"
echo "$PAYLOAD" | jq . 2>/dev/null || echo "$PAYLOAD"
echo ""

echo "🚀 Sending request to: $IMAGINE_ENDPOINT"
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$IMAGINE_ENDPOINT" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

# Extract HTTP status code and body
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✅ Request successful! (HTTP $HTTP_CODE)${NC}"
    echo "--------------------------------------------------------------------------------"

    # Parse response
    if command -v jq &> /dev/null; then
        echo "$BODY" | jq .
        VIDEO_ID=$(echo "$BODY" | jq -r '.id')
        VIDEO_URL=$(echo "$BODY" | jq -r '.video_url')
        STATUS=$(echo "$BODY" | jq -r '.status')
        BATCH_ID=$(echo "$BODY" | jq -r '.batch_id')
    else
        echo "$BODY"
        VIDEO_URL=$(echo "$BODY" | grep -o '"video_url":"[^"]*"' | cut -d'"' -f4)
        VIDEO_ID=$(echo "$BODY" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    fi

    echo ""
    echo "================================================================================
    echo "🎬 Video Generation Details:"
    echo "================================================================================"
    echo -e "  ${BLUE}Video ID:${NC} $VIDEO_ID"
    echo -e "  ${BLUE}Video URL:${NC} $VIDEO_URL"
    echo "================================================================================"
    echo ""

    # Ask if user wants to poll for completion
    echo "⏳ The video is now being generated. This typically takes 1-3 minutes."
    echo ""
    read -p "Do you want to poll for video completion? (y/n): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "📡 Polling for video completion..."
        echo "   Checking: $VIDEO_URL"
        echo ""

        MAX_ATTEMPTS=30
        ATTEMPT=0

        while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
            ATTEMPT=$((ATTEMPT + 1))
            echo -n "   Attempt $ATTEMPT/$MAX_ATTEMPTS... "

            # Check if video is accessible
            HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$VIDEO_URL")

            if [ "$HTTP_STATUS" -eq 200 ]; then
                echo -e "${GREEN}✅ Video is ready!${NC}"
                echo ""
                echo "================================================================================"
                echo "🎉 Video Generation Complete!"
                echo "================================================================================"
                echo ""
                echo -e "📹 ${GREEN}Video URL:${NC} $VIDEO_URL"
                echo -e "📋 ${BLUE}Video ID:${NC} $VIDEO_ID"
                echo ""
                echo "💡 You can now access the video at the URL above"
                echo "================================================================================"
                exit 0
            else
                echo -e "${YELLOW}⏳ Not ready yet (HTTP $HTTP_STATUS)${NC}"
            fi

            # Wait before next attempt
            if [ $ATTEMPT -lt $MAX_ATTEMPTS ]; then
                sleep 10
            fi
        done

        echo ""
        echo -e "${YELLOW}⚠️  Timeout: Video generation is taking longer than expected${NC}"
        echo "   The video might still be processing. Check the URL manually:"
        echo "   $VIDEO_URL"
    else
        echo ""
        echo "💡 You can manually check the video status by accessing:"
        echo "   $VIDEO_URL"
    fi

else
    echo -e "${RED}❌ Request failed! (HTTP $HTTP_CODE)${NC}"
    echo "--------------------------------------------------------------------------------"
    echo "Response:"
    echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
    exit 1
fi

echo ""
echo "================================================================================"
echo "Testing Complete!"
echo "================================================================================"
