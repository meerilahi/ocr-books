import os
from typing import Any, Dict
from book_model import BookModel, ChapterModel
from firebase_service import FirestoreCRUD

def save_book_to_firebase(input_dir: str, book_info: Dict[str, Any]):
    crud = FirestoreCRUD(".firebase_credentials.json")
    chapters = []
    for chapterNo, chapter in book_info['chapters'].items():
        chapter_path = os.path.join(input_dir, book_info['name'], f"{chapterNo}.md")
        if os.path.exists(chapter_path):
            with open(chapter_path, 'r', encoding='utf-8') as f:
                content = f.read()
            chapters.append(ChapterModel(chapterNo, chapter['chapterTitle'], content))
        else:
            print(f"Chapter file not found: {chapter_path}")
    book = BookModel(
        title=book_info['name'],
        chapters=chapters
    )
    crud.add_book(book)