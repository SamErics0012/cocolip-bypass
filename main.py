import asyncio
import json
import mimetypes
import os
import time
from typing import List, Literal, Optional, Union
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(
    title="Cococlip AI Video & Image Generation API",
    description="Reverse proxy for Cococlip.ai and PicLumen AI with support for text-to-video, image-to-video, audio-to-video, and text-to-image generation",
    version="1.0.0",
    docs_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Headers extracted from the provided CURL command
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.6",
    "content-type": "application/json",
    "origin": "https://cococlip.ai",
    "priority": "u=1, i",
    "referer": "https://cococlip.ai/features/text-to-video",
    "sec-ch-ua": '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "useremail": "cosmiccreation106@gmail.com",
    "cookie": "__Host-authjs.csrf-token=252ceb859e4294ba32fe4878776bfbb1672871d7d1ba8a8bcea563c42357c394%7C2f5e1586b11d0c631fcc3a0ada6bdbf6a8a66a08f8de835e61d14de36a3b0dba; __Secure-authjs.callback-url=https%3A%2F%2Fcococlip.ai; __Secure-authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiOE8zeXc4ZnVvbXBpd3VNbHBuUnRldkJ6bUJrLWFXV3htcGtyVzBGZUVSVGpUZVpOaWlBNDBRVGZ1d2M1SGFDWjRMMHkxMnVzSi14TGxBdVFUYnFDdHcifQ..N7xwsdlnrH_55_t-HSo3gg.QQUrllrAS27IWr9PaWUreBnWrUzU62tAhXXAHJfWV3_tKt5iuIc5nTBd6p1bZfqOabE2Dw-KrOVyXdiuqXaFylc9ak5Vw6MM-RCqy01tMVvY67Ko-B5bowxGqZ_LGBjmTk9-_dFk1PsUBlKN70OdR97-cu8lx475lt4eZCWFWNBgXKR4fpajOrovU9wPQX0yO5V6s9ZiptxoygC3NcLaonM2sFask51DBcg-7dhgnXJPT6e6ODS_rsLCPmBvPQvirSWRZB4NV62jvxbte1vAWsHUD1WdyMI2ibx-0uIu-NUeBZrRNw5OJoJasHzjP6auIBnc_TsKQJK041jGC9ikhNHR6c2JWrTPBFaWq8awQNNWIzGG0Hg5ox6qhn4admWuMqfeA0RDH3qQBaz0LJkrDQ.03JwqV5Wi-UwSRvv-obHhPYp4wjab3pmlEFTllHeVlQ",
}

PICLUMEN_HEADERS = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.6",
    "authorization": "0283a4d403da081d4a789eb1f8ad0fc6a5e6ee94",
    "content-type": "application/json;charset=UTF-8",
    "contenttype": "application/x-www-form-urlencoded;charset=UTF-8",
    "origin": "https://www.piclumen.com",
    "platform": "Web",
    "priority": "u=1, i",
    "referer": "https://www.piclumen.com/",
    "sec-ch-ua": '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
}

# Imagine.art API Headers
IMAGINE_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.6",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJiZGMxZTFkNS03M2JkLTRhNWUtYTE2YS1mMTExNDU5MmY3ZjgiLCJpbnRlZ3JpdHlDaGVjayI6ZmFsc2UsImJhc2VVcmwiOiIiLCJwcm9kdWN0VmFsaWRGb3IiOiJJTUFHSU5FIiwiaXNBZG1pbiI6ZmFsc2UsImlhdCI6MTc2NzMzMDE3MSwiZXhwIjoxNzY3MzUxNzcxLCJzdWIiOiJiZGMxZTFkNS03M2JkLTRhNWUtYTE2YS1mMTExNDU5MmY3ZjgiLCJqdGkiOiJkMWMyZWY4OS1jMmJlLTRiOTctOWVlZi0wY2U0NmYwMDhhMzQifQ.5UuRCh623py0Kh5xowzgp_HPHkATW-tr0vknGk0fGvc",
    "origin": "https://www.imagine.art",
    "priority": "u=1, i",
    "referer": "https://www.imagine.art/",
    "sec-ch-ua": '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
}

# --- Helper Functions ---


def sanitize_filename(filename: str) -> str:
    """Remove spaces and special characters from filename"""
    import re

    # Get name and extension
    name, ext = os.path.splitext(filename)
    # Replace spaces and special chars with underscores
    name = re.sub(r"[^\w\-]", "_", name)
    # Remove consecutive underscores
    name = re.sub(r"_+", "_", name)
    # Remove leading/trailing underscores
    name = name.strip("_")
    return f"{name}{ext}"


def validate_image_file(file: UploadFile) -> None:
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    allowed_extensions = [".jpg", ".jpeg", ".png", ".webp"]

    content_type = file.content_type or ""
    filename = file.filename or ""
    file_ext = os.path.splitext(filename)[1].lower()

    if content_type not in allowed_types and file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image file type. Allowed: JPEG, PNG, WebP. Got: {content_type or file_ext}",
        )


def validate_audio_file(file: UploadFile) -> None:
    allowed_types = [
        "audio/mpeg",
        "audio/mp3",
        "audio/wav",
        "audio/x-wav",
        "audio/wave",
    ]
    allowed_extensions = [".mp3", ".wav", ".wave"]

    content_type = file.content_type or ""
    filename = file.filename or ""
    file_ext = os.path.splitext(filename)[1].lower()

    if content_type not in allowed_types and file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid audio file type. Allowed: MP3, WAV. Got: {content_type or file_ext}",
        )


# --- Pydantic Models ---


class ModelObject(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "hailuo02standard",
                "object": "model",
                "created": 1704067200,
                "owned_by": "cococlip",
            }
        }
    )

    id: str = Field(..., description="Model identifier")
    object: str = Field(default="model", description="Object type")
    created: int = Field(..., description="Unix timestamp of model creation")
    owned_by: str = Field(
        default="cococlip", description="Organization that owns the model"
    )


class ModelsListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "object": "list",
                "data": [
                    {
                        "id": "hailuo02standard",
                        "object": "model",
                        "created": 1704067200,
                        "owned_by": "cococlip",
                    },
                    {
                        "id": "seedancev1lite",
                        "object": "model",
                        "created": 1704067200,
                        "owned_by": "cococlip",
                    },
                    {
                        "id": "hailuo23fast",
                        "object": "model",
                        "created": 1704067200,
                        "owned_by": "cococlip",
                    },
                    {
                        "id": "wan25fast",
                        "object": "model",
                        "created": 1704067200,
                        "owned_by": "cococlip",
                    },
                    {
                        "id": "Infinitetalk",
                        "object": "model",
                        "created": 1704067200,
                        "owned_by": "cococlip",
                    },
                ],
            }
        }
    )

    object: str = Field(default="list", description="Object type")
    data: List[ModelObject] = Field(..., description="List of available models")


class VideoGenerationRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "model": "hailuo02standard",
                "prompt": "A serene landscape with mountains and a flowing river at sunset",
                "prompt_optimizer": True,
                "duration": 5,
                "aspect_ratio": "16:9",
                "resolution": "720p",
            }
        }
    )

    model: Literal["hailuo02standard", "seedancev1lite"] = Field(
        default="hailuo02standard",
        description="AI model for video generation",
        json_schema_extra={"example": "hailuo02standard"},
    )
    prompt: str = Field(
        ...,
        description="Text description for the video",
        min_length=1,
        max_length=1000,
        json_schema_extra={
            "example": "A serene landscape with mountains and a flowing river at sunset"
        },
    )
    prompt_optimizer: bool = Field(
        default=True,
        description="Optimize prompt for better results",
        json_schema_extra={"example": True},
    )
    duration: Literal[5, 6, 10] = Field(
        default=5,
        description="Duration in seconds (Hailuo: 6, Seedance: 5 or 10)",
        json_schema_extra={"example": 5},
    )
    aspect_ratio: Literal["21:9", "16:9", "4:3", "1:1", "3:4", "9:16", "9:21"] = Field(
        default="1:1",
        description="Video aspect ratio",
        json_schema_extra={"example": "16:9"},
    )
    resolution: Literal["480p", "720p", "1080p", "512p", "768p"] = Field(
        default="480p",
        description="Video resolution quality",
        json_schema_extra={"example": "720p"},
    )


class VideoGenerationResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://cococlip.ai/videos/example-video.mp4",
                "status": "COMPLETED",
            }
        }
    )

    url: str = Field(..., description="URL of the generated video")
    status: str = Field(
        ..., description="Status of the video generation (COMPLETED, FAILED, etc.)"
    )


class ImageToVideoRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "model": "hailuo23fast",
                "prompt": "make the image come to life with gentle motion",
                "resolution": "768p",
                "duration": 6,
                "enable_prompt_expansion": False,
                "negative_prompt": "",
            }
        }
    )

    model: Literal["hailuo23fast", "wan25fast"] = Field(
        default="hailuo23fast",
        description="AI model for image-to-video generation",
        json_schema_extra={"example": "hailuo23fast"},
    )
    prompt: str = Field(
        ...,
        description="Text prompt describing the desired motion",
        min_length=1,
        max_length=500,
        json_schema_extra={"example": "make the image come to life with gentle motion"},
    )
    resolution: Literal["768p", "720p", "1080p"] = Field(
        default="768p",
        description="Video resolution (hailuo23fast: 768p, wan25fast: 720p/1080p)",
        json_schema_extra={"example": "768p"},
    )
    duration: Literal[5, 6, 10] = Field(
        default=6,
        description="Duration in seconds (hailuo23fast: 6s/10s, wan25fast: 5s/10s)",
        json_schema_extra={"example": 6},
    )
    enable_prompt_expansion: bool = Field(
        default=False,
        description="Enable automatic prompt expansion",
        json_schema_extra={"example": False},
    )
    negative_prompt: str = Field(
        default="",
        description="Negative prompt to avoid unwanted elements",
        json_schema_extra={"example": ""},
    )


class ImageToVideoResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://d1q70pf5vjeyhc.cloudfront.net/predictions/45a96667279e4a2f83cfe131566d4923/1.mp4",
                "status": "completed",
                "task_id": "45a96667279e4a2f83cfe131566d4923",
            }
        }
    )

    url: str = Field(..., description="URL of the generated video")
    status: str = Field(..., description="Status of the video generation")
    task_id: str = Field(..., description="Task ID for tracking")


class AudioToVideoRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"prompt": "", "resolution": "720p", "audio_duration": 5.06}
        }
    )

    prompt: str = Field(
        default="",
        description="Optional text prompt for additional control",
        json_schema_extra={"example": ""},
    )
    resolution: Literal["720p", "1080p"] = Field(
        default="720p",
        description="Video resolution",
        json_schema_extra={"example": "720p"},
    )
    audio_duration: Optional[float] = Field(
        default=None,
        description="Duration of audio in seconds (auto-detected if not provided)",
        json_schema_extra={"example": 5.06},
    )


class AudioToVideoResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://d2p7pge43lyniu.cloudfront.net/output/e160ebee-e7dc-44f3-99f5-d0a632e206c8-u1_614106f4-e845-4f2b-a9a6-ea0a8b68ccec.mp4",
                "status": "COMPLETED",
                "task_id": "be49ce022530438f984ffd602ec454ad",
                "inference_time": 128036,
            }
        }
    )

    url: str = Field(..., description="URL of the generated video")
    status: str = Field(..., description="Status of the video generation")
    task_id: str = Field(..., description="Task ID for tracking")
    inference_time: Optional[int] = Field(
        None, description="Time taken for inference in milliseconds"
    )


class TextToImageRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "model": "piclumen-realistic-v2",
                "prompt": "cat sitting on a couch",
                "negative_prompt": "NSFW, watermark",
                "width": 1024,
                "height": 1024,
                "steps": 25,
                "cfg_scale": 4.5,
                "batch_size": 1,
            }
        }
    )

    model: Literal["piclumen-realistic-v2", "midjourney"] = Field(
        default="piclumen-realistic-v2",
        description="AI model for image generation (piclumen-realistic-v2 or midjourney)",
        json_schema_extra={"example": "piclumen-realistic-v2"},
    )
    prompt: str = Field(
        ...,
        description="Text description for the image",
        min_length=1,
        max_length=2000,
        json_schema_extra={"example": "cat sitting on a couch"},
    )
    negative_prompt: str = Field(
        default="NSFW, watermark",
        description="Negative prompt to avoid unwanted elements (not used by Midjourney)",
        json_schema_extra={"example": "NSFW, watermark"},
    )
    width: Literal[512, 768, 1024] = Field(
        default=1024, description="Image width", json_schema_extra={"example": 1024}
    )
    height: Literal[512, 768, 1024] = Field(
        default=1024, description="Image height", json_schema_extra={"example": 1024}
    )
    steps: Optional[int] = Field(
        default=25,
        ge=0,
        le=50,
        description="Number of generation steps (ignored by Midjourney, use 0)",
        json_schema_extra={"example": 25},
    )
    cfg_scale: Optional[float] = Field(
        default=4.5,
        ge=0.0,
        le=20.0,
        description="CFG scale for prompt adherence (ignored by Midjourney, use 0)",
        json_schema_extra={"example": 4.5},
    )
    batch_size: int = Field(
        default=1,
        ge=1,
        le=4,
        description="Number of images to generate (1-4 for PicLumen, always 4 for Midjourney)",
        json_schema_extra={"example": 1},
    )


class ImageData(BaseModel):
    url: str = Field(..., description="URL of the generated image")


class TextToImageResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "created": 1704067200,
                "data": [
                    {
                        "url": "https://images.piclumen.com/normal/20251231/14/c2f4277c35934b55a0c67d23cca3b6da.webp"
                    },
                    {
                        "url": "https://images.piclumen.com/normal/20251231/14/f8e9d2c1a4b35678e9f01234a5b6c7d8.webp"
                    },
                ],
                "task_id": "ed67501f-6e29-487b-955d-086dc9646037",
            }
        }
    )

    created: int = Field(
        ..., description="Unix timestamp of when the images were created"
    )
    data: List[ImageData] = Field(..., description="List of generated images")
    task_id: str = Field(..., description="Task ID for tracking")


class ImagineTextToVideoRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "A cat eating hotdogs in a park",
                "aspect_ratio": "16:9",
                "duration": 12,
                "resolution": "1080p",
                "style_id": 60503,
                "is_enhance": True,
            }
        }
    )

    prompt: str = Field(
        ...,
        description="Text description for the video",
        min_length=1,
        max_length=2000,
        json_schema_extra={"example": "A cat eating hotdogs in a park"},
    )
    aspect_ratio: Literal["16:9", "9:16", "4:3", "1:1"] = Field(
        default="16:9",
        description="Video aspect ratio",
        json_schema_extra={"example": "16:9"},
    )
    duration: Literal[5, 6, 12] = Field(
        default=12,
        description="Video duration in seconds (5, 6, or 12)",
        json_schema_extra={"example": 12},
    )
    resolution: Literal["720p", "1080p"] = Field(
        default="1080p",
        description="Video resolution",
        json_schema_extra={"example": "1080p"},
    )
    style_id: int = Field(
        default=60503,
        description="Style ID for video generation",
        json_schema_extra={"example": 60503},
    )
    is_enhance: bool = Field(
        default=True,
        description="Enable prompt enhancement",
        json_schema_extra={"example": True},
    )


class ImagineTextToVideoResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "85f8e695-38cc-4023-b15e-49313cadcbfc",
                "status": "COMPLETED",
                "video_url": "https://asset.imagine.art/processed/85f8e695-38cc-4023-b15e-49313cadcbfc",
                "batch_id": "dde09073-c355-4443-aa80-0736d8358621",
            }
        }
    )

    id: str = Field(..., description="Generation task ID")
    status: str = Field(..., description="Status of the video generation")
    video_url: str = Field(..., description="URL to check for the generated video")
    batch_id: str = Field(..., description="Batch ID for tracking")


