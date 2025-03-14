from fastapi import APIRouter, UploadFile, File, HTTPException
import httpx

router = APIRouter()

@router.post("/generate-saliency/")
async def generate_saliency(image: UploadFile = File(...)):
    """
    Upload an image and get back the generated saliency map.
    """
    image_bytes = await image.read()
    model_url = "http://model1.knative.local/generate"

    async with httpx.AsyncClient() as client:
        response = await client.post(model_url, files={"file": image_bytes})

    if response.status_code == 200:
        return {"message": "Saliency map generated!", "saliency_map": response.json()}
    else:
        raise HTTPException(status_code=500, detail="Model processing failed.")
