# 

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import argparse
import subprocess
import json
import os
import sys
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Dictionary mapping OCR models to their virtual environments and scripts
MODELS = {
    "tesseract": {"env": ".venv", "script": "models/tesseract_ocr.py"},
    "trocr": {"env": ".venv", "script": "models/trocr_ocr.py"},
    "easyocr": {"env": ".venv", "script": "models/easyocr_ocr.py"},
    "paddleocr": {"env": ".venv", "script": "models/paddleocr_ocr.py"},
}

def extract_json_from_output(output: str) -> dict:
    """
    Extract a valid JSON object from mixed stdout output.
    
    Args:
        output: The stdout output from the subprocess.
        
    Returns:
        A dictionary with the parsed JSON data or an error message.
    """
    json_start = output.find("{")
    json_end = output.rfind("}")
    
    if json_start != -1 and json_end != -1:
        json_str = output[json_start:json_end + 1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logging.error("JSON decoding error: %s", e)
            return {"error": "Failed to parse JSON from output"}
    logging.error("Could not extract JSON from output.")
    return {"error": "JSON not found in output"}

def run_ocr_model(model_name: str, image_path: str) -> dict:
    """
    Run the selected OCR model inside its corresponding virtual environment.
    
    Args:
        model_name: The name of the OCR model.
        image_path: The path to the image file.
        
    Returns:
        A dictionary containing the model's output or an error message.
    """
    if model_name not in MODELS:
        logging.error("Unknown model '%s'. Available models: %s", model_name, ", ".join(MODELS.keys()))
        sys.exit(1)

    env_path = MODELS[model_name]["env"]
    script_path = MODELS[model_name]["script"]

    # Build the path to the Python executable within the virtual environment
    if os.name == "nt":
        python_executable = os.path.join(env_path, "Scripts", "python.exe")
    else:
        python_executable = os.path.join(env_path, "bin", "python")
    
    # Construct the command to run the script
    command = [python_executable, script_path, "--image_path", image_path]
    logging.debug("Executing command: %s", " ".join(command))

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        if result.returncode != 0:
            logging.error("Script exited with code %d", result.returncode)
            logging.error("stderr: %s", result.stderr)
            return {"error": f"Script exited with code {result.returncode}", "stderr": result.stderr}
        logging.debug("OCR output: %s", result.stdout)
        return extract_json_from_output(result.stdout)

    except Exception as e:
        logging.error("Error executing command: %s", e)
        logging.error("Traceback:\n%s", traceback.format_exc())  # Вывод полного стека ошибки
        return {"error": str(e)}

def save_results_to_file(image_path: str, model_name: str, ocr_result: dict):
    """
    Save the OCR result to a text file in the same directory as the image.
    
    Args:
        image_path: The path to the image file.
        model_name: The name of the OCR model.
        ocr_result: The result of the OCR processing.
    """
    # Extract the directory and filename of the image
    image_dir = os.path.dirname(image_path)
    image_filename = os.path.basename(image_path)
    
    # Create the output file name
    output_filename = f"{os.path.splitext(image_filename)[0]}_{model_name}.txt"
    output_path = os.path.join(image_dir, output_filename)
    
    # Extract the OCR text from the result (assuming it is in a 'text' field)
    ocr_text = ocr_result.get("result", "")
    
    # Write the result to the file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ocr_text)
        logging.info("OCR result saved to: %s", output_path)
    except Exception as e:
        logging.error("Error saving OCR result to file: %s", e)

def main():
    parser = argparse.ArgumentParser(description="Run OCR models on an image and save results.")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug output.")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not os.path.exists(args.image_path):
        logging.error("Image not found: %s", args.image_path)
        sys.exit(1)

    for model_name in MODELS.keys():
        result = run_ocr_model(model_name, args.image_path)
        save_results_to_file(args.image_path, model_name, result)

if __name__ == "__main__":
    main()
