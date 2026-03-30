from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import numpy as np

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def _to_tensor(features):
    if isinstance(features, torch.Tensor):
        return features
    if hasattr(features, "pooler_output") and features.pooler_output is not None:
        return features.pooler_output
    if hasattr(features, "last_hidden_state"):
        return features.last_hidden_state[:, 0, :]
    return features[0]


def embed_image(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        features = model.get_image_features(**inputs)

    features = _to_tensor(features)
    features = features / features.norm(dim=-1, keepdim=True)
    return features.detach().cpu().numpy().reshape(-1).astype("float32")  # (512,)


def embed_text(text):
    inputs = processor(text=[text], return_tensors="pt", padding=True)

    with torch.no_grad():
        features = model.get_text_features(**inputs)

    features = _to_tensor(features)
    features = features / features.norm(dim=-1, keepdim=True)
    return features.detach().cpu().numpy().reshape(1, -1).astype("float32")  # (1, 512)