import sys
sys.stdout.reconfigure(encoding='utf-8')

import argparse
import json
from paddleocr import PaddleOCR

import logging

# Disable PaddleOCR logs
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.basicConfig(level=logging.ERROR)


# Initialize PaddleOCR
paddle_ocr = PaddleOCR()

def ocr_paddleocr(image_path):
    """
    Perform OCR using PaddleOCR and return recognized text.
    """
    try:
        result = paddle_ocr.ocr(image_path)
        recognized_text = " ".join([line[1][0] for line in result[0]]) if result and result[0] else ""
        return {"engine": "PaddleOCR", "result": recognized_text, "error": None}
    except Exception as e:
        return {"engine": "PaddleOCR", "result": None, "error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PaddleOCR processing.")
    parser.add_argument("--image_path", type=str, required=True, help="Path to the image file.")
    args = parser.parse_args()

    if not args.image_path:
        print(json.dumps({"engine": "PaddleOCR", "result": None, "error": "No image path provided"}))
    else:
        result = ocr_paddleocr(args.image_path)
        print(json.dumps(result, ensure_ascii=False))
