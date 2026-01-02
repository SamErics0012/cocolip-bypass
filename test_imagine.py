#!/usr/bin/env python3
"""
Test script for Imagine.art Text-to-Video API endpoint
"""

import sys
import time

import requests

# Configuration
API_BASE_URL = "http://localhost:8000"  # Change to your deployed URL
IMAGINE_ENDPOINT = f"{API_BASE_URL}/v1/imagine-text-to-video/generations"


def test_imagine_text_to_video():
    """
    Test the Imagine.art text-to-video generation endpoint
    """
    print("=" * 80)
    print("Testing Imagine.art Text-to-Video Generation")
    print("=" * 80)

    # Test payload
    payload = {
        "prompt": "A majestic eagle soaring through mountain peaks at sunset, cinematic camera movement",
        "aspect_ratio": "16:9",
        "duration": 12,
        "resolution": "1080p",
        "style_id": 60503,
        "is_enhance": True,
    }

    print("\n📝 Request Payload:")
    print("-" * 80)
    for key, value in payload.items():
        print(f"  {key}: {value}")
    print("-" * 80)

    try:
        # Step 1: Send generation request
        print("\n🚀 Sending request to Imagine.art API...")
        response = requests.post(IMAGINE_ENDPOINT, json=payload, timeout=60)

        if response.status_code != 200:
            print(f"\n❌ Error: Request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return False

        result = response.json()

        print("\n✅ Request successful!")
        print("-" * 80)
        print(f"  Video ID: {result['id']}")
        print(f"  Status: {result['status']}")
        print(f"  Batch ID: {result['batch_id']}")
        print(f"  Video URL: {result['video_url']}")
        print("-" * 80)

        # The API automatically polls for completion!
        video_url = result["video_url"]
        video_id = result["id"]
        status = result["status"]

        print("\n" + "=" * 80)
        print("🎉 Video Generation Complete!")
        print("=" * 80)
        print(f"\n📹 Video URL: {video_url}")
        print(f"📋 Video ID: {video_id}")
        print(f"📊 Status: {status}")
        print(
            "\n💡 The API automatically waited for completion - video is ready to use!"
        )
        print("=" * 80)
        return True

    except requests.exceptions.Timeout:
        print("\n❌ Error: Request timed out")
        return False

    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to {API_BASE_URL}")
        print("   Make sure the API server is running")
        return False

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_multiple_configurations():
    """
    Test multiple configuration options
    Note: Each test will take 1-3 minutes as the API polls automatically
    """
    print("\n" + "=" * 80)
    print("Testing Multiple Configurations")
    print("=" * 80)
    print("⚠️  Note: Each test takes 1-3 minutes (API polls automatically)\n")

    test_cases = [
        {
            "name": "Short Video - 9:16 (Mobile)",
            "payload": {
                "prompt": "A peaceful zen garden with flowing water and cherry blossoms",
                "aspect_ratio": "9:16",
                "duration": 6,
                "resolution": "720p",
                "style_id": 60503,
                "is_enhance": True,
            },
        },
        {
            "name": "Square Video - 1:1 (Social Media)",
            "payload": {
                "prompt": "A colorful abstract art piece with flowing paint",
                "aspect_ratio": "1:1",
                "duration": 6,
                "resolution": "720p",
                "style_id": 60503,
                "is_enhance": False,
            },
        },
        {
            "name": "Cinematic - 16:9 HD",
            "payload": {
                "prompt": "A futuristic cityscape at night with neon lights",
                "aspect_ratio": "16:9",
                "duration": 12,
                "resolution": "1080p",
                "style_id": 60503,
                "is_enhance": True,
            },
        },
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"Test Case {i}/{len(test_cases)}: {test_case['name']}")
        print(f"{'=' * 80}")

        print("\n📝 Configuration:")
        for key, value in test_case["payload"].items():
            print(f"  {key}: {value}")

        try:
            print("\n🚀 Sending request...")
            response = requests.post(
                IMAGINE_ENDPOINT, json=test_case["payload"], timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                print(f"\n✅ Success!")
                print(f"   Video ID: {result['id']}")
                print(f"   Video URL: {result['video_url']}")
                results.append(
                    {
                        "name": test_case["name"],
                        "success": True,
                        "video_id": result["id"],
                        "video_url": result["video_url"],
                    }
                )
            else:
                print(f"\n❌ Failed with status {response.status_code}")
                print(f"   Response: {response.text}")
                results.append(
                    {
                        "name": test_case["name"],
                        "success": False,
                        "error": response.text,
                    }
                )

        except Exception as e:
            print(f"\n❌ Exception: {str(e)}")
            results.append(
                {"name": test_case["name"], "success": False, "error": str(e)}
            )

        # Small delay between tests
        if i < len(test_cases):
            print("\nWaiting 3 seconds before next test...")
            time.sleep(3)

    # Print summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"\n{i}. {result['name']}: {status}")
        if result["success"]:
            print(f"   Video URL: {result['video_url']}")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║              Imagine.art Text-to-Video API Test Script                    ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)

    # Check if server is accessible
    try:
        print(f"🔍 Checking API server at {API_BASE_URL}...")
        response = requests.get(f"{API_BASE_URL}/v1/models", timeout=10)
        if response.status_code == 200:
            print("✅ API server is accessible\n")
        else:
            print(f"⚠️  API server responded with status {response.status_code}\n")
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API server at {API_BASE_URL}")
        print("   Please make sure the server is running and the URL is correct")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️  Warning: {str(e)}\n")

    # Run tests based on command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--multi":
        test_multiple_configurations()
    else:
        success = test_imagine_text_to_video()
        sys.exit(0 if success else 1)

    print("\n" + "=" * 80)
    print("Testing Complete!")
    print("=" * 80)