# --- Endpoints ---


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    from fastapi.responses import HTMLResponse

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{app.title} - Swagger UI</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css">
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: #000000 !important;
            }}

            .swagger-ui {{
                background: #000000 !important;
            }}

            .swagger-ui .opblock-tag {{
                color: #ffffff !important;
                border-bottom: 1px solid #333333 !important;
            }}

            .swagger-ui .opblock {{
                background: #0a0a0a !important;
                border: 1px solid #333333 !important;
                border-radius: 4px !important;
                margin-bottom: 15px !important;
            }}

            .swagger-ui .opblock .opblock-summary {{
                background: #111111 !important;
                border-color: #333333 !important;
            }}

            .swagger-ui .opblock .opblock-summary:hover {{
                background: #1a1a1a !important;
            }}

            .swagger-ui .opblock-description-wrapper,
            .swagger-ui .opblock-body {{
                background: #0a0a0a !important;
                color: #ffffff !important;
            }}

            .swagger-ui .btn {{
                background: #1a1a1a !important;
                color: #ffffff !important;
                border: 1px solid #333333 !important;
            }}

            .swagger-ui .btn:hover {{
                background: #2a2a2a !important;
            }}

            .swagger-ui .btn.execute {{
                background: #0d47a1 !important;
                border-color: #0d47a1 !important;
            }}

            .swagger-ui .btn.execute:hover {{
                background: #1565c0 !important;
            }}

            .swagger-ui input[type=text],
            .swagger-ui input[type=password],
            .swagger-ui input[type=email],
            .swagger-ui textarea,
            .swagger-ui select {{
                background: #1a1a1a !important;
                color: #ffffff !important;
                border: 1px solid #333333 !important;
            }}

            .swagger-ui select option {{
                background: #1a1a1a !important;
                color: #ffffff !important;
            }}

            .swagger-ui .response-col_status {{
                color: #ffffff !important;
            }}

            .swagger-ui .response-col_description {{
                color: #ffffff !important;
            }}

            .swagger-ui table {{
                background: #0a0a0a !important;
            }}

            .swagger-ui table thead tr th,
            .swagger-ui table tbody tr td {{
                color: #ffffff !important;
                border-color: #333333 !important;
            }}

            .swagger-ui .model-box,
            .swagger-ui .model {{
                background: #1a1a1a !important;
                color: #ffffff !important;
                border: 1px solid #333333 !important;
            }}

            .swagger-ui .prop-type {{
                color: #4fc3f7 !important;
            }}

            .swagger-ui .prop-format {{
                color: #81c784 !important;
            }}

            .swagger-ui .parameter__name {{
                color: #ffffff !important;
            }}

            .swagger-ui .parameter__type {{
                color: #4fc3f7 !important;
            }}

            .swagger-ui .renderedMarkdown p,
            .swagger-ui .renderedMarkdown code,
            .swagger-ui .renderedMarkdown pre {{
                color: #ffffff !important;
            }}

            .swagger-ui code {{
                background: #1a1a1a !important;
                color: #4fc3f7 !important;
                border: 1px solid #333333 !important;
            }}

            .swagger-ui pre {{
                background: #1a1a1a !important;
                color: #ffffff !important;
                border: 1px solid #333333 !important;
            }}

            .swagger-ui .topbar {{
                background: #0a0a0a !important;
                border-bottom: 1px solid #333333 !important;
            }}

            .swagger-ui .info .title,
            .swagger-ui .info .title small,
            .swagger-ui .info p,
            .swagger-ui .info a {{
                color: #ffffff !important;
            }}

            .swagger-ui .scheme-container {{
                background: #0a0a0a !important;
                border: 1px solid #333333 !important;
            }}

            .swagger-ui .loading-container {{
                background: #000000 !important;
            }}

            .swagger-ui .model-toggle {{
                color: #ffffff !important;
            }}

            .swagger-ui .model-toggle:after {{
                background: #4fc3f7 !important;
            }}

            .swagger-ui section.models {{
                background: #0a0a0a !important;
                border: 1px solid #333333 !important;
            }}

            .swagger-ui section.models h4 {{
                color: #ffffff !important;
            }}

            .swagger-ui .responses-inner h4,
            .swagger-ui .responses-inner h5 {{
                color: #ffffff !important;
            }}

            .swagger-ui .tab li {{
                color: #ffffff !important;
            }}

            .swagger-ui .tab li.active {{
                background: #1a1a1a !important;
            }}

            .swagger-ui .dialog-ux {{
                background: #0a0a0a !important;
                border: 1px solid #333333 !important;
            }}

            .swagger-ui .dialog-ux .modal-ux {{
                background: #0a0a0a !important;
                border: 1px solid #333333 !important;
            }}

            .swagger-ui .dialog-ux .modal-ux-header {{
                background: #111111 !important;
                border-bottom: 1px solid #333333 !important;
            }}

            .swagger-ui .dialog-ux .modal-ux-header h3 {{
                color: #ffffff !important;
            }}

            .swagger-ui .dialog-ux .modal-ux-content {{
                background: #0a0a0a !important;
                color: #ffffff !important;
            }}

            .swagger-ui a {{
                color: #4fc3f7 !important;
            }}

            .swagger-ui a:hover {{
                color: #81d4fa !important;
            }}

            .swagger-ui .highlight-code {{
                background: #1a1a1a !important;
            }}

            .swagger-ui .highlight-code .microlight {{
                color: #ffffff !important;
            }}

            .swagger-ui .copy-to-clipboard {{
                background: #1a1a1a !important;
                border: 1px solid #333333 !important;
            }}

            .swagger-ui .copy-to-clipboard button {{
                background: transparent !important;
                color: #ffffff !important;
            }}
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {{
                window.ui = SwaggerUIBundle({{
                    url: '{app.openapi_url}',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "BaseLayout",
                    supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
                    defaultModelsExpandDepth: 1,
                    defaultModelExpandDepth: 3,
                    docExpansion: 'list',
                    filter: false,
                    showRequestHeaders: true,
                    showExtensions: true,
                    tryItOutEnabled: true,
                    persistAuthorization: true
                }})
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get(
    "/v1/models",
    response_model=ModelsListResponse,
    tags=["Models"],
    summary="List Available Models",
    description="""
    Returns a list of available AI models for video and image generation.

    This endpoint is OpenAI-compatible and follows the same response structure.

    **Available Models:**
    - `hailuo02standard` - High quality text-to-video model (6s duration)
    - `seedancev1lite` - Lightweight text-to-video model (5s or 10s duration)
    - `hailuo23fast` - Fast image-to-video model (6s/10s duration, 768p)
    - `wan25fast` - Wan 2.5 image-to-video model (5s/10s duration, 720p/1080p)
    - `Infinitetalk` - Audio-to-video model (talking portrait, 720p/1080p)
    - `piclumen-realistic-v2` - PicLumen Realistic V2 text-to-image model
    - `midjourney` - Midjourney-style text-to-image model (supports batch generation)
    """,
    responses={
        200: {
            "description": "List of available models",
            "content": {
                "application/json": {
                    "example": {
                        "object": "list",
                        "data": [
                            {
                                "id": "hailuo02standard",
                                "object": "model",
                                "created": 1704067200,
                                "owned_by": "cococlip",
                            },
                            {
                                "id": "seedancev1lite",
                                "object": "model",
                                "created": 1704067200,
                                "owned_by": "cococlip",
                            },
                            {
                                "id": "hailuo23fast",
                                "object": "model",
                                "created": 1704067200,
                                "owned_by": "cococlip",
                            },
                            {
                                "id": "wan25fast",
                                "object": "model",
                                "created": 1704067200,
                                "owned_by": "cococlip",
                            },
                            {
                                "id": "Infinitetalk",
                                "object": "model",
                                "created": 1704067200,
                                "owned_by": "cococlip",
                            },
                        ],
                    }
                }
            },
        }
    },
)
async def list_models():
    return ModelsListResponse(
        object="list",
        data=[
            ModelObject(
                id="hailuo02standard",
                object="model",
                created=1704067200,
                owned_by="cococlip",
            ),
            ModelObject(
                id="seedancev1lite",
                object="model",
                created=1704067200,
                owned_by="cococlip",
            ),
            ModelObject(
                id="hailuo23fast",
                object="model",
                created=1704067200,
                owned_by="cococlip",
            ),
            ModelObject(
                id="wan25fast", object="model", created=1704067200, owned_by="cococlip"
            ),
            ModelObject(
                id="Infinitetalk",
                object="model",
                created=1704067200,
                owned_by="cococlip",
            ),
            ModelObject(
                id="piclumen-realistic-v2",
                object="model",
                created=1704067200,
                owned_by="piclumen",
            ),
            ModelObject(
                id="midjourney", object="model", created=1704067200, owned_by="piclumen"
            ),
            ModelObject(
                id="imagine-text-to-video",
                object="model",
                created=1704067200,
                owned_by="imagine.art",
            ),
        ],
    )


@app.post(
    "/v1/video/generations",
    response_model=VideoGenerationResponse,
    tags=["Video Generation"],
    summary="Generate AI Video from Text",
    description="""
    Generate a video using AI models (Hailuo or Seedance).

    **Supported Models:**
    - `hailuo02standard` - High quality model (supports duration: 6s)
    - `seedancev1lite` - Lite model (supports duration: 5s or 10s)

    **Parameters:**
    - Choose your preferred model, aspect ratio, resolution, and duration
    - Provide a descriptive prompt for best results
    - Enable prompt_optimizer for enhanced output quality

    **Response:**
    - Returns the video URL and status upon completion
    - The API polls automatically until the video is ready
    """,
    responses={
        200: {
            "description": "Video generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "url": "https://cococlip.ai/videos/example-video.mp4",
                        "status": "COMPLETED",
                    }
                }
            },
        },
        400: {
            "description": "Invalid request or video generation failed",
        },
        500: {
            "description": "Internal server error or upstream API error",
        },
    },
)
async def generate_video(request: VideoGenerationRequest):
    if request.model == "hailuo02standard":
        url_generate = "https://cococlip.ai/api/v3/text2video/hailuo02standard"
        # Hailuo specific mapping if needed.
        # Assuming it accepts same keys or we pass what we have.
        payload = {
            "prompt": request.prompt,
            "prompt_optimizer": request.prompt_optimizer,
            "duration": request.duration,
            # Pass new params if supported
            "aspect_ratio": request.aspect_ratio,
            "resolution": request.resolution,
        }
        url_status_base = "https://cococlip.ai/api/v3/text2video/hailuo02standard/get"

    elif request.model == "seedancev1lite":
        url_generate = "https://cococlip.ai/api/v3/text2video/seedancev1lite"
        payload = {
            "prompt": request.prompt,
            "aspect_ratio": request.aspect_ratio,
            "duration": request.duration,
            "resolution": request.resolution,
            # seedancev1lite might not use prompt_optimizer, but we can omit if unsure or include if safe.
            # Based on curl, it wasn't there.
        }
        url_status_base = "https://cococlip.ai/api/v3/text2video/seedancev1lite/get"
    else:
        raise HTTPException(status_code=400, detail="Invalid model specified")

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Step 1: Send generation request
        try:
            response = await client.post(url_generate, headers=HEADERS, json=payload)
            response.raise_for_status()
            data = response.json()

            generation_id = data.get("id")
            if not generation_id:
                generation_id = (
                    data.get("job_id") or data.get("uuid") or data.get("task_id")
                )

            if not generation_id:
                raise HTTPException(
                    status_code=500,
                    detail=f"Could not extract generation ID from response: {data}",
                )

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Generation request failed: {e.response.text}",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

        # Step 2: Poll for results

        while True:
            try:
                # Wait 10 seconds before polling
                await asyncio.sleep(10)

                status_response = await client.get(
                    url_status_base, headers=HEADERS, params={"id": generation_id}
                )
                status_response.raise_for_status()
                try:
                    status_data = status_response.json()
                except json.JSONDecodeError:
                    print(
                        f"Non-JSON response received. Content: {status_response.text}"
                    )
                    continue

                status = status_data.get("status")

                if status == "COMPLETED":
                    return VideoGenerationResponse(
                        url=status_data.get("url"), status=status
                    )
                elif status == "FAILED":
                    raise HTTPException(
                        status_code=400, detail="Video generation failed"
                    )

                print(f"Current status: {status}. Waiting...")

            except httpx.HTTPStatusError as e:
                print(f"Polling error: {e.response.text}")
                if e.response.status_code == 429:
                    await asyncio.sleep(20)
                    continue
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Polling failed: {e.response.text}",
                )


