# Cocolip Bypass API 🎬

A FastAPI-based reverse proxy service for **Cococlip.ai** and **PicLumen AI** that provides programmatic access to multiple AI generation capabilities:

- 🎥 **Text-to-Video** - Generate videos from text prompts
- 🖼️➡️🎥 **Image-to-Video** - Animate static images
- 🎤➡️🎥 **Audio-to-Video** - Create talking portrait videos (✅ **Prompt Supported**)
- 📝➡️🖼️ **Text-to-Image** - Generate images from text descriptions

## 🌟 Features

- ✅ **RESTful API** - OpenAI-compatible endpoint structure
- ✅ **Async/Await** - High-performance async operations
- ✅ **Interactive Docs** - Dark-themed Swagger UI at `/docs`
- ✅ **File Upload Support** - Automatic file handling and validation
- ✅ **Polling Mechanism** - Auto-polls until generation completes
- ✅ **CORS Enabled** - Ready for web integration
- ✅ **Docker Support** - Easy deployment with Docker

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/SamErics0012/cocolip-bypass.git
cd cocolip-bypass

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The API will be available at `http://localhost:8000`

### Docker Deployment

```bash
# Build the image
docker build -t cocolip-bypass .

# Run the container
docker run -p 8000:8000 cocolip-bypass
```

### Railway Deployment

This project is configured for Railway.app deployment:

1. Connect your GitHub repository to Railway
2. Railway will automatically detect the `Dockerfile`
3. Deploy and get your public URL

## 📚 API Documentation

### Base URL
- **Local**: `http://localhost:8000`
- **Production**: `https://your-app.railway.app`

### Interactive Documentation
Visit `/docs` for the full Swagger UI interface.

---

## 🎯 Endpoints

### 1. List Available Models

```bash
GET /v1/models
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {"id": "hailuo02standard", "object": "model", "owned_by": "cococlip"},
    {"id": "seedancev1lite", "object": "model", "owned_by": "cococlip"},
    {"id": "hailuo23fast", "object": "model", "owned_by": "cococlip"},
    {"id": "wan25fast", "object": "model", "owned_by": "cococlip"},
    {"id": "Infinitetalk", "object": "model", "owned_by": "cococlip"},
    {"id": "piclumen-realistic-v2", "object": "model", "owned_by": "piclumen"},
    {"id": "midjourney", "object": "model", "owned_by": "piclumen"},
    {"id": "imagine-text-to-video", "object": "model", "owned_by": "imagine.art"}
  ]
}
```

---

### 2. Text-to-Video Generation

```bash
POST /v1/video/generations
```

**Request:**
```json
{
  "model": "hailuo02standard",
  "prompt": "A cat playing piano in a jazz club",
  "duration": 6,
  "aspect_ratio": "16:9",
  "resolution": "720p"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/v1/video/generations" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "hailuo02standard",
    "prompt": "A cat playing piano in a jazz club",
    "duration": 6,
    "aspect_ratio": "16:9",
    "resolution": "720p"
  }'
```

---

### 3. Image-to-Video Generation

```bash
POST /v1/image-to-video/generations
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/v1/image-to-video/generations" \
  -F "image=@/path/to/image.jpg" \
  -F "model=hailuo23fast" \
  -F "prompt=The character smiles and waves" \
  -F "resolution=768p" \
  -F "duration=6"
```

---

### 4. Audio-to-Video Generation (Talking Portrait)

✅ **PROMPT IS FULLY SUPPORTED** - Add motion and animation instructions!

```bash
POST /v1/audio-to-video/generations
```

#### ⭐ cURL Examples with Prompt Support

**Example 1: With Motion Prompt**
```bash
curl -X POST "http://localhost:8000/v1/audio-to-video/generations" \
  -F "image=@portrait.jpg" \
  -F "audio=@voice.mp3" \
  -F "prompt=make video in motion" \
  -F "resolution=720p" \
  -F "audio_duration=5.06"
```

**Example 2: With Animation Instructions**
```bash
curl -X POST "http://localhost:8000/v1/audio-to-video/generations" \
  -F "image=@portrait.jpg" \
  -F "audio=@voice.mp3" \
  -F "prompt=animate with realistic expressions and head movements" \
  -F "resolution=1080p"
```

