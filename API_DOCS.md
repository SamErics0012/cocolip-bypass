# Cococlip AI Video Generation API - Documentation

## Base URL
```
https://your-app.railway.app
```

## Interactive Documentation
Visit `/docs` for Swagger UI interface to test all endpoints interactively.

---

## Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/models` | GET | List all available AI models |
| `/v1/text-to-video/generations` | POST | Generate video from text prompt |
| `/v1/image-to-video/generations` | POST | Generate video from image + prompt |
| `/v1/audio-to-video/generations` | POST | Generate talking portrait from image + audio |
| `/v1/imagine-text-to-video/generations` | POST | Generate video from text using Imagine.art |

---

## 1. List Available Models

### Request
```bash
curl -X GET "https://your-app.railway.app/v1/models"
```

### Response
```json
{
  "object": "list",
  "data": [
    {"id": "hailuo02standard", "object": "model", "created": 1704067200, "owned_by": "cococlip"},
    {"id": "seedancev1lite", "object": "model", "created": 1704067200, "owned_by": "cococlip"},
    {"id": "hailuo23fast", "object": "model", "created": 1704067200, "owned_by": "cococlip"},
    {"id": "wan25fast", "object": "model", "created": 1704067200, "owned_by": "cococlip"},
    {"id": "Infinitetalk", "object": "model", "created": 1704067200, "owned_by": "cococlip"},
    {"id": "imagine-text-to-video", "object": "model", "created": 1704067200, "owned_by": "imagine.art"}
  ]
}
```

---

## 2. Text-to-Video Generation

### Request (JSON)
```bash
curl -X POST "https://your-app.railway.app/v1/text-to-video/generations" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "hailuo02standard",
    "prompt": "A cat playing piano in a jazz club"
  }'
```

### Response
```json
{
  "url": "https://d1q70pf5vjeyhc.cloudfront.net/predictions/abc123.mp4",
  "status": "COMPLETED",
  "task_id": "abc123"
}
```

---

## 3. Image-to-Video Generation

### Request (Multipart Form Data)
```bash
curl -X POST "https://your-app.railway.app/v1/image-to-video/generations" \
  -F "image=@/path/to/image.jpg" \
  -F "model=hailuo23fast" \
  -F "prompt=The character smiles and waves" \
  -F "resolution=768p" \
  -F "duration=6"
```

### JavaScript/Fetch Example
```javascript
const formData = new FormData();
formData.append('image', imageFile); // File from input element
formData.append('model', 'hailuo23fast');
formData.append('prompt', 'The character smiles and waves');
formData.append('resolution', '768p');
formData.append('duration', '6');

const response = await fetch('https://your-app.railway.app/v1/image-to-video/generations', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Video URL:', result.url);
```

### Response
```json
{
  "url": "https://d1q70pf5vjeyhc.cloudfront.net/predictions/xyz789.mp4",
  "status": "completed",
  "task_id": "xyz789"
}
```

---

## 4. Audio-to-Video Generation (Talking Portrait)

**⚠️ IMPORTANT**: The `image` parameter must be an **image file** (JPEG, PNG, WebP), NOT a video file. If you upload a video file (`.mp4`), you will get a 400 error from the backend.

### cURL Example (With Prompt Support)
```bash
# Example 1: With motion prompt
curl -X POST "https://your-app.railway.app/v1/audio-to-video/generations" \
  -F "image=@portrait.jpg" \
  -F "audio=@voice.mp3" \
  -F "prompt=make video in motion" \
  -F "resolution=1080p" \
  -F "audio_duration=5.06"

# Example 2: With animation instructions
curl -X POST "https://your-app.railway.app/v1/audio-to-video/generations" \
  -F "image=@portrait.jpg" \
  -F "audio=@voice.mp3" \
  -F "prompt=animate with realistic expressions and head movements" \
  -F "resolution=720p"

# Example 3: Without prompt (empty)
curl -X POST "https://your-app.railway.app/v1/audio-to-video/generations" \
  -F "image=@portrait.jpg" \
  -F "audio=@voice.mp3" \
  -F "prompt=" \
  -F "resolution=1080p"
```

**Notes**: 
- ✅ `prompt` field is **SUPPORTED** - use it to add motion or animation instructions
- `audio_duration` is optional. Leave it empty or omit it - the API auto-detects audio length.
- Example prompts: "make video in motion", "animate with realistic expressions", "natural head movements and blinking"

