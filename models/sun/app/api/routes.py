# from fastapi import APIRouter, UploadFile, File
# from fastapi.responses import StreamingResponse
# from PIL import Image
#
# import io
# from typing import List, AsyncGenerator
# import numpy as np
#
# from app.saliency.saliency import make_saliency_map
#
# router = APIRouter()
#
# async def read_image(image_file: UploadFile) -> np.ndarray:
#     image_bytes = await image_file.read()
#     image = Image.open(io.BytesIO(image_bytes))
#
#     return np.array(image)
#
#
# @router.post("/process")
# async def process_images(image_files: List[UploadFile] = File(...)):
#     async def image_generator() -> AsyncGenerator[bytes, None]:
#         for input_image_file in image_files:
#             input_image = await read_image(input_image_file)
#             saliency_map = make_saliency_map(input_image)
#
#             img_io = io.BytesIO()
#             Image.fromarray(saliency_map).save(img_io, format="PNG")
#             img_io.seek(0)
#
#             yield img_io.getvalue()
#
#     return StreamingResponse(image_generator(), media_type="application/octet-stream")
#
# @router.get("/hello")
# def hello():
#     return { "hello": "world" }
#
import io
from typing import List, AsyncGenerator
import numpy as np
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image

from app.saliency.saliency import make_saliency_map

router = APIRouter()


async def load_image(image_file: UploadFile) -> tuple[np.ndarray, str]:
    """Safely load an image from an UploadFile and return the image array and filename."""
    # Read all content at once to avoid problems with closed files later
    content = await image_file.read()
    image = Image.open(io.BytesIO(content))
    return np.array(image), image_file.filename


async def process_image(image_array: np.ndarray) -> bytes:
    """Process an image array and return the processed image as bytes."""
    saliency_map = make_saliency_map(image_array)

    img_io = io.BytesIO()
    Image.fromarray(saliency_map).save(img_io, format="PNG")
    img_io.seek(0)

    return img_io.getvalue()


@router.post("/process")
async def process_images(image_files: List[UploadFile] = File(...)) -> StreamingResponse:
    # Load all images upfront to avoid closed file issues
    image_data = []
    for image_file in image_files:
        try:
            image_array, filename = await load_image(image_file)
            image_data.append((image_array, filename))
        except Exception as e:
            # Handle errors for individual files
            print(f"Error loading image {image_file.filename}: {str(e)}")

    async def image_generator() -> AsyncGenerator[bytes, None]:
        for image_array, _ in image_data:
            processed_image = await process_image(image_array)
            yield processed_image

    return StreamingResponse(
        image_generator(),
        media_type="application/octet-stream"
    )


@router.get("/hello")
def hello():
    return {"hello": "world"}
