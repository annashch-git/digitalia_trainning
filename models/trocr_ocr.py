import sys
sys.stdout.reconfigure(encoding='utf-8')

import argparse
import json
from transformers import VisionEncoderDecoderModel, TrOCRProcessor, AutoProcessor
from PIL import Image

# Load your specific TrOCR model
torch_processor = AutoProcessor.from_pretrained(r"D:\XAMK\Internship\Trainnig_rep\digitalia_trainning\models\multicentury-htr-model")
torch_model = VisionEncoderDecoderModel.from_pretrained(r"D:\XAMK\Internship\Trainnig_rep\digitalia_trainning\models\multicentury-htr-model")


def ocr_trocr(image_path):
    """
    Perform OCR using your specific TrOCR model (Kansallisarkisto/multicentury-htr-model).
    """
    image = Image.open(image_path).convert("RGB")
    inputs = torch_processor(images=image, return_tensors="pt")
    outputs = torch_model.generate(**inputs)
    result = torch_processor.batch_decode(outputs, skip_special_tokens=True)
    return result[0] if result else ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TrOCR processing with Kansallisarkisto/multicentury-htr-model.")
    parser.add_argument("--image_path", type=str, required=True, help="Path to the image file.")
    args = parser.parse_args()

    print(json.dumps({"engine": "TrOCR (Kansallisarkisto)", "result": ocr_trocr(args.image_path), "error": None}))
