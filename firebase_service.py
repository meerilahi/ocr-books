from typing import List
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from book_model import BookModel, ChapterModel

class FirestoreCRUD:

    def __init__(self, cred_path: str = None):
        if not firebase_admin._apps:
            if cred_path:
                cred = credentials.Certificate(cred_path)
            else:
                cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.books_collection = "books"
        self.booksInfo_collection = "booksInfo"

    def add_book(self, book: BookModel) -> str:
        book_col_ref = self.db.collection(self.books_collection).document()
        book_col_ref.set(book.to_dict())
        bookInfo_col_ref = self.db.collection(self.booksInfo_collection).document()
        bookInfo_col_ref.set({
            'title' : book.title,
            'chapters' : {chapter.chapter_No : chapter.title for chapter in book.chapters }
        })
        return book_col_ref.id

    
    def add_chapter_to_book(self, book_id: str, chapter: ChapterModel) -> bool:
        book_ref = self.db.collection(self.books_collection).document(book_id)
        book_data = book_ref.get().to_dict()    
        if not book_data:
            return False
        book = BookModel.from_dict(book_data)
        book.chapters.append(chapter)
        book_ref.update({'chapters': [ch.to_dict() for ch in book.chapters]})
        return True

    def get_book(self, book_id: str) -> BookModel:
        doc_ref = self.db.collection(self.books_collection).document(book_id)
        doc = doc_ref.get()
        if doc.exists:
            return BookModel.from_dict(doc.to_dict())
        return None

    def get_all_books(self) -> List[BookModel]:
        docs = self.db.collection(self.books_collection).stream()
        return [BookModel.from_dict(doc.to_dict()) for doc in docs]

    def get_books_by_title(self, title: str) -> List[BookModel]:
        docs = self.db.collection(self.books_collection)\
                      .where(filter=FieldFilter('title', '>=', title))\
                      .where(filter=FieldFilter('title', '<=', title + '\uf8ff'))\
                      .stream()
        return [BookModel.from_dict(doc.to_dict()) for doc in docs]

    def get_chapter(self, book_id: str, chapter_no: int) -> ChapterModel:
        book = self.get_book(book_id)
        if book and book.chapters:
            for chapter in book.chapters:
                if chapter.chapter_No == chapter_no:
                    return chapter
        return None

    def update_book_title(self, book_id: str, new_title: str) -> bool:
        book_ref = self.db.collection(self.books_collection).document(book_id)
        book_ref.update({'title': new_title})
        return True

    def update_chapter(self, book_id: str, chapter_no: int, new_chapter: ChapterModel) -> bool:
        if new_chapter.chapter_No != chapter_no:
            return False
        book_ref = self.db.collection(self.books_collection).document(book_id)
        book_data = book_ref.get().to_dict()
        if not book_data:
            return False
        book = BookModel.from_dict(book_data)
        updated = False
        for i, chapter in enumerate(book.chapters):
            if chapter.chapter_No == chapter_no:
                book.chapters[i] = new_chapter
                updated = True
                break
        if updated:
            book_ref.update({'chapters': [ch.to_dict() for ch in book.chapters]})
            return True
        return False

    def delete_book(self, book_id: str) -> bool:
        self.db.collection(self.books_collection).document(book_id).delete()
        return True

    def delete_chapter(self, book_id: str, chapter_no: int) -> bool:
        book_ref = self.db.collection(self.books_collection).document(book_id)
        book_data = book_ref.get().to_dict()
        if not book_data:
            return False
        book = BookModel.from_dict(book_data)
        original_length = len(book.chapters)
        book.chapters = [ch for ch in book.chapters if ch.chapter_No != chapter_no]
        if len(book.chapters) < original_length:
            book_ref.update({'chapters': [ch.to_dict() for ch in book.chapters]})
            return True
        return False


if __name__ == "__main__":
    # Initialize with your Firebase credentials file
    crud = FirestoreCRUD(".firebase_credentials.json")
    
    # Create a book with chapters
    book = BookModel(
        title="Python Programming",
        chapters=[
            ChapterModel(1, "Introduction", "Welcome to Python programming..."),
            ChapterModel(2, "Variables", "Variables are used to store data...")
        ]
    )
    
    # Add book to Firestore - now returns just the ID string
    book_id = crud.add_book(book)
    print(f"Book added with ID: {book_id}")
    
    # Add a new chapter - now book_id is a string
    new_chapter = ChapterModel(3, "Functions", "Functions are reusable blocks of code...")
    success = crud.add_chapter_to_book(book_id, new_chapter)
    print(f"Chapter added successfully: {success}")
    
    # Get the book
    retrieved_book = crud.get_book(book_id)
    print(f"Retrieved book: {retrieved_book.title}")
    print(f"Chapters: {[ch.title for ch in retrieved_book.chapters]}")
    
    # Update a chapter
    updated_chapter = ChapterModel(2, "Variables and Data Types", "Updated content...")
    crud.update_chapter(book_id, 2, updated_chapter)
    
    # Get a specific chapter
    chapter = crud.get_chapter(book_id, 2)
    print(f"Chapter 2 title: {chapter.title}")
    
    # Delete a chapter
    crud.delete_chapter(book_id, 1)
    
    # Delete the book
    crud.delete_book(book_id)