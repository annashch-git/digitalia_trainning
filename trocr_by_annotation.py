import json
import os
import argparse
from PIL import Image
import editdistance
from transformers import VisionEncoderDecoderModel, AutoProcessor
import torch
import re
import logging
import warnings
from transformers import logging as transformers_logging

transformers_logging.set_verbosity_error()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.WARNING) 

parser = argparse.ArgumentParser(description="OCR with TrOCR + CER/WER evaluation")
parser.add_argument("image", type=str, help="Path to image file")
parser.add_argument("ann", type=str, help="Path to annotation JSON")
args = parser.parse_args()

processor = AutoProcessor.from_pretrained(r"D:\XAMK\Internship\Trainnig_rep\digitalia_trainning\models\multicentury-htr-model")
model = VisionEncoderDecoderModel.from_pretrained(r"D:\XAMK\Internship\Trainnig_rep\digitalia_trainning\models\multicentury-htr-model")

def ocr_trocr(image):
    inputs = processor(images=image, return_tensors="pt")
    outputs = model.generate(**inputs)
    text = processor.batch_decode(outputs, skip_special_tokens=True)
    return text[0] if text else ""

image = Image.open(args.image).convert("RGB")

with open(args.ann, "r", encoding="utf-8") as f:
    raw = f.read().strip()

try:
    annotations = json.loads(raw)
except json.JSONDecodeError:
    lines = raw.splitlines()
    lines = lines[1:] 
    content = "".join(lines).strip()
    if content.endswith(","):
        content = content[:-1]
    try:
        annotations = json.loads("[" + content + "}]")
    except json.JSONDecodeError as e:
        print(e)
        exit(1)

results = []
all_gt_chars = 0
all_ocr_chars = 0
char_errors = 0

all_gt_words = 0
all_ocr_words = 0
word_errors = 0

ocr_lines = []

for ann in annotations:
    bboxes = ann["bbox"]
    gts = ann["transcription"]

    for bbox, gt_text in zip(bboxes, gts):
        x = int(bbox["x"] * image.width / 100)
        y = int(bbox["y"] * image.height / 100)
        w = int(bbox["width"] * image.width / 100)
        h = int(bbox["height"] * image.height / 100)

        cropped = image.crop((x, y, x + w, y + h))

        try:
            ocr_text = ocr_trocr(cropped)
        except Exception as e:
            ocr_text = f"[ERROR: {e}]"

        # CER
        char_errors += editdistance.eval(gt_text, ocr_text)
        all_gt_chars += len(gt_text)
        all_ocr_chars += len(ocr_text)

        # WER
        gt_words = re.findall(r'\S+', gt_text)
        ocr_words = re.findall(r'\S+', ocr_text)
        word_errors += editdistance.eval(gt_words, ocr_words)
        all_gt_words += len(gt_words)
        all_ocr_words += len(ocr_words)

        results.append({
            "gt": gt_text,
            "ocr": ocr_text,
        })

        ocr_lines.append(ocr_text)

base_name = os.path.splitext(os.path.basename(args.image))[0]
output_dir = os.path.dirname(args.image)

output_txt_path = os.path.join(output_dir, f"{base_name}_trocr.txt")

with open(output_txt_path, "w", encoding="utf-8") as f:
    for line in ocr_lines:
        f.write(line + "\n")

metrics_path = os.path.join(output_dir, f"{base_name}_trocr_metrics.txt")

cer = char_errors / all_gt_chars if all_gt_chars > 0 else 0
wer = word_errors / all_gt_words if all_gt_words > 0 else 0

print(f"Word Error Rate (СER): {cer:.4f}")
print(f"Word Error Rate (WER): {wer:.4f}")
print(f"OCR saved to: {output_dir}")
