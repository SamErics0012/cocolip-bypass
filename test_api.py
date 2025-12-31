import requests
import json

url = "http://localhost:8000/v1/text-to-image/generations"
payload = {
    "model": "midjourney",
    "prompt": "cat sitting on a couch",
    "width": 1024,
    "height": 1024
}

print("Sending request...")
response = requests.post(url, json=payload, timeout=300)
print(f"Status Code: {response.status_code}")
print(f"Response:\n{json.dumps(response.json(), indent=2)}")
