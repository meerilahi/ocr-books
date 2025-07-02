import base64
import json
import os
from mistralai import ImageURLChunk
from mistralai import Mistral
from pdf2image import convert_from_path
from io import BytesIO

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def ocr_images(image_bytes_list):
    markdowns = []
    for image_bytes in image_bytes_list:
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        base64_data_url = f"data:image/jpeg;base64,{image_base64}"
        response_json = client.ocr.process(document=ImageURLChunk(image_url=base64_data_url), model="mistral-ocr-latest").model_dump()
        markdowns.append(response_json['pages'][0]['markdown'])
    return '\n'.join(markdowns)

def process_book(input_path, chapters_map, output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for chapterNo, range in chapters_map.items():
        
        print(f"   Processing chapter no : {chapterNo}")
        image_bytes_list = []
        images = convert_from_path(input_path, dpi=300, first_page=range['start_page'], last_page=range['end_page'])
        for img in images:
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='JPEG')
            image_bytes_list.append(img_byte_arr.getvalue())
        

        ocr_result = ocr_images(image_bytes_list)
        output_file = os.path.join(output_dir, f"{chapterNo}.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(ocr_result))
        
def process_books(input_dir, chapters_mappings_path, output_dir):
    print("OCRBooks Started")
    maps = json.load(open(chapters_mappings_path, 'r', encoding='utf-8'))
    for bookName, chapters_map in maps.items():
        input_path = f"{input_dir}/{bookName}.pdf"
        output_dir = f"{output_dir}/{bookName}"
        print(f"\nProcessing book: {bookName}")
        process_book(input_path, chapters_map, output_dir)
        print("-" * 50)
    print("OCRBooks Started")

if __name__ == "__main__":
    process_books("BooksPdfs", "BooksChaptersMappings.json", "BooksMarkdowns")