@app.post(
    "/v1/image-to-video/generations",
    response_model=ImageToVideoResponse,
    tags=["Image to Video"],
    summary="Generate Video from Image",
    description="""
    Generate a video from an uploaded image using AI.

    **Process:**
    1. Upload an image file (JPEG, PNG, WebP supported)
    2. Provide a prompt describing the desired motion
    3. The API handles the upload and generation automatically
    4. Polls until the video is ready and returns the final URL

    **Parameters:**
    - `image`: Image file to animate (required)
    - `model`: AI model to use (hailuo23fast or wan25fast)
    - `prompt`: Description of the desired motion (required)
    - `resolution`: Video resolution (hailuo23fast: 768p, wan25fast: 720p/1080p)
    - `duration`: Video duration in seconds (hailuo23fast: 6s/10s, wan25fast: 5s/10s)
    - `enable_prompt_expansion`: Enable automatic prompt expansion (optional)
    - `negative_prompt`: Negative prompt to avoid unwanted elements (optional)

    **Models:**
    - `hailuo23fast` - Fast, high-quality image-to-video model (768p, 6s/10s)
    - `wan25fast` - Wan 2.5 image-to-video model (720p/1080p, 5s/10s)
    """,
    responses={
        200: {
            "description": "Video generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "url": "https://d1q70pf5vjeyhc.cloudfront.net/predictions/45a96667279e4a2f83cfe131566d4923/1.mp4",
                        "status": "completed",
                        "task_id": "45a96667279e4a2f83cfe131566d4923",
                    }
                }
            },
        },
        400: {
            "description": "Invalid request or generation failed",
        },
        500: {
            "description": "Internal server error or upload failed",
        },
    },
)
async def generate_video_from_image(
    image: UploadFile = File(..., description="Image file to animate"),
    model: str = Form(
        "hailuo23fast", description="AI model (hailuo23fast or wan25fast)"
    ),
    prompt: str = Form(..., description="Description of the desired motion"),
    resolution: str = Form("768p", description="Video resolution"),
    duration: int = Form(6, description="Duration in seconds"),
    enable_prompt_expansion: bool = Form(
        False, description="Enable automatic prompt expansion"
    ),
    negative_prompt: str = Form(
        "", description="Negative prompt to avoid unwanted elements"
    ),
):
    validate_image_file(image)

    if model not in ["hailuo23fast", "wan25fast"]:
        raise HTTPException(
            status_code=400, detail="Invalid model. Choose hailuo23fast or wan25fast"
        )

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            file_content = await image.read()
            file_name = sanitize_filename(image.filename or "image.jpg")

            upload_payload = {"fileName": file_name}
            upload_response = await client.post(
                "https://cococlip.ai/api/v2/upload",
                headers=HEADERS,
                json=upload_payload,
            )
            upload_response.raise_for_status()
            upload_data = upload_response.json()

            presigned_url = upload_data.get("url")
            if not presigned_url:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to get presigned URL: {upload_data}",
                )

            content_type = (
                image.content_type or mimetypes.guess_type(file_name)[0] or "image/jpeg"
            )

            put_response = await client.put(
                presigned_url,
                content=file_content,
                headers={"Content-Type": content_type},
            )
            put_response.raise_for_status()

            print(f"Image uploaded successfully. Status: {put_response.status_code}")

            parsed_r2_url = urlparse(presigned_url)
            r2_path = parsed_r2_url.path
            uploaded_image_url = f"https://cococlip.aiitalianbrainrot.com{r2_path}"
            print(f"Using CDN URL: {uploaded_image_url}")

            if model == "hailuo23fast":
                generation_payload = {
                    "prompt": prompt,
                    "image": uploaded_image_url,
                    "duration": duration,
                }
            else:
                generation_payload = {
                    "image": uploaded_image_url,
                    "prompt": prompt,
                    "resolution": resolution,
                    "duration": duration,
                    "enable_prompt_expansion": enable_prompt_expansion,
                    "negative_prompt": negative_prompt,
                }

            generation_url = f"https://cococlip.ai/api/v3/image2video/{model}"
            generation_response = await client.post(
                generation_url, headers=HEADERS, json=generation_payload
            )
            generation_response.raise_for_status()
            generation_data = generation_response.json()

            if model == "hailuo23fast":
                if generation_data.get("code") != 200:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Generation request failed: {generation_data}",
                    )
                task_id = generation_data.get("data", {}).get("taskId")
            else:
                if generation_data.get("code") != 200:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Generation request failed: {generation_data}",
                    )
                task_id = generation_data.get("data", {}).get("taskId")

            if not task_id:
                raise HTTPException(
                    status_code=500,
                    detail=f"Could not extract task ID from response: {generation_data}",
                )

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Request failed: {e.response.text}",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

        while True:
            try:
                await asyncio.sleep(10)

                status_url = f"https://cococlip.ai/api/v3/image2video/{model}/get"
                status_response = await client.get(
                    status_url, headers=HEADERS, params={"id": task_id}
                )
                status_response.raise_for_status()

                try:
                    status_data = status_response.json()
                except json.JSONDecodeError:
                    print(
                        f"Non-JSON response received. Content: {status_response.text}"
                    )
                    continue

                if model == "hailuo23fast":
                    if status_data.get("code") != 200:
                        print(f"Unexpected response code: {status_data}")
                        continue

                    data = status_data.get("data", {})
                    success_flag = data.get("successFlag")
                    status = data.get("status")

                    if success_flag == 1 and status == "completed":
                        video_url = data.get("response", {}).get("url")
                        if not video_url:
                            raise HTTPException(
                                status_code=500,
                                detail=f"Video URL not found in completed response: {status_data}",
                            )

                        return ImageToVideoResponse(
                            url=video_url, status=status, task_id=task_id
                        )

                    elif status == "failed":
                        raise HTTPException(
                            status_code=400, detail="Video generation failed"
                        )

                    print(
                        f"Current status: {status} (successFlag: {success_flag}). Waiting..."
                    )

                else:
                    video_url = status_data.get("url")
                    status = status_data.get("status")

                    if status == "COMPLETED" and video_url:
                        return ImageToVideoResponse(
                            url=video_url, status=status, task_id=task_id
                        )

                    elif status == "FAILED":
                        raise HTTPException(
                            status_code=400, detail="Video generation failed"
                        )

                    elif not video_url and not status:
                        print(f"Still processing... Waiting...")
                    else:
                        print(f"Current status: {status}. Waiting...")

            except httpx.HTTPStatusError as e:
                print(f"Polling error: {e.response.text}")
                if e.response.status_code == 429:
                    await asyncio.sleep(20)
                    continue
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Polling failed: {e.response.text}",
                )


