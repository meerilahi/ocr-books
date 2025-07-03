import json
import os
from typing import Any, Dict
from clean_images import clean_images
from ocr_images import ocr_images
from save_book_to_firebase import save_book_to_firebase

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
        
        print(f"    Writing OCR text to disk for chapter: {chapterNo}")
        output_path = os.path.join(output_dir, book_info['name'], f"{chapterNo}.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ocr_text)
    
    print(f"    Saving Book to Firebase: {book_info['name']}")
    save_book_to_firebase(output_dir, book_info)
    

    

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