### JavaScript/Fetch Example (Website Integration)
```javascript
async function generateTalkingPortrait(imageFile, audioFile) {
  // Validate file types before uploading
  if (!imageFile.type.startsWith('image/')) {
    throw new Error('Please upload an image file (JPEG, PNG, WebP), not a video');
  }
  if (!audioFile.type.startsWith('audio/')) {
    throw new Error('Please upload an audio file (MP3, WAV)');
  }
  
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('audio', audioFile);
  formData.append('prompt', 'make video in motion'); // ✅ SUPPORTED - add motion/animation instructions
  formData.append('resolution', '1080p'); // or '720p'
  // audio_duration is optional - API auto-detects from audio file
  
  try {
    const response = await fetch('https://your-app.railway.app/v1/audio-to-video/generations', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error generating video:', error);
    throw error;
  }
}

// Usage in your website
document.getElementById('generateBtn').addEventListener('click', async () => {
  const imageInput = document.getElementById('imageUpload');
  const audioInput = document.getElementById('audioUpload');
  
  const imageFile = imageInput.files[0];
  const audioFile = audioInput.files[0];
  
  if (!imageFile || !audioFile) {
    alert('Please select both image and audio files');
    return;
  }
  
  const result = await generateTalkingPortrait(imageFile, audioFile);
  
  // Display the generated video
  const videoPlayer = document.getElementById('resultVideo');
  videoPlayer.src = result.url;
  videoPlayer.play();
  
  console.log('Task ID:', result.task_id);
  console.log('Inference Time:', result.inference_time, 'ms');
});
```

### Python Example
```python
import requests

url = "https://your-app.railway.app/v1/audio-to-video/generations"

with open('portrait.jpg', 'rb') as img, open('voice.mp3', 'rb') as aud:
    files = {
        'image': ('portrait.jpg', img, 'image/jpeg'),
        'audio': ('voice.mp3', aud, 'audio/mpeg')
    }
    
    data = {
        'prompt': 'make video in motion',  # ✅ SUPPORTED - add motion instructions
        'resolution': '1080p'
        # audio_duration is optional - omit to auto-detect
    }
    
    response = requests.post(url, files=files, data=data)
    result = response.json()
    
    print(f"Video URL: {result['url']}")
    print(f"Status: {result['status']}")
    print(f"Inference Time: {result['inference_time']}ms")
```

### Response
```json
{
  "url": "https://d2p7pge43lyniu.cloudfront.net/output/talking-portrait.mp4",
  "status": "COMPLETED",
  "task_id": "be49ce022530438f984ffd602ec454ad",
  "inference_time": 128036
}
```

---

## 5. Imagine.art Text-to-Video Generation

### Request (JSON)
```bash
curl -X POST "https://your-app.railway.app/v1/imagine-text-to-video/generations" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cat eating hotdogs in a park",
    "aspect_ratio": "16:9",
    "duration": 12,
    "resolution": "1080p",
    "style_id": 60503,
    "is_enhance": true
  }'
```

### JavaScript/Fetch Example
```javascript
const response = await fetch('https://your-app.railway.app/v1/imagine-text-to-video/generations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    prompt: 'A cat eating hotdogs in a park',
    aspect_ratio: '16:9',
    duration: 12,
    resolution: '1080p',
    style_id: 60503,
    is_enhance: true
  })
});

const result = await response.json();
console.log('Video ID:', result.id);
console.log('Video URL:', result.video_url);
console.log('Status:', result.status);

// The API automatically polls for completion!
// The video_url in the response is ready to use
console.log('Video is ready at:', result.video_url);
```

### Response
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
- No manual polling required - just like other video generation endpoints

---

