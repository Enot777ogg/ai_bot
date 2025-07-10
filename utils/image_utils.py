import base64
from PIL import Image
from io import BytesIO

def encode_image_to_base64(path: str) -> str:
    image = Image.open(path)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
