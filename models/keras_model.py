import keras_ocr

def load_model():
    # Load the pre-trained Keras-OCR model
    pipeline = keras_ocr.pipeline.Pipeline()
    return pipeline

def recognize_text(pipeline, image_path):
    # Read the image
    image = keras_ocr.tools.read(image_path)
    # Predict text in the image
    predictions = pipeline.recognize([image])
    return predictions

if __name__ == "__main__":
    # Load the model
    ocr_pipeline = load_model()
    
    # Example usage with an image
    image_path = "image.png"  # Path to your image
    results = recognize_text(ocr_pipeline, image_path)
    
    for text in results[0]:
        print(f"Text: {text[0]}, Confidence: {text[1]:.2f}")
