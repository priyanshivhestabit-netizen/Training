import os
import pytesseract
from PIL import Image

from transformers import BlipProcessor, BlipForConditionalGeneration 
import torch

blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def extract_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}")
        return ""
    
def generate_caption(image_path):
   
    try:
        img = Image.open(image_path).convert("RGB")
        inputs = blip_processor(img, return_tensors="pt")
 
        with torch.no_grad():
            out = blip_model.generate(**inputs, max_new_tokens=50)
 
        caption = blip_processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        print(f"Caption error on {image_path}: {e}")
        return ""
    

def load_images(folder):
    images = []
 
    for file in os.listdir(folder):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(folder, file)
 
            print(f"  Processing: {file}")
 
            ocr_text = extract_text(path)
            caption = generate_caption(path)
 
            combined_text = ""
            if ocr_text:
                combined_text += f"OCR: {ocr_text} "
            if caption:
                combined_text += f"Caption: {caption}"
 
            images.append({
                "path": path,
                "text": combined_text.strip(),   # used for CLIP text embedding & display
                "ocr_text": ocr_text,            # raw OCR only
                "caption": caption,              # BLIP caption only
                "source": file
            })
 
    print(f"  Loaded {len(images)} images")
    return images
