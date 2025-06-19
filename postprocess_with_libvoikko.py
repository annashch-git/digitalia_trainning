import libvoikko
import sys
import os
import re
import jiwer

def preprocess_text(text):
    """
    Normalize text: lowercase, remove excess whitespace, standardize line breaks.
    """
    text = text.lower()
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def read_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def calculate_wer_cer(ground_truth_text, ocr_result_text):
    """Calculates WER and CER between ground truth and OCR output."""
    wer = jiwer.wer(ground_truth_text, ocr_result_text)
    cer = jiwer.cer(ground_truth_text, ocr_result_text)
    return wer, cer

def postprocess_ocr_file(input_path, output_path_base):
    # Read OCR result from file
    ocr_text = read_text(input_path)
    preprocessed_text = preprocess_text(ocr_text)
    
    os.add_dll_directory(r"C:\Voikko")
    v = libvoikko.Voikko("fi")
    
    words = preprocessed_text.split()
    corrected_tokens = []
    for word in words:
        if not word.isalpha():
            corrected_tokens.append(word)
            continue
        if v.spell(word):
            corrected_tokens.append(word)
        else:
            suggestions = v.suggest(word)
            if suggestions:
                corrected_tokens.append(suggestions[0])
            else:
                corrected_tokens.append(word)
    corrected_text = " ".join(corrected_tokens)
    corrected_text = re.sub(r'\s([?.!,;:])', r'\1', corrected_text)
    
    with open(f"{output_path_base}__Libvoikko.txt", "w", encoding="utf-8") as f:
        f.write(corrected_text)
    
    v.terminate()
    return corrected_text

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python postprocess_with_libvoikko.py <ground_truth.txt> <input_ocr_result.txt>")
        sys.exit(1)
    
    ground_truth_path = sys.argv[1]
    input_path = sys.argv[2]
    
    # Output file naming
    file_dir = os.path.dirname(input_path)
    file_name = os.path.basename(input_path)
    name, ext = os.path.splitext(file_name)
    output_path_base = os.path.join(file_dir, name)
    
    # Normalize and save ground truth
    ground_truth_text_raw = read_text(ground_truth_path)
    ground_truth_text = preprocess_text(ground_truth_text_raw)
    gt_norm_filename = os.path.splitext(os.path.basename(ground_truth_path))[0] + "_normalized.txt"
    gt_norm_path = os.path.join(os.path.dirname(ground_truth_path), gt_norm_filename)
    with open(gt_norm_path, "w", encoding="utf-8") as f:
        f.write(ground_truth_text)
    print(f"Normalized ground truth saved as {gt_norm_path}")
    
    postprocessed_text = postprocess_ocr_file(input_path, output_path_base)
    print(f"Postprocessed file saved as {output_path_base}__Libvoikko.txt")
    
    # WER/CER
    wer, cer = calculate_wer_cer(ground_truth_text, postprocessed_text)
    print(f"WER: {wer:.4f}")
    print(f"CER: {cer:.4f}")
