import os
from pdf2image import convert_from_path
from PIL import Image
from fpdf import FPDF
import tempfile

def bisect_pdf_vertically(pdf_path, output_pdf_path, language='English', start_page=0):
    
    pages = convert_from_path(pdf_path)
    all_bisected_images = []

    for idx, page in enumerate(pages):
        if idx < start_page:
            all_bisected_images.append(page)
            continue
        width, height = page.size
        left_box = (0, 0, width // 2, height)
        right_box = (width // 2, 0, width, height)
        left_image = page.crop(left_box)
        right_image = page.crop(right_box)
        if language == 'English':
            all_bisected_images.extend([left_image, right_image])
        else:
            all_bisected_images.extend([right_image, left_image])
    pdf = FPDF(unit='pt')
    for idx, img in enumerate(all_bisected_images):
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_img:
            img_path = temp_img.name
            img.save(img_path, 'JPEG')
        width, height = img.size
        pdf.add_page(format=(width, height))
        pdf.image(img_path, 0, 0, width, height)
        os.remove(img_path)
    pdf.output(output_pdf_path)

if __name__ == "__main__":
    input_pdf = "BooksPdfs/Grade_9_Biology.pdf"
    output_pdf = "output_bisected.pdf"
    language = "English"
    
    bisect_pdf_vertically(input_pdf, output_pdf, language, start_page=2)