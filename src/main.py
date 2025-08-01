from fastapi import FastAPI
from fastapi.responses import Response
from src.models import SlideRequest
from src.image_generator import generate_slide_image
import json

app = FastAPI()


@app.post("/generate")
async def generate_slide(request: SlideRequest):
    image_bytes = generate_slide_image(request)
    return Response(content=image_bytes, media_type="image/png")


@app.get("/.well-known/schemas/slide-generator.json")
async def get_schema():
    schema = SlideRequest.model_json_schema()
    return schema


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)