# OCR Models Comparison

## Overview
This project compares the performance of various OCR (Optical Character Recognition) models using a shared set of test images. The models evaluated include Tesseract, EasyOCR, PaddleOCR, and Hugging Face-based models (TrOCR).

### Goals
- Assess the accuracy and performance of different OCR engines on real-world images.
- Analyze the impact of text type (printed vs. handwritten) on model performance.
- Develop a versatile tool for OCR model evaluation, suitable for integration into other projects.

---

## Libraries and Technologies Used
1. **Tesseract OCR**
   - A widely used, traditional OCR solution.
2. **EasyOCR**
   - Lightweight and simple-to-use OCR engine.
3. **PaddleOCR**
   - A robust library supporting multi-language OCR.
4. **TrOCR (Hugging Face)**
   - Transformer-based models capable of recognizing both printed and handwritten text.
5. **Python Logging**
   - Used to filter unnecessary messages and improve the clarity of output.

---

## Usage Instructions
To analyze an image using the OCR models, run the following command in your terminal:

```bash
python models.py <path_to_image>
```

#### Example:
```bash
python models.py figure-65.png
```

---

## Logging Configuration
To ensure output readability and suppress verbose logs:
- Messages below the `WARNING` level are hidden.
- Output focuses exclusively on OCR results.

### Benefits of Logging:
- Streamlines debugging by reducing noise from external libraries.
- Makes outputs concise and relevant.

---

## Notes and Considerations
1. **TrOCR**
   - Performs well on handwritten text but may have reduced accuracy with printed text.
2. **PaddleOCR**
   - Optimal performance is achieved using a GPU.
3. **EasyOCR**
   - Offers ease of integration but can be slower on larger images.

