import sys
import io
import json
import os
import ollama
import argparse

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def load_image(image_path):
    """Load image as binary data."""
    with open(image_path, "rb") as f:
        return f.read()

def recognize_text(image_path):
    """Recognize text from an image using Ollama OCR."""
    image_data = load_image(image_path)

    # Sending the image to Ollama OCR
    response = ollama.chat(
        model="llava",
        messages=[{
            "role": "user",
            "content": "Extract only the text from the image. Do not add any explanations, quotation marks, brackets, or extra words. Output only the raw text exactly as it appears. If you can't recognize the text, leave the output blank.",
            "images": [image_data],
        }]
    )

    text_result = response.get("message", {}).get("content", "")
    return {"engine": "Ollama", "result": text_result, "error": None}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ollama OCR processing.")
    parser.add_argument("--image_path", type=str, required=True, help="Path to the image file.")
    args = parser.parse_args()

    if not args.image_path:
        print(json.dumps({"engine": "Ollama", "result": None, "error": "No image path provided"}))
    else:
        result = recognize_text(args.image_path)
        print(json.dumps(result, ensure_ascii=False))
