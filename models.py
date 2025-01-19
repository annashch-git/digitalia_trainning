import argparse
from transformers import VisionEncoderDecoderModel, AutoProcessor
from paddleocr import PaddleOCR
import easyocr
import pytesseract
from PIL import Image
import os

import logging
from transformers import logging as transformers_logging
logging.getLogger("easyocr").setLevel(logging.ERROR)
logging.getLogger("ppocr").setLevel(logging.ERROR)
transformers_logging.set_verbosity_error()
logging.basicConfig(level=logging.ERROR)


# Initialize Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  

# Initialize TrOCR
torch_processor = AutoProcessor.from_pretrained(r"D:\XAMK\Internship\Trainnig_rep\digitalia_trainning\multicentury-htr-model")
torch_model = VisionEncoderDecoderModel.from_pretrained(r"D:\XAMK\Internship\Trainnig_rep\digitalia_trainning\multicentury-htr-model")

# Initialize EasyOCR
easyocr_reader = easyocr.Reader(['en'], gpu=False)

# Initialize PaddleOCR
paddle_ocr = PaddleOCR()

# Function for Tesseract OCR
def ocr_tesseract(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

# Function for TrOCR
def ocr_trocr(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = torch_processor(images=image, return_tensors="pt")
    outputs = torch_model.generate(**inputs)
    result = torch_processor.batch_decode(outputs, skip_special_tokens=True)
    return result

# Function for EasyOCR
def ocr_easyocr(image_path):
    return easyocr_reader.readtext(image_path, detail=0)

# Function for PaddleOCR
def ocr_paddleocr(image_path):
    result = paddle_ocr.ocr(image_path)
    return [line[1][0] for line in result[0]]

# Run all OCR engines
def run_all_ocr_engines(image_path):
    print("Tesseract OCR Result:")
    print(ocr_tesseract(image_path))

    print("\nTrOCR Result:")
    print(ocr_trocr(image_path))

    print("\nEasyOCR Result:")
    print(ocr_easyocr(image_path))

    print("\nPaddleOCR Result:")
    print(ocr_paddleocr(image_path))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OCR on an image using multiple engines.")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    args = parser.parse_args()

    if not os.path.exists(args.image_path):
        print(f"Image not found: {args.image_path}")
    else:
        run_all_ocr_engines(args.image_path)
