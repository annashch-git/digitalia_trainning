import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import ollama
import os


def load_image(image_path):
    """Load image as binary data."""
    with open(image_path, "rb") as f:
        return f.read()

def recognize_text(image_path):
    """Recognize text from an image using Ollama OCR and save the result to a file."""
    image_data = load_image(image_path)
    
    # Sending the image to Ollama OCR
    response = ollama.chat(
        model="llava",
        messages=[
            {
                "role": "user",
                "content": "Extract only the text from the image. Do not add any explanations, quotation marks, brackets, or extra words. Output only the raw text exactly as it appears. If you can't recognize the text, leave the output blank.",
                "images": [image_data],
            }
        ]
    )
    
    text_result = response.get("message", {}).get("content", "The text is not found.")
    
    # Generate output filename
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_file = os.path.join(os.path.dirname(image_path), f"{base_name}_ollamaocr.txt")
    
    # Save result to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text_result.strip())
    
    print(f"OCR result saved to: {output_file}")
    return output_file

# Usage example
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    recognize_text(image_path)