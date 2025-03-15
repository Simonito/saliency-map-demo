from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import aiohttp
import os

router = APIRouter()

SUN_MODEL_URL = os.getenv("SUN_MODEL_URL", "http://localhost:8081")


@router.post("/generate-saliency/")
async def generate_saliency(images: list[UploadFile] = File(...)):
    """
    Upload an image and get back the generated saliency map, streamed.
    """
    form_data = aiohttp.FormData()

    for img in images:
        form_data.add_field(
            "image_files",
            await img.read(),
            filename=img.filename,
            content_type=img.content_type
        )

    async def stream_response():
        async with aiohttp.ClientSession() as session:
            async with session.post(SUN_MODEL_URL + "/process", data=form_data) as response:

                if response.status != 200:
                    raise HTTPException(status_code=500, detail="Saliency model processing failed.")

                buffer = b""
                try:
                    async for data, end_of_http_chunk in response.content.iter_chunks():
                        buffer += data
                        if end_of_http_chunk:
                            yield buffer
                            buffer = b""
                except aiohttp.ClientConnectionError as e:
                    print(f"Downstream connection closed unexpectedly | {e}")
                except Exception as e:
                    print(f"Exception while streaming response | {e}")

    return StreamingResponse(stream_response(), media_type="application/octet-stream")


@router.get("/hello")
def hello():
    return {"serus": "svet"}
