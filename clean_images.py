import os
from typing import Any, Dict, List
from PIL import Image
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