@app.post(
    "/v1/audio-to-video/generations",
    response_model=AudioToVideoResponse,
    tags=["Audio to Video"],
    summary="Generate Talking Portrait Video from Audio",
    description="""
    Generate a talking portrait video from an image and audio file using Infinite Talk AI.

    **Process:**
    1. Upload an image file (portrait/face photo recommended)
    2. Upload an audio file (speech, voice, etc.)
    3. Optionally provide a text prompt for additional control
    4. The API handles uploads and generation automatically
    5. Polls until the video is ready and returns the final URL

    **Parameters:**
    - `image`: Image file of the portrait (required)
    - `audio`: Audio file to sync with the portrait (required)
    - `prompt`: Optional text prompt for additional control
    - `resolution`: Video resolution (720p or 1080p)
    - `audio_duration`: Optional audio duration in seconds (auto-detected if not provided)

    **Model:** Infinitetalk (talking portrait generation with audio sync)

    **Use Cases:**
    - Create talking avatars
    - Animate portraits with voiceovers
    - Generate video presentations with audio narration
    """,
    responses={
        200: {
            "description": "Video generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "url": "https://d2p7pge43lyniu.cloudfront.net/output/e160ebee-e7dc-44f3-99f5-d0a632e206c8-u1_614106f4-e845-4f2b-a9a6-ea0a8b68ccec.mp4",
                        "status": "COMPLETED",
                        "task_id": "be49ce022530438f984ffd602ec454ad",
                        "inference_time": 128036,
                    }
                }
            },
        },
        400: {
            "description": "Invalid request or generation failed",
        },
        500: {
            "description": "Internal server error or upload failed",
        },
    },
)
async def generate_audio_to_video(
    image: UploadFile = File(..., description="Image file of the portrait"),
    audio: UploadFile = File(..., description="Audio file to sync with the portrait"),
    prompt: str = Form("", description="Optional text prompt for additional control"),
    resolution: str = Form("720p", description="Video resolution (720p or 1080p)"),
    audio_duration: Union[float, str, None] = Form(
        None, description="Audio duration in seconds (auto-detected if not provided)"
    ),
):
    validate_image_file(image)
    validate_audio_file(audio)

    # Handle empty string for audio_duration
    if audio_duration == "" or audio_duration is None:
        audio_duration = None
    else:
        try:
            audio_duration = float(audio_duration)
        except (ValueError, TypeError):
            audio_duration = None

    async with httpx.AsyncClient(timeout=180.0) as client:
        try:
            image_content = await image.read()
            image_name = sanitize_filename(image.filename or "image.jpg")

            image_upload_payload = {"fileName": image_name}
            image_upload_response = await client.post(
                "https://cococlip.ai/api/v2/upload",
                headers=HEADERS,
                json=image_upload_payload,
            )
            image_upload_response.raise_for_status()
            image_upload_data = image_upload_response.json()

            print(f"Image upload response: {image_upload_data}")

            image_presigned_url = image_upload_data.get("url")

            if not image_presigned_url:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to get image presigned URL: {image_upload_data}",
                )

            image_content_type = (
                image.content_type
                or mimetypes.guess_type(image_name)[0]
                or "image/jpeg"
            )

            image_put_response = await client.put(
                image_presigned_url,
                content=image_content,
                headers={"Content-Type": image_content_type},
            )
            image_put_response.raise_for_status()

            print(
                f"Image uploaded successfully. Status: {image_put_response.status_code}"
            )

            # Extract filename from R2 URL and construct public CDN URL
            parsed_r2_url = urlparse(image_presigned_url)
            r2_path = parsed_r2_url.path  # e.g., /upload/sam566-1767091949020rn5aai.png
            uploaded_image_url = f"https://cococlip.aiitalianbrainrot.com{r2_path}"
            print(f"Using CDN URL: {uploaded_image_url}")

            audio_content = await audio.read()
            audio_name = sanitize_filename(audio.filename or "audio.mp3")

            audio_upload_payload = {"fileName": audio_name}
            audio_upload_response = await client.post(
                "https://cococlip.ai/api/v2/upload",
                headers=HEADERS,
                json=audio_upload_payload,
            )
            audio_upload_response.raise_for_status()
            audio_upload_data = audio_upload_response.json()

            print(f"Audio upload response: {audio_upload_data}")

            audio_presigned_url = audio_upload_data.get("url")

            if not audio_presigned_url:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to get audio presigned URL: {audio_upload_data}",
                )

            audio_content_type = (
                audio.content_type
                or mimetypes.guess_type(audio_name)[0]
                or "audio/mpeg"
            )

            audio_put_response = await client.put(
                audio_presigned_url,
                content=audio_content,
                headers={"Content-Type": audio_content_type},
            )
            audio_put_response.raise_for_status()

            print(
                f"Audio uploaded successfully. Status: {audio_put_response.status_code}"
            )

            # Extract filename from R2 URL and construct public CDN URL
            parsed_audio_r2_url = urlparse(audio_presigned_url)
            audio_r2_path = parsed_audio_r2_url.path
            uploaded_audio_url = (
                f"https://cococlip.aiitalianbrainrot.com{audio_r2_path}"
            )
            print(f"Using audio CDN URL: {uploaded_audio_url}")

            generation_payload = {
                "image": uploaded_image_url,
                "audio": uploaded_audio_url,
                "prompt": prompt,
                "resolution": resolution,
            }

            if audio_duration is not None:
                generation_payload["audio_duration"] = str(audio_duration)
            else:
                generation_payload["audio_duration"] = "5.0"

            print(f"Generation payload: {generation_payload}")

            generation_response = await client.post(
                "https://cococlip.ai/api/v3/audio2video/Infinitetalk",
                headers=HEADERS,
                json=generation_payload,
            )
            generation_response.raise_for_status()
            generation_data = generation_response.json()

            print(f"Generation response: {generation_data}")

            task_id = generation_data.get("task_id")
            if not task_id:
                raise HTTPException(
                    status_code=500,
                    detail=f"Could not extract task ID from response: {generation_data}",
                )

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Request failed: {e.response.text}",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

        while True:
            try:
                await asyncio.sleep(10)

                status_response = await client.get(
                    "https://cococlip.ai/api/v3/audio2video/Infinitetalk/get",
                    headers=HEADERS,
                    params={"id": task_id},
                )
                status_response.raise_for_status()

                try:
                    status_data = status_response.json()
                except json.JSONDecodeError:
                    print(f"Non-JSON or empty response. Still processing... Waiting...")
                    continue

                video_url = status_data.get("url")
                status = status_data.get("status")
                inference_time = status_data.get("inference_time")

                if status == "COMPLETED" and video_url:
                    return AudioToVideoResponse(
                        url=video_url,
                        status=status,
                        task_id=task_id,
                        inference_time=inference_time,
                    )

                elif status == "FAILED":
                    raise HTTPException(
                        status_code=400, detail="Video generation failed"
                    )

                elif not video_url and not status:
                    print(f"Still processing... Waiting...")
                else:
                    print(f"Current status: {status}. Waiting...")

            except httpx.HTTPStatusError as e:
                print(f"Polling error: {e.response.text}")
                if e.response.status_code == 429:
                    await asyncio.sleep(20)
                    continue
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Polling failed: {e.response.text}",
                )


