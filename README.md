```markdown
# OCR Models Comparison

## Description
This project is designed to test and compare the performance of various OCR (Optical Character Recognition) models on the same set of images. It evaluates results from Tesseract, EasyOCR, PaddleOCR, and Hugging Face-based models (TrOCR).

## Purpose
- To explore the accuracy and performance of different OCR engines on real-world images.
- To study how text type (printed vs. handwritten) affects model performance.
- To create a universal tool for OCR model evaluation with potential for integration into other projects.

---

## Libraries and Technologies Used
1. **Tesseract OCR** - Classic OCR solution.
2. **EasyOCR** - Lightweight and easy-to-use OCR engine.
3. **PaddleOCR** - Powerful library with multi-language OCR support.
4. **TrOCR (Hugging Face)** - Transformer-based models for text recognition, including handwritten text.
5. **Python Logging** - Used to suppress unnecessary messages and improve output readability.

---

## Usage
Run the script by providing the path to the image for analysis:
```bash
python models.py <path_to_image>
```

Example:
```bash
python models.py figure-65.png
```

---

## Logging
Logging is used to suppress excessive messages from libraries and improve output readability. This is especially helpful when working with multiple models that may generate unnecessary warnings and debug logs. Logging configuration allows you to:
- Suppress messages below the `WARNING` level.
- Focus the output only on OCR results.

---

## Notes
1. **TrOCR**: If the model is trained for handwritten text, accuracy may drop for printed text.
2. **PaddleOCR**: Using a GPU is recommended for faster performance.
3. **EasyOCR**: Simple to integrate but may have slower performance on larger images.
```