# OCR-Books (KPK Textbook OCR Tool)

This repository contains scripts and tools for performing OCR (Optical Character Recognition) on all KPK board textbooks. It is used to extract clean, structured text from scanned book PDFs to enable further NLP or educational AI applications.

## Features
- ✅ OCR for scanned KPK textbooks
- ✅ Extracts structured text chapter-wise
- ✅ Supports preprocessing to improve OCR accuracy
- ✅ Outputs text in clean, readable format
- ✅ Can be used as a standalone script or integrated into other systems (e.g., TestPilot)

## Tech Stack
- Python
- Tesseract OCR
- PDF Processing: PyMuPDF (fitz), pdf2image
- Image Preprocessing: OpenCV, PIL

## Supported Languages
- English
- Urdu *(partial, depends on trained data availability)*



## How to Use
```bash
# Step 1: Install requirements
pip install -r requirements.txt

# Step 2: Run OCR on a book PDF
python main.py --input data/book.pdf --output output/book.txt
```

## Output Format
- Plain `.txt` files for each book
- Each chapter separated and optionally cleaned
- Ready for further NLP or educational use

## Status
Actively used as an internal tool for educational data extraction. Can be extended for Urdu/Pashto OCR with better Tesseract training data.

## License
MIT License