@app.post(
    "/v1/text-to-image/generations",
    response_model=TextToImageResponse,
    tags=["Text to Image"],
    summary="Generate Image from Text",
    description="""
    Generate images from a text prompt using PicLumen or Midjourney models.

    **Process:**
    1. Submit a text prompt describing the desired image
    2. The API creates a generation task and returns a task ID
    3. Polls automatically until images are ready
    4. Returns the final image URLs (1-4 images depending on batch_size)

    **Parameters:**
    - `model`: Choose between "piclumen-realistic-v2" or "midjourney"
    - `prompt`: Text description of the image (required)
    - `negative_prompt`: Elements to avoid (only for piclumen-realistic-v2)
    - `width`: Image width in pixels (512, 768, or 1024)
    - `height`: Image height in pixels (512, 768, or 1024)
    - `batch_size`: Number of images to generate (1-4, default: 1)
    - `steps`: Generation steps (piclumen-realistic-v2 only, 1-50, default: 25)
    - `cfg_scale`: CFG scale (piclumen-realistic-v2 only, 1.0-20.0, default: 4.5)

    **Models:**
    - **PicLumen Realistic V2** - High quality realistic image generation (1-4 images)
    - **Midjourney** - Midjourney-style artistic image generation (always generates 4 images)
    """,
    responses={
        200: {
            "description": "Image(s) generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "created": 1704067200,
                        "data": [
                            {
                                "url": "https://images.piclumen.com/normal/20251231/14/c2f4277c35934b55a0c67d23cca3b6da.webp"
                            },
                            {
                                "url": "https://images.piclumen.com/normal/20251231/14/f8e9d2c1a4b35678e9f01234a5b6c7d8.webp"
                            },
                            {
                                "url": "https://images.piclumen.com/normal/20251231/14/a1b2c3d4e5f6789012345678901abcde.webp"
                            },
                            {
                                "url": "https://images.piclumen.com/normal/20251231/14/9876543210fedcba09876543210fedcb.webp"
                            },
                        ],
                        "task_id": "ed67501f-6e29-487b-955d-086dc9646037",
                    }
                }
            },
        },
        400: {
            "description": "Invalid request or generation failed",
        },
        500: {
            "description": "Internal server error or upstream API error",
        },
    },
)
async def generate_text_to_image(request: TextToImageRequest):
    import random

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            seed = random.randint(1000000000, 9999999999)

            if request.model == "piclumen-realistic-v2":
                generation_payload = {
                    "model_id": "34ec1b5a-8962-4a93-b047-68cec9691dc2",
                    "prompt": request.prompt,
                    "negative_prompt": request.negative_prompt,
                    "seed": seed,
                    "mainCategory": "",
                    "subCategory": "",
                    "continueCreate": False,
                    "resolution": {
                        "width": request.width,
                        "height": request.height,
                        "batch_size": request.batch_size,
                    },
                    "batch_size": request.batch_size,
                    "steps": request.steps,
                    "cfg": request.cfg_scale,
                    "sampler_name": "dpmpp_2m_sde_gpu",
                    "scheduler": "karras",
                    "multi_img2img_info": {"style_list": []},
                    "img_control_info": {"style_list": []},
                    "highPixels": False,
                    "model_ability": {"anime_style_control": None},
                    "denoise": 1,
                    "type": "image",
                }
            else:
                generation_payload = {
                    "model_id": "tmjv7-a1b2c3d4-e5f6-4789-0abc-def123456789",
                    "prompt": request.prompt,
                    "negative_prompt": "",
                    "seed": seed,
                    "mainCategory": "",
                    "subCategory": "",
                    "continueCreate": False,
                    "resolution": {
                        "width": request.width,
                        "height": request.height,
                        "batch_size": 4,
                    },
                    "batch_size": 4,
                    "steps": 0,
                    "cfg": 0,
                    "sampler_name": None,
                    "scheduler": None,
                    "multi_img2img_info": {"style_list": []},
                    "img_control_info": {"style_list": []},
                    "highPixels": False,
                    "model_ability": {"anime_style_control": None},
                    "denoise": 0,
                    "type": "image",
                }

            print(f"Creating generation task with payload: {generation_payload}")

            generation_response = await client.post(
                "https://api.piclumen.com/api/gen/create",
                headers=PICLUMEN_HEADERS,
                json=generation_payload,
            )
            generation_response.raise_for_status()
            generation_data = generation_response.json()

            print(f"Generation response: {generation_data}")

            if generation_data.get("status") != 0:
                raise HTTPException(
                    status_code=500,
                    detail=f"Generation request failed: {generation_data.get('message', 'Unknown error')}",
                )

            mark_id = generation_data.get("data", {}).get("markId")
            if not mark_id:
                raise HTTPException(
                    status_code=500,
                    detail=f"Could not extract markId from response: {generation_data}",
                )

            print(f"Got markId: {mark_id}")

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Generation request failed: {e.response.text}",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

        while True:
            try:
                await asyncio.sleep(5)

                status_response = await client.post(
                    "https://api.piclumen.com/api/task/batch-process-task",
                    headers=PICLUMEN_HEADERS,
                    json=[mark_id],
                )
                status_response.raise_for_status()

                try:
                    status_data = status_response.json()
                except json.JSONDecodeError:
                    print(
                        f"Non-JSON response received. Content: {status_response.text}"
                    )
                    continue

                print(f"Status response: {status_data}")

                if status_data.get("status") != 0:
                    print(f"Unexpected status code: {status_data}")
                    continue

                task_data_list = status_data.get("data", [])
                if not task_data_list or len(task_data_list) == 0:
                    print("No task data in response. Waiting...")
                    continue

                task_data = task_data_list[0]
                task_status = task_data.get("status")

                print(f"Current task status: {task_status}")

                if task_status == "success":
                    img_urls = task_data.get("img_urls")
                    if not img_urls or len(img_urls) == 0:
                        raise HTTPException(
                            status_code=500,
                            detail=f"No image URLs in completed response: {status_data}",
                        )

                    image_urls = [
                        img.get("imgUrl") for img in img_urls if img.get("imgUrl")
                    ]
                    if not image_urls:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Image URLs not found in response: {status_data}",
                        )

                    image_data_list = [ImageData(url=url) for url in image_urls]

                    return TextToImageResponse(
                        created=int(time.time()), data=image_data_list, task_id=mark_id
                    )

                elif task_status == "failed":
                    raise HTTPException(
                        status_code=400, detail="Image generation failed"
                    )

                elif task_status == "running":
                    print("Task still running. Waiting...")
                else:
                    print(f"Unknown status: {task_status}. Waiting...")

            except httpx.HTTPStatusError as e:
                print(f"Polling error: {e.response.text}")
                if e.response.status_code == 429:
                    await asyncio.sleep(20)
                    continue
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Polling failed: {e.response.text}",
                )


