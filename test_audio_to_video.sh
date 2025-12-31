#!/bin/bash

# Audio-to-Video Generation Test with Prompt Support
# This script demonstrates how to use the audio-to-video endpoint with prompt

# Base URL (change to your deployment URL)
BASE_URL="http://localhost:8000"
# BASE_URL="https://your-app.railway.app"

# Test 1: Basic audio-to-video with prompt
echo "=== Test 1: Audio-to-Video with Motion Prompt ==="
curl -X POST "${BASE_URL}/v1/audio-to-video/generations" \
  -F "image=@/path/to/portrait.jpg" \
  -F "audio=@/path/to/audio.mp3" \
  -F "prompt=make video in motion" \
  -F "resolution=720p" \
  -F "audio_duration=5.06"

echo -e "\n\n"

# Test 2: Audio-to-video with different prompt
echo "=== Test 2: Audio-to-Video with Custom Animation ==="
curl -X POST "${BASE_URL}/v1/audio-to-video/generations" \
  -F "image=@/path/to/portrait.jpg" \
  -F "audio=@/path/to/audio.mp3" \
  -F "prompt=animate with realistic expressions and head movements" \
  -F "resolution=1080p"

echo -e "\n\n"

# Test 3: Audio-to-video with empty prompt (default behavior)
echo "=== Test 3: Audio-to-Video with No Prompt ==="
curl -X POST "${BASE_URL}/v1/audio-to-video/generations" \
  -F "image=@/path/to/portrait.jpg" \
  -F "audio=@/path/to/audio.mp3" \
  -F "prompt=" \
  -F "resolution=720p"

echo -e "\n\n"

# Test 4: Windows PowerShell equivalent
echo "=== PowerShell Command (for Windows users) ==="
echo 'Invoke-WebRequest -Uri "http://localhost:8000/v1/audio-to-video/generations" `
  -Method POST `
  -Form @{
    image = Get-Item -Path "C:\path\to\portrait.jpg"
    audio = Get-Item -Path "C:\path\to\audio.mp3"
    prompt = "make video in motion"
    resolution = "720p"
    audio_duration = "5.06"
  }'

echo -e "\n\n"

# Test 5: Python requests example
echo "=== Python Example ==="
cat << 'EOF'
import requests

url = "http://localhost:8000/v1/audio-to-video/generations"

with open('portrait.jpg', 'rb') as img, open('audio.mp3', 'rb') as aud:
    files = {
        'image': ('portrait.jpg', img, 'image/jpeg'),
        'audio': ('audio.mp3', aud, 'audio/mpeg')
    }

    data = {
        'prompt': 'make video in motion',
        'resolution': '720p',
        'audio_duration': 5.06
    }

    response = requests.post(url, files=files, data=data)
    result = response.json()

    print(f"Video URL: {result['url']}")
    print(f"Status: {result['status']}")
    print(f"Task ID: {result['task_id']}")
    print(f"Inference Time: {result['inference_time']}ms")
EOF

echo -e "\n\n"

# Test 6: JavaScript/Fetch example
echo "=== JavaScript/Fetch Example ==="
cat << 'EOF'
const formData = new FormData();
formData.append('image', imageFile); // File from <input type="file">
formData.append('audio', audioFile); // File from <input type="file">
formData.append('prompt', 'make video in motion');
formData.append('resolution', '720p');
formData.append('audio_duration', '5.06');

fetch('http://localhost:8000/v1/audio-to-video/generations', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(result => {
  console.log('Video URL:', result.url);
  console.log('Status:', result.status);
  console.log('Task ID:', result.task_id);
  console.log('Inference Time:', result.inference_time, 'ms');
})
.catch(error => console.error('Error:', error));
EOF

echo -e "\n\n"
echo "=== Notes ==="
echo "✅ Prompt parameter is SUPPORTED"
echo "✅ Use 'prompt' field to add motion or animation instructions"
echo "✅ Resolution supports: 720p, 1080p"
echo "✅ audio_duration is optional (auto-detected if omitted)"
echo ""
echo "Example prompts:"
echo "  - 'make video in motion'"
echo "  - 'animate with realistic expressions'"
echo "  - 'natural head movements and blinking'"
echo "  - 'dynamic facial expressions'"
