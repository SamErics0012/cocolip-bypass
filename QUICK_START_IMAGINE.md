# 🚀 Quick Start: Imagine.art Text-to-Video

## ⚡ 30-Second Setup

```bash
# 1. Start the server
python main.py

# 2. Test the endpoint
curl -X POST "http://localhost:8000/v1/imagine-text-to-video/generations" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A cat eating hotdogs in a park", "duration": 12, "resolution": "1080p"}'

# 3. Run automated test
python test_imagine.py
```

---

## 📝 Basic Request

```json
{
  "prompt": "A majestic eagle soaring through mountains at sunset",
  "aspect_ratio": "1:1",
  "duration": 5,
  "resolution": "720p",
  "style_id": 60503,
  "is_enhance": true
}
```

**Response:**
```json
{
  "id": "85f8e695-...",
  "status": "COMPLETED",
  "video_url": "https://asset.imagine.art/processed/85f8e695-...",
  "batch_id": "dde09073-..."
}

**Seedance Pro Parameters:**
- Durations: 3s, 4s, 5s, 6s, 7s, 8s, 9s, 10s, 11s, 12s
- Resolutions: 480p, 720p, 1080p
- Aspect Ratios: 3:4 (portrait), 1:1 (square), 4:3 (standard)
}
```

---

## 🐍 Python (Copy & Paste)

```python
import requests
import time

def generate_video(prompt):
    # Send request - API automatically polls for completion!
    response = requests.post(
        "http://localhost:8000/v1/imagine-text-to-video/generations",
        json={
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "duration": 5,
            "resolution": "720p",
            "style_id": 60503,
            "is_enhance": True
        }
    )
    result = response.json()
    
    # Video is ready immediately - no manual polling needed!
    video_url = result['video_url']
    status = result['status']
    
    print(f"✅ Status: {status}")
    print(f"📹 Video URL: {video_url}")
    return video_url

# Use it
video = generate_video("A cat eating hotdogs in a park")
```

---

## 🌐 JavaScript (Copy & Paste)

```javascript
async function generateVideo(prompt) {
  // Send request - API automatically polls for completion!
  const response = await fetch('http://localhost:8000/v1/imagine-text-to-video/generations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt,
      aspect_ratio: "1:1",
      duration: 5,
      resolution: "720p",
      style_id: 60503,
      is_enhance: true
    })
  });
  
  const result = await response.json();
  
  // Video is ready immediately - no manual polling needed!
  const videoUrl = result.video_url;
  const status = result.status;
  
  console.log(`✅ Status: ${status}`);
  console.log(`📹 Video URL: ${videoUrl}`);
  return videoUrl;
}

// Use it
const video = await generateVideo("A cat eating hotdogs in a park");
```

---

## ⚙️ Parameters Cheat Sheet

| Parameter | Options | Default | Notes |
|-----------|---------|---------|-------|
| `prompt` | string (1-2000 chars) | **required** | Be descriptive! |
| `aspect_ratio` | `3:4`, `1:1`, `4:3` | `1:1` | 3:4 portrait, 1:1 square, 4:3 standard |
| `duration` | `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12` | `5` | Longer = more complex scenes |
| `resolution` | `480p`, `720p`, `1080p` | `720p` | 480p fast, 720p balanced, 1080p quality |
| `style_id` | integer | `60503` | Experimental: try different values |
| `is_enhance` | boolean | `true` | Keep enabled for better results |

---

## ⏱️ Generation Time

**Seedance Pro:**
- **3-5s @ 480p**: ~60-90 seconds
- **5-7s @ 720p**: ~90-120 seconds
- **8-12s @ 1080p**: ~2-3 minutes

**Note: The API automatically polls for completion - you don't need to do anything!**

---

## 🎯 Common Use Cases

### Standard Video (YouTube/Landscape)
```json
{"aspect_ratio": "4:3", "duration": 10, "resolution": "1080p"}
```

### Portrait Video (TikTok/Reels)
```json
{"aspect_ratio": "3:4", "duration": 7, "resolution": "720p"}
```

### Square Post (Instagram)
```json
{"aspect_ratio": "1:1", "duration": 5, "resolution": "720p"}
```

---

## 💡 Prompt Tips

### Good Prompts ✅
- "A majestic eagle soaring through snow-capped mountains at golden hour, cinematic"
- "Time-lapse of a blooming flower in a lush garden, macro photography"
- "Underwater scene with colorful fish swimming through coral reef, 4K quality"

### Bad Prompts ❌
- "bird" (too vague)
- "video" (no subject)
- "something cool" (not descriptive)

**Keywords that help:**
- Cinematic, 4K, professional
- Slow motion, time-lapse, dynamic
- At sunset, in nature, underwater
- Camera panning, zooming, tracking

---

## 🧪 Quick Test

```bash
# Test with provided script
python test_imagine.py

# Or shell script
./test_imagine.sh

# Or manual cURL
curl -X POST "http://localhost:8000/v1/imagine-text-to-video/generations" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test", "duration": 6, "resolution": "720p"}'
```

---

## 🐛 Troubleshooting

### Request takes long time
**Fix**: Normal! The API automatically polls until video is ready (1-3 minutes depending on duration and resolution).

### "Could not extract video ID"
**Fix**: Check response format. May be array or object:
```python
if isinstance(data, list): result = data[0]
else: result = data
```

### 401 Unauthorized
**Fix**: Bearer token expired. Update `IMAGINE_HEADERS` in `main.py`

### Timeout after 5 minutes
**Fix**: Rare case - video might still be processing. Status will be "PROCESSING" in response.

---

## 📚 More Info

- **Full API Docs**: `API_DOCS.md`
- **Implementation Details**: `IMAGINE_ART_IMPLEMENTATION.md`
- **All Endpoints**: http://localhost:8000/docs
- **Test Scripts**: `test_imagine.py`, `test_imagine.sh`

---

## 🎉 That's It!

You're ready to generate videos with Imagine.art API.

**Remember**: The API automatically polls for completion - just make the request and wait for the response!