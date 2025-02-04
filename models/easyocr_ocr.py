import argparse
import json
import easyocr

# Initialize EasyOCR reader
easyocr_reader = easyocr.Reader(['en'], gpu=False)

def ocr_easyocr(image_path):
    """
    Perform OCR using EasyOCR.
    """
    result = easyocr_reader.readtext(image_path, detail=0)
    return " ".join(result) if result else ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EasyOCR processing.")
    parser.add_argument("--image_path", type=str, required=True, help="Path to the image file.")
    args = parser.parse_args()

    print(json.dumps({"engine": "EasyOCR", "result": ocr_easyocr(args.image_path), "error": None}))
