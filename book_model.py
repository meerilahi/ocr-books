from typing import List

class ChapterModel:
    
    def __init__(self, chapter_No: int, title: str, content: str):
        self.chapter_No = chapter_No
        self.title = title
        self.content = content

    def to_dict(self):
        return {
            'chapter_No': self.chapter_No,
            'title': self.title,
            'content': self.content
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            chapter_No=data.get('chapter_No'),
            title=data.get('title'),
            content=data.get('content')
        )

class BookModel:
    
    def __init__(self, title: str, chapters: List[ChapterModel] = None):
        self.title = title
        self.chapters = chapters if chapters is not None else []

    def to_dict(self):
        return {
            'title': self.title,
            'chapters': [chapter.to_dict() for chapter in self.chapters]
        }

    @classmethod
    def from_dict(cls, data: dict):
        chapters = [ChapterModel.from_dict(chapter) for chapter in data.get('chapters', [])]
        return cls(
            title=data.get('title'),
            chapters=chapters
        )