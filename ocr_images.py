import base64
from io import BytesIO
import os
from typing import List
from PIL import Image
from mistralai import ImageURLChunk, Mistral
import dotenv

dotenv.load_dotenv()

def ocr_images(images: List[Image.Image]) -> str:

    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    image_bytes_list = []
    for img in images:
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='JPEG')
            image_bytes_list.append(img_byte_arr.getvalue())
    
    markdowns = []
    for index , image_bytes in enumerate(image_bytes_list):
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        base64_data_url = f"data:image/jpeg;base64,{image_base64}"
        response_json = client.ocr.process(document=ImageURLChunk(image_url=base64_data_url), model="mistral-ocr-latest").model_dump()
        markdowns.append(response_json['pages'][0]['markdown'])

    return '\n'.join(markdowns)
