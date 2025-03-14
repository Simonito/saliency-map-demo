from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Saliency Map API",
    description="An API for generating saliency maps from images.",
    version="1.0.0",
)

app.include_router(router)