**Example 3: Without Prompt (Default Behavior)**
```bash
curl -X POST "http://localhost:8000/v1/audio-to-video/generations" \
  -F "image=@portrait.jpg" \
  -F "audio=@voice.mp3" \
  -F "prompt=" \
  -F "resolution=720p"
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | File | ✅ Yes | Portrait image (JPEG, PNG, WebP) |
| `audio` | File | ✅ Yes | Audio file (MP3, WAV) |
| `prompt` | String | ❌ No | **✅ SUPPORTED** - Motion/animation instructions |
| `resolution` | String | ❌ No | Video resolution: `720p` or `1080p` (default: `720p`) |
| `audio_duration` | Float | ❌ No | Audio duration in seconds (auto-detected if omitted) |

#### Prompt Examples

Use the `prompt` field to control motion and animation:

- ✅ `"make video in motion"`
- ✅ `"animate with realistic expressions"`
- ✅ `"natural head movements and blinking"`
- ✅ `"dynamic facial expressions and lip sync"`
- ✅ `"smooth and natural animation"`

#### Response

```json
{
  "url": "https://d2p7pge43lyniu.cloudfront.net/output/video.mp4",
  "status": "COMPLETED",
  "task_id": "be49ce022530438f984ffd602ec454ad",
  "inference_time": 128036
}
```

---

### 5. Imagine.art Text-to-Video Generation

```bash
POST /v1/imagine-text-to-video/generations
```

**Request:**
```json
{
  "prompt": "A majestic eagle soaring through mountain peaks at sunset",
  "aspect_ratio": "16:9",
  "duration": 12,
  "resolution": "1080p",
  "style_id": 60503,
  "is_enhance": true
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/v1/imagine-text-to-video/generations" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A majestic eagle soaring through mountain peaks at sunset",
    "aspect_ratio": "16:9",
    "duration": 12,
    "resolution": "1080p",
    "style_id": 60503,
    "is_enhance": true
  }'
```

**Response:**
```json
{
  "id": "85f8e695-38cc-4023-b15e-49313cadcbfc",
  "status": "COMPLETED",
  "video_url": "https://asset.imagine.art/processed/85f8e695-38cc-4023-b15e-49313cadcbfc",
  "batch_id": "dde09073-c355-4443-aa80-0736d8358621"
}
```

**Important Notes:**
- The API automatically polls for completion (typically 1-3 minutes)
- The endpoint waits until the video is fully generated before returning
- The `video_url` in the response is ready to use immediately
- No manual polling required - works just like other video generation endpoints

**Python Example:**
```python
import requests

url = "http://localhost:8000/v1/imagine-text-to-video/generations"

payload = {
    "prompt": "A cat eating hotdogs in a park",
    "aspect_ratio": "16:9",
    "duration": 12,
    "resolution": "1080p",
    "style_id": 60503,
    "is_enhance": True
}

# Send generation request (API automatically polls for completion)
response = requests.post(url, json=payload)
result = response.json()

print(f"Video ID: {result['id']}")
print(f"Status: {result['status']}")
print(f"Video URL: {result['video_url']}")

# Video is ready to use immediately!
# The API waits for completion before returning
```

---

### 6. Text-to-Image Generation

```bash
POST /v1/text-to-image/generations
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/v1/text-to-image/generations" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "piclumen-realistic-v2",
    "prompt": "a cute cat sitting on a couch",
    "width": 1024,
    "height": 1024,
    "batch_size": 2
  }'
```

---

## 💻 Code Examples

### Python

```python
import requests

# Audio-to-Video with Prompt
url = "http://localhost:8000/v1/audio-to-video/generations"

with open('portrait.jpg', 'rb') as img, open('voice.mp3', 'rb') as aud:
    files = {
        'image': ('portrait.jpg', img, 'image/jpeg'),
        'audio': ('voice.mp3', aud, 'audio/mpeg')
    }
    
    data = {
        'prompt': 'make video in motion',  # ✅ Prompt is supported!
        'resolution': '1080p',
        'audio_duration': 5.06
    }
    
    response = requests.post(url, files=files, data=data)
    result = response.json()
    
    print(f"Video URL: {result['url']}")
    print(f"Status: {result['status']}")
```

### JavaScript/Fetch

```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('audio', audioFile);
formData.append('prompt', 'make video in motion'); // ✅ Prompt supported!
formData.append('resolution', '720p');

