# OCR Models Comparison  

## Overview  
This project compares the performance of various OCR (Optical Character Recognition) models using a shared set of test images. The models evaluated include Tesseract, EasyOCR, PaddleOCR, Hugging Face-based models (TrOCR), and **Ollama (LLaVA-based model)**.  

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
5. **Ollama (LLaVA-based OCR)**  
   - Uses a vision-language model for OCR, capable of understanding complex text layouts.  

---

## Usage Instructions  

To analyze an image using all OCR models, run the following command in your terminal:  

```bash
python main_script.py <path_to_image>
```

#### Example:  
```bash
python main_script.py figure-65.png
```  

This command will process the image using all available models and save the results to corresponding text files in the same directory as the input image.  

### Running a Specific OCR Model  

If you want to run a specific OCR model instead of all models, modify the command as follows:  

```bash
python models/<model_script>.py <path_to_image>
```

#### Example (Running Tesseract OCR only):  
```bash
python models/tesseract_ocr.py figure-65.png
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

## Environment Configuration  

Each OCR model runs in its designated virtual environment:  

| Model     | Virtual Environment |
|-----------|--------------------|
| Tesseract | `.venv` |
| TrOCR | `.venv` |
| EasyOCR | `.venv` |
| PaddleOCR | `.venv` |
| Ollama | `.venv_ollama` |


If Ollama is not running, start the server manually before executing the script:  
```bash
ollama serve &
```

---

## Output  

The extracted text for each model is saved in a separate text file in the same directory as the input image:  

```
image_tesseract.txt  
image_easyocr.txt  
image_paddleocr.txt  
image_trocr.txt  
image_ollamaocr.txt  
```

---