@app.post(
    "/v1/imagine-text-to-video/generations",
    response_model=ImagineTextToVideoResponse,
    tags=["Video Generation"],
    summary="Generate Video from Text using Imagine.art",
    description="""
    Generate a video from a text prompt using Imagine.art's text-to-video API.

    **Process:**
    1. Submit a text prompt describing the desired video
    2. The API creates a generation task with Imagine.art
    3. Automatically polls until the video is fully generated
    4. Returns the final video URL when ready

    **Parameters:**
    - `prompt`: Text description of the video (required)
    - `aspect_ratio`: Video aspect ratio (16:9, 9:16, 4:3, 1:1)
    - `duration`: Video duration in seconds (6 or 12)
    - `resolution`: Video resolution (720p or 1080p)
    - `style_id`: Style ID for video generation (default: 60503)
    - `is_enhance`: Enable prompt enhancement (default: True)

    **Model:** Imagine.art Text-to-Video (Seedance model)

    **Note:** The API automatically polls for completion (typically 1-3 minutes).
    The response includes the final video URL when generation is complete.
    """,
    responses={
        200: {
            "description": "Video generation task created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "85f8e695-38cc-4023-b15e-49313cadcbfc",
                        "status": "COMPLETED",
                        "video_url": "https://asset.imagine.art/processed/85f8e695-38cc-4023-b15e-49313cadcbfc",
                        "batch_id": "dde09073-c355-4443-aa80-0736d8358621",
                    }
                },
            },
        },
        400: {
            "description": "Invalid request or generation failed",
        },
        500: {
            "description": "Internal server error or upstream API error",
        },
    },
)
async def generate_imagine_text_to_video(request: ImagineTextToVideoRequest):
    import uuid

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            # Use fixed org_id and parent_id from the working account
            # These should be updated with your actual account IDs
            org_id = "425c7fab-779a-4d62-bd02-8c3c7064e229"
            parent_id = "3453d02d-025d-42e3-aacd-c7db2112b621"
            placeholder_uuid = str(uuid.uuid4())

            # Prepare the multipart form data
            form_data = {
                "style_id": str(request.style_id),
                "aspect_ratio": request.aspect_ratio,
                "variation": "text_to_video",
                "count": "1",
                "prompt": request.prompt,
                "is_enhance": "1" if request.is_enhance else "0",
                "enhancer_id": "seedance_t2v_prompt_enhancer",
                "duration": str(request.duration),
                "resolution": request.resolution,
                "clientVersion": "1",
                "parent_id": parent_id,
                "org_id": org_id,
                "metadata": json.dumps(
                    {
                        "placeholderUuid": placeholder_uuid,
                        "promptWithoutManipulation": request.prompt,
                        "modeId": 0,
                    }
                ),
                "use_plugin": "true",
            }

            print(f"Sending request to Imagine.art with data: {form_data}")

            # Prepare headers without content-type (let httpx set it with boundary)
            headers = {
                k: v for k, v in IMAGINE_HEADERS.items() if k.lower() != "content-type"
            }

            # Convert form_data to proper multipart format
            # For multipart/form-data in httpx, use files parameter with (None, value) tuples
            multipart_data = {key: (None, value) for key, value in form_data.items()}

            # Send the POST request as multipart/form-data
            generation_response = await client.post(
                "https://imagine.vyro.ai/v1/video/upload",
                headers=headers,
                files=multipart_data,
            )
            generation_response.raise_for_status()
            generation_data = generation_response.json()

            print(f"Generation response: {generation_data}")

            # Extract the response data
            if isinstance(generation_data, list) and len(generation_data) > 0:
                result = generation_data[0]
            else:
                result = generation_data

            # Ensure result is a dictionary
            if not isinstance(result, dict):
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected response format: {generation_data}",
                )

            video_id = result.get("id")
            batch_id = result.get("batchId")
            initial_status = result.get("status")

            if not video_id:
                raise HTTPException(
                    status_code=500,
                    detail=f"Could not extract video ID from response: {generation_data}",
                )

            print(f"Video ID: {video_id}, starting polling...")

            # Construct the actual video URL (processed, not thumbnails)
            video_url = f"https://asset.imagine.art/processed/{video_id}"

            # Step 2: Poll for video completion (like other endpoints)
            max_attempts = 30  # 30 attempts * 10 seconds = 5 minutes max
            attempt = 0

            while attempt < max_attempts:
                try:
                    attempt += 1
                    await asyncio.sleep(10)  # Wait 10 seconds between checks

                    print(
                        f"Polling attempt {attempt}/{max_attempts} for video: {video_url}"
                    )

                    # Check if video is accessible
                    check_response = await client.head(video_url, timeout=10)

                    if check_response.status_code == 200:
                        print(f"✅ Video is ready: {video_url}")
                        return ImagineTextToVideoResponse(
                            id=video_id,
                            status="COMPLETED",
                            video_url=video_url,
                            batch_id=batch_id or "",
                        )

                    print(f"Video not ready yet (Status: {check_response.status_code})")

                except httpx.HTTPStatusError as e:
                    print(f"Polling error: {e}")
                    if e.response.status_code == 429:
                        await asyncio.sleep(20)  # Rate limited, wait longer
                        continue
                except Exception as e:
                    print(f"Polling exception: {e}")
                    # Continue polling even on errors (video might still be processing)

            # Timeout reached but return URL anyway (might still be processing)
            print(f"⚠️ Timeout reached after {max_attempts} attempts, returning URL")
            return ImagineTextToVideoResponse(
                id=video_id,
                status="PROCESSING",
                video_url=video_url,
                batch_id=batch_id or "",
            )

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Generation request failed: {e.response.text}",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    # To use dark theme properly with swagger ui, we often rely on browser extensions or custom CSS injection.
    # Since I'm running backend code, I'll inject a dark theme CSS via the CDN in the HTML response above.
    # However, the standard swagger-ui.css is light.
    # I will update the CSS URL in get_swagger_ui_html to a dark theme.
    # A popular one is "Swagger UI Dark" or similar.
    # For now, I'll use a known trick: adding custom CSS.
    uvicorn.run(app, host="0.0.0.0", port=8000)
