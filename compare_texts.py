import sys
import subprocess
import jiwer

def read_text(file_path):
    """Reads text from a file and returns it as a string."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()

def calculate_wer_cer(ground_truth_path, ocr_result_path):
    """Calculates WER and CER between ground truth and OCR output."""
    # Read texts from files
    ground_truth = read_text(ground_truth_path)
    ocr_result = read_text(ocr_result_path)

    # Compute WER and CER
    wer = jiwer.wer(ground_truth, ocr_result)
    cer = jiwer.cer(ground_truth, ocr_result)

    return wer, cer

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python compare_texts.py <ground_truth.txt> <ocr_result.txt>")
        sys.exit(1)

    ground_truth_path = sys.argv[1]
    ocr_result_path = sys.argv[2]

    # Calculate WER and CER
    wer, cer = calculate_wer_cer(ground_truth_path, ocr_result_path)

    print(f"WER: {wer:.4f}")
    print(f"CER: {cer:.4f}")



