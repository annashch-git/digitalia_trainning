from transformers import VisionEncoderDecoderModel, AutoProcessor
from PIL import Image

# Укажите путь к процессору и модели
torch_processor = AutoProcessor.from_pretrained(r"D:\XAMK\Internship\Trainnig_rep\digitalia_trainning\multicentury-htr-model")
torch_model = VisionEncoderDecoderModel.from_pretrained(r"D:\XAMK\Internship\Trainnig_rep\digitalia_trainning\multicentury-htr-model")

# Обработка изображения
image_path = "figure-65.png"
image = Image.open(image_path).convert("RGB")
inputs = processor(images=image, return_tensors="pt")
outputs = model.generate(**inputs)
result = processor.batch_decode(outputs, skip_special_tokens=True)

print("OCR Result:", result)
