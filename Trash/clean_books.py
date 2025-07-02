import os
from PyPDF2 import PdfReader, PdfWriter

def remove_pages_from_start(input_pdf_path, output_directory, pages_to_remove):
    os.makedirs(output_directory, exist_ok=True)
    filename = os.path.basename(input_pdf_path)
    output_pdf_path = os.path.join(output_directory, filename)
    with open(input_pdf_path, 'rb') as input_file:
        reader = PdfReader(input_file)
        writer = PdfWriter()
        total_pages = len(reader.pages)
        if pages_to_remove >= total_pages:
            raise ValueError(
                f"Cannot remove {pages_to_remove} pages from a PDF with only {total_pages} pages"
            )
        for page_num in range(pages_to_remove, total_pages):
            writer.add_page(reader.pages[page_num])
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)
    return output_pdf_path

def clean_books(input_dir, output_dir, leading_pages_map,):
    os.makedirs(output_dir, exist_ok=True)
    
    for filename, pages_to_remove in leading_pages_map.items():
        input_pdf_path = os.path.join(input_dir, filename)
        print(f"Processing {filename} to remove {pages_to_remove} leading pages...")
        try:
            remove_pages_from_start(input_pdf_path, output_dir, pages_to_remove)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    
    leading_pages_map = {
    'Grade_9_Biology.pdf' : 3,
    'Grade_9_Chemistry.pdf' : 2,
    }
    input_directory = "BooksPdfs"
    output_directory = "CleanedBooksPdfs"
    print("Starting to clean books...")
    clean_books(input_directory, output_directory, leading_pages_map)
    print("Books cleaned successfully.")