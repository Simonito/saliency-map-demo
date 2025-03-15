import io
from typing import List, Generator
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


def process_image(image_array: np.ndarray) -> bytes:
    """Process an image array and return the processed image as bytes."""
    saliency_map = make_saliency_map(image_array)

    img_io = io.BytesIO()
    Image.fromarray(saliency_map).save(img_io, format="PNG")
    img_io.seek(0)

    return img_io.getvalue()


@router.post("/process")
async def process_images(image_files: List[UploadFile] = File(...)) -> StreamingResponse:
    # Load all images upfront to avoid closed file issues
    print(f"Model received {len(image_files)} files")
    image_data = []
    for image_file in image_files:
        try:
            image_array, filename = await load_image(image_file)
            image_data.append((image_array, filename))
        except Exception as e:
            # Handle errors for individual files
            print(f"Error loading image {image_file.filename}: {str(e)}")

    def image_generator() -> Generator[bytes, None]:
        img_count = 0
        for img_array, fname in image_data:
            img_count += 1
            print(f"Processing image #{img_count}: {fname}")

            try:
                processed_image = process_image(img_array)
                if not processed_image:
                    print(f"⚠️ Warning: Processed image #{img_count} is empty!")
                    continue

                print(f"✅ Generated processed image #{img_count}, size: {len(processed_image)} bytes")
                yield processed_image
            except Exception as e:
                print(f"❌ Error processing image {fname}: {e}")
                continue
        print(f"🎯 Total images processed: {img_count}")

    return StreamingResponse(
        image_generator(),
        media_type="application/octet-stream"
    )


@router.get("/hello")
def hello():
    return {"hello": "world"}
