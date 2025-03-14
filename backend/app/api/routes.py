from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import os
import io

router = APIRouter()

SUN_MODEL_URL = os.getenv("SUN_MODEL_URL", "http://localhost:8081")


@router.post("/generate-saliency/")
async def generate_saliency(images: list[UploadFile] = File(...)):
    """
    Upload an image and get back the generated saliency map, streamed.
    """
    async with httpx.AsyncClient() as client:
        files = [("image_files", (img.filename, await img.read(), img.content_type)) for img in images]

        response = await client.post(SUN_MODEL_URL + "/process", files=files)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Saliency model processing failed.")

        async def stream_response():
            async for chunk in response.aiter_bytes():
                print('streaming chunk')
                yield chunk  # Stream the response chunk by chunk

        return StreamingResponse(stream_response(), media_type="application/octet-stream")


@router.get("/hello")
def hello():
    return {"serus": "svet"}
