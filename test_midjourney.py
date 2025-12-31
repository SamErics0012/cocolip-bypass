import requests
import json
import sys

url = "http://localhost:8000/v1/text-to-image/generations"

payload = {
    "model": "midjourney",
    "prompt": "a cute cat sitting on a windowsill",
    "width": 1024,
    "height": 1024
}

print("Testing Midjourney model...")
print(f"Request: {json.dumps(payload, indent=2)}")
print("\nSending request...")

try:
    response = requests.post(url, json=payload, timeout=180)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\nSUCCESS!")
        print(f"\nResponse:")
        print(json.dumps(result, indent=2))
        print(f"\nGenerated {len(result['data'])} images:")
        for idx, img in enumerate(result['data'], 1):
            print(f"  Image {idx}: {img['url']}")
    else:
        print(f"\nERROR: {response.status_code}")
        print("Response text:")
        print(response.text)
        
except Exception as e:
    print(f"\nException occurred: {str(e)}")
    import traceback
    traceback.print_exc()
