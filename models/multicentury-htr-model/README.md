---
license: apache-2.0
language:
- fi
- sv
metrics:
- cer
pipeline_tag: image-to-text
---
# Model description

**Model Name:** multicentury-htr-model

**Model Type:** Transformer-based OCR (TrOCR)

**Base Model:** microsoft/trocr-large-handwritten

**Purpose:** Handwritten text recognition

**Languages:** Swedish, Finnish

**License:** Apache 2.0

This model is a fine-tuned version of the microsoft/trocr-large-handwritten model, specialized for recognizing handwritten text. It has been trained on various dataset from 17th to 20th centuries and can be used for applications such as document digitization, form recognition, or any task involving handwritten text extraction.

# Model Architecture

The model is based on a Transformer architecture (TrOCR) with an encoder-decoder setup:

- The encoder processes images of handwritten text.
- The decoder generates corresponding text output.

# Intended Use

This model is designed for handwritten text recognition and is intended for use in:

- Document digitization (e.g., archival work, historical manuscripts)
- Handwritten notes transcription

# Training data

The training datasetincludes more than 760 000 samples of handwritten text rows, covering a wide variety of handwriting styles and text samples.

# Evaluation

The model was evaluated on test dataset. Below are key metrics:

**Character Error Rate (CER):** 3.2

**Test Dataset Description:** size ~94 900 text rows

# How to Use the Model

You can use the model directly with Hugging Face’s pipeline function or by manually loading the processor and model.

```python
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

# Load the model and processor
processor = TrOCRProcessor.from_pretrained("Kansallisarkisto/multicentury-htr-model/processor")
model = VisionEncoderDecoderModel.from_pretrained("Kansallisarkisto/multicentury-htr-model")

# Open an image of handwritten text
image = Image.open("path_to_image.png")

# Preprocess and predict
pixel_values = processor(image, return_tensors="pt").pixel_values
generated_ids = model.generate(pixel_values)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(generated_text)

```

# Limitations and Biases

The model was trained primarily on handwritten text that uses basic Latin characters (A-Z, a-z) and includes Nordic special characters (å, ä, ö). It has not been trained on non-Latin alphabets, such as Chinese characters, Cyrillic script, or other writing systems like Arabic or Hebrew.
The model may not generalize well to any other languages than Finnish, Swedish or English.

# Future Work

Potential improvements for this model include:

- Expanding training data: Incorporating more diverse handwriting styles and languages.
- Optimizing for specific domains: Fine-tuning the model on domain-specific handwriting.

# Citation

If you use this model in your work, please cite it as:

@misc{multicentury_htr_model_2024,

  author = {Kansallisarkisto},

  title = {Multicentury HTR Model: Handwritten Text Recognition},
  
  year = {2024},
  
  publisher = {Hugging Face},
  
  howpublished = {\url{https://huggingface.co/Kansallisarkisto/multicentury-htr-model/}},

}

## Model Card Authors

Author: Kansallisarkisto
Contact Information: riikka.marttila@kansallisarkisto.fi, ilkka.jokipii@kansallisarkisto.fi