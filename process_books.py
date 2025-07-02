import base64
from io import BytesIO
import json
import os
from typing import Any, Dict, List
from PIL import Image
from fpdf import FPDF
from mistralai import ImageURLChunk, Mistral
from pdf2image import convert_from_path


def clean_images(book_info:Dict[str,Any], input_dir:str) -> Dict[str, List[Image.Image]]:
    
    pdf_path = os.path.join(input_dir, book_info['name']+".pdf")
    pages = convert_from_path(pdf_path)

    if book_info['bisect'] == 'none':
        all_bisected_images = pages
    else:
        all_bisected_images = []
        for idx, page in enumerate(pages):
            width, height = page.size
            left_box = (0, 0, width // 2, height)
            right_box = (width // 2, 0, width, height)
            left_image = page.crop(left_box)
            right_image = page.crop(right_box)
            if book_info["bisect"] == 'left':
                all_bisected_images.extend([left_image, right_image])
            else:
                all_bisected_images.extend([right_image, left_image])
                
    all_bisected_images = all_bisected_images[book_info['leading_pages']:]

    images_dict = {}
    for chapterNo, info in book_info['chapters'].items():
        start_page = info['start_page']
        end_page = info['end_page']
        images_dict[chapterNo] = all_bisected_images[start_page+1:end_page+1]
    
    return images_dict

def ocr_images(images: List[Image.Image]) -> str:

    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    image_bytes_list = []
    for img in images:
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='JPEG')
            image_bytes_list.append(img_byte_arr.getvalue())
    
    markdowns = []
    for image_bytes in image_bytes_list:
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        base64_data_url = f"data:image/jpeg;base64,{image_base64}"
        response_json = client.ocr.process(document=ImageURLChunk(image_url=base64_data_url), model="mistral-ocr-latest").model_dump()
        markdowns.append(response_json['pages'][0]['markdown'])

    return '\n'.join(markdowns)

def process_book(book_info:Dict[str, Any] , input_dir:str , output_dir:str) -> None:
    print(f"Processing book: {book_info['name']}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(os.path.join(output_dir, book_info['name'])):
        os.makedirs(os.path.join(output_dir, book_info['name']))

    print("    Cleaning images...")
    images_dict = clean_images(book_info, input_dir)

    for chapterNo, images in images_dict.items():
        
        print(f"    Performing OCR on chapter: {chapterNo}")
        ocr_text = ocr_images(images)
        
        print(f"    Saving OCR text for chapter: {chapterNo}")
        output_path = os.path.join(output_dir, book_info['name'], f"{chapterNo}_ocr.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ocr_text)

def process_books(input_dir:str, output_dir:str, books_info_path:Dict[str, Any]) -> None:
    print("Processing books...")
    books_info = json.load(open(books_info_path, 'r'))
    for _, book_info in books_info.items():
        process_book(book_info, input_dir, output_dir)
    print("Processing completed.")

if __name__ == "__main__":
    
    input_dir = "input_books"
    output_dir = "output_books"
    books_info_path = "books_info.json"

    process_books(input_dir, output_dir, books_info_path)