## Complete HTML Example for Audio-to-Video

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Talking Portrait Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .upload-section {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="file"], select {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            background: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #0056b3;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        #loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        #result {
            display: none;
            margin-top: 20px;
        }
        video {
            width: 100%;
            border-radius: 5px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #007bff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Talking Portrait Generator</h1>
        <p>Upload a portrait image and audio file to create a talking avatar</p>
        
        <div class="upload-section">
            <label for="imageUpload">Portrait Image (JPG, PNG)</label>
            <input type="file" id="imageUpload" accept="image/*" required>
            
            <label for="audioUpload">Audio File (MP3, WAV)</label>
            <input type="file" id="audioUpload" accept="audio/*" required>
            
            <label for="resolution">Video Resolution</label>
            <select id="resolution">
                <option value="720p">720p (HD)</option>
                <option value="1080p" selected>1080p (Full HD)</option>
            </select>
            
            <button id="generateBtn">Generate Talking Portrait</button>
        </div>
        
        <div id="loading">
            <div class="spinner"></div>
            <p>Generating your talking portrait... This may take 1-3 minutes.</p>
        </div>
        
        <div id="result">
            <h2>Your Talking Portrait</h2>
            <video id="resultVideo" controls></video>
            <p><a id="downloadLink" download="talking-portrait.mp4">Download Video</a></p>
        </div>
    </div>

    <script>
        const API_URL = 'https://your-app.railway.app/v1/audio-to-video/generations';
        
        document.getElementById('generateBtn').addEventListener('click', async () => {
            const imageInput = document.getElementById('imageUpload');
            const audioInput = document.getElementById('audioUpload');
            const resolution = document.getElementById('resolution').value;
            
            const imageFile = imageInput.files[0];
            const audioFile = audioInput.files[0];
            
            if (!imageFile || !audioFile) {
                alert('Please select both image and audio files');
                return;
            }
            
            // Validate file types
            if (!imageFile.type.startsWith('image/')) {
                alert('Please upload an IMAGE file (JPEG, PNG, WebP), not a video');
                return;
            }
            if (!audioFile.type.startsWith('audio/')) {
                alert('Please upload an AUDIO file (MP3, WAV)');
                return;
            }
            
            // Show loading
            document.getElementById('generateBtn').disabled = true;
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            try {
                const formData = new FormData();
                formData.append('image', imageFile);
                formData.append('audio', audioFile);
                formData.append('prompt', '');
                formData.append('resolution', resolution);
                
                const response = await fetch(API_URL, {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Generation failed');
                }
                
                const result = await response.json();
                
                // Display result
                document.getElementById('loading').style.display = 'none';
                document.getElementById('result').style.display = 'block';
                document.getElementById('resultVideo').src = result.url;
                document.getElementById('downloadLink').href = result.url;
                
                console.log('Generation completed:', result);
                
            } catch (error) {
                console.error('Error:', error);
                alert('Error generating video: ' + error.message);
                document.getElementById('loading').style.display = 'none';
            } finally {
                document.getElementById('generateBtn').disabled = false;
            }
        });
    </script>
</body>
</html>
```

---

## Model Parameters

### Text-to-Video Models

#### hailuo02standard
- **Duration**: 6 seconds (fixed)
- **Resolution**: High quality
- **Use case**: Best quality text-to-video

#### seedancev1lite
- **Duration**: 5s or 10s
- **Resolution**: 720p, 1080p
- **Aspect Ratio**: 9:16, 16:9, 1:1
- **Use case**: Lightweight, customizable

### Image-to-Video Models

#### hailuo23fast
- **Resolution**: 768p (fixed)
- **Duration**: 6s or 10s
- **Use case**: Fast image animation

#### wan25fast
- **Resolution**: 720p or 1080p
- **Duration**: 5s or 10s
- **Use case**: High-quality image-to-video

### Audio-to-Video Model

#### Infinitetalk
- **Resolution**: 720p or 1080p
- **Duration**: Matches audio length
- **Use case**: Talking portraits, lip-sync videos

### Imagine.art Text-to-Video Model

#### imagine-text-to-video
- **Resolution**: 720p or 1080p
- **Duration**: 5s, 6s, or 12s
- **Aspect Ratio**: 16:9, 9:16, 4:3, 1:1
- **Use case**: High-quality text-to-video generation with style control
- **Special Features**: 
  - Style customization via style_id
  - Prompt enhancement support
  - Seedance T2V model backend
  - Automatic polling (no manual polling needed)

---
</text>

<old_text line=493>
### Audio-to-Video
- Use clear portrait images with visible face
- Audio should be clear speech/voice
- **✅ Prompt is supported**: Add motion instructions like "make video in motion", "animate with realistic expressions"
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
- Experiment with different style_ids for varied artistic styles
- Enable prompt enhancement for more detailed video generation
- Use descriptive prompts with specific subjects, actions, and settings
- Choose 12s duration for more complex scenes and animations
- 1080p resolution recommended for high-quality output
- The API automatically polls for completion - no manual polling needed
- Generation typically takes 1-3 minutes (the endpoint waits for completion)

## Error Handling

All endpoints return standard HTTP status codes:

- **200**: Success
- **400**: Bad request (invalid parameters, wrong file type)
- **500**: Server error (generation failed)

### Common Errors

#### Invalid File Type
```json
{
  "detail": "Invalid image file type. Allowed: JPEG, PNG, WebP. Got: video/mp4"
}
```

**Solution**: Ensure you're uploading the correct file type:
- **Image files**: `.jpg`, `.jpeg`, `.png`, `.webp` only
- **Audio files**: `.mp3`, `.wav` only
- ❌ **NOT videos** (`.mp4`, `.mov`, etc.)

#### CORS Error (Website Integration)
If you see `Failed to fetch` or CORS errors in browser console, the API now has CORS enabled. Make sure you're using the latest deployment.

#### Generation Failed
```json
{
  "detail": "Polling failed: ..."
}
```

**Common causes**:
- Uploaded wrong file type (e.g., video instead of image)
- File is corrupted or too large
- Invalid parameters for the model

---

## Rate Limits

The API polls the Cococlip backend every 10 seconds. Large requests may take 1-3 minutes to complete due to AI processing time.

---

## Tips for Best Results

### Audio-to-Video
- Use clear portrait images with visible face
- Audio should be clear speech/voice
- **✅ Prompt is supported**: Add motion instructions like "make video in motion", "animate with realistic expressions"
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

---

## Support

For issues or questions:
- Check `/docs` for interactive testing
- Verify file formats (JPEG/PNG for images, MP3/WAV for audio)
- Ensure files are under 50MB