const response = await fetch('http://localhost:8000/v1/audio-to-video/generations', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Video URL:', result.url);
```

### PowerShell (Windows)

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/v1/audio-to-video/generations" `
  -Method POST `
  -Form @{
    image = Get-Item -Path "C:\path\to\portrait.jpg"
    audio = Get-Item -Path "C:\path\to\audio.mp3"
    prompt = "make video in motion"
    resolution = "720p"
  }
```

---

## 🎨 Model Capabilities

### Video Generation Models

| Model | Type | Duration | Resolution | Features |
|-------|------|----------|------------|----------|
| `hailuo02standard` | Text-to-Video | 6s | High Quality | Best quality text-to-video |
| `seedancev1lite` | Text-to-Video | 5s, 10s | 720p, 1080p | Customizable aspect ratios |
| `hailuo23fast` | Image-to-Video | 6s, 10s | 768p | Fast image animation |
| `wan25fast` | Image-to-Video | 5s, 10s | 720p, 1080p | High-quality image-to-video |
| `Infinitetalk` | Audio-to-Video | Auto | 720p, 1080p | ✅ **Prompt Supported** - Talking portraits |
| `imagine-text-to-video` | Text-to-Video | 5s, 6s, 12s | 720p, 1080p | Imagine.art Seedance - automatic polling |

### Image Generation Models

| Model | Type | Batch Size | Features |
|-------|------|------------|----------|
| `piclumen-realistic-v2` | Text-to-Image | 1-4 | Realistic image generation, configurable steps/CFG |
| `midjourney` | Text-to-Image | 4 (fixed) | Midjourney-style artistic images |

---

## 🔧 Configuration

### Environment Variables

```bash
PORT=8000  # Server port (default: 8000)
```

### Dependencies

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
httpx==0.26.0
python-multipart==0.0.6
```

---

## 📝 Important Notes

### Audio-to-Video (Infinitetalk)

- ✅ **Prompt parameter IS SUPPORTED** - Use it to control motion and animation
- Upload **image files only** (JPEG, PNG, WebP) - NOT video files
- Audio files should be MP3 or WAV format
- Recommended resolution: 1080p for best quality
- Processing time: 1-3 minutes depending on audio length

### File Requirements

**Images:**
- Formats: JPEG, PNG, WebP
- Recommended: Clear portrait photos with visible faces
- No strict size limits

**Audio:**
- Formats: MP3, WAV
- Recommended: Under 30 seconds for faster processing
- Clear speech/voice for best results

---

## 🚨 Error Handling

Common errors and solutions:

### 400 Bad Request
```json
{
  "detail": "Invalid image file type. Allowed: JPEG, PNG, WebP. Got: video/mp4"
}
```
**Solution:** Ensure you're uploading image files, not videos.

### 500 Internal Server Error
```json
{
  "detail": "Failed to get presigned URL"
}
```
**Solution:** Check authentication tokens in `main.py` - they may have expired.

---

## 🔐 Security Notes

⚠️ **Warning:** This project contains hardcoded authentication credentials that will expire over time.

For production use, consider:
- Moving credentials to environment variables
- Implementing token refresh mechanisms
- Adding API key authentication
- Rate limiting

---

## 📖 Full Documentation

See [API_DOCS.md](./API_DOCS.md) for comprehensive documentation with more examples.

---

## 🛠️ Development

### Run Tests

```bash
# Test text-to-image
python test_api.py

# Test Imagine.art text-to-video
python test_imagine.py

# Test multiple configurations
python test_imagine.py --multi

# Test with shell script
chmod +x test_imagine.sh
./test_imagine.sh

# Test audio-to-video with custom files
chmod +x test_audio_to_video.sh
./test_audio_to_video.sh
```

### Project Structure

```
cocolip-bypass/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── railway.toml        # Railway deployment config
├── API_DOCS.md         # Detailed API documentation
├── README.md           # This file
├── test_api.py         # Test script
└── test_audio_to_video.sh  # Audio-to-video test examples
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is for educational purposes only. Ensure you comply with Cococlip.ai and PicLumen's terms of service.

---

## 🔗 Links

- **GitHub Repository:** https://github.com/SamErics0012/cocolip-bypass
- **Cococlip.ai:** https://cococlip.ai
- **PicLumen:** https://www.piclumen.com

---

## 💡 Tips for Best Results

### Audio-to-Video with Prompt
- ✅ **Use the prompt field** to guide motion: `"make video in motion"`, `"animate with realistic expressions"`
- Use clear portrait images with visible faces
- Audio should be clear speech/voice
- Recommended resolution: 1080p for best quality
- Keep audio under 30 seconds for faster processing

### Image-to-Video
- Use high-quality source images
- Describe motion clearly in prompt
- Longer durations (10s) allow more complex animations

### Text-to-Video
- Be specific in prompts
- Describe scene, subject, and action clearly
- Use descriptive language for better results

### Imagine.art Text-to-Video
- Experiment with different `style_id` values for varied artistic styles
- Enable `is_enhance` for more detailed video generation
- Use descriptive prompts with specific subjects, actions, and settings
- Choose 12s duration for more complex scenes and animations
- 1080p resolution recommended for high-quality output
- The API automatically polls for completion - no manual polling needed
- Generation typically takes 1-3 minutes (the endpoint waits for completion)

### Text-to-Image
- Detailed prompts yield better results
- Use negative prompts to avoid unwanted elements
- Experiment with batch sizes for variety

---

## 📞 Support

For issues or questions:
1. Check the interactive documentation at `/docs`
2. Review [API_DOCS.md](./API_DOCS.md)
3. Open an issue on GitHub
4. Verify file formats (JPEG/PNG for images, MP3/WAV for audio)

---

**Made with ❤️ for AI Video & Image Generation**