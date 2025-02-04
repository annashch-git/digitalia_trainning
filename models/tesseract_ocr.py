import argparse
import json
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def ocr_tesseract(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tesseract OCR processing.")
    parser.add_argument("--image_path", type=str, required=True, help="Path to the image file.")
    args = parser.parse_args()

    if not args.image_path:
        print(json.dumps({"engine": "Tesseract", "error": "No image path provided"}))
    else:
        print(json.dumps({"engine": "Tesseract", "result": ocr_tesseract(args.image_path), "error": None}))
