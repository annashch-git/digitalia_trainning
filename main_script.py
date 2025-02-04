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
    "keras": {"env": "keras_env", "script": "models/keras_model.py"},
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
        result = subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        logging.error("Error executing command: %s", e)
        return {"error": str(e)}

    logging.debug("stdout: %s", result.stdout)
    logging.debug("stderr: %s", result.stderr)

    if result.returncode != 0:
        logging.error("Script exited with code %d", result.returncode)
        return {"error": f"Script exited with code {result.returncode}", "stderr": result.stderr}

    return extract_json_from_output(result.stdout)

def main():
    parser = argparse.ArgumentParser(description="Run a selected OCR model on an image.")
    parser.add_argument("model", type=str, help=f"OCR model name ({', '.join(MODELS.keys())}).")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug output.")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not os.path.exists(args.image_path):
        logging.error("Image not found: %s", args.image_path)
        sys.exit(1)

    result = run_ocr_model(args.model, args.image_path)
    print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
