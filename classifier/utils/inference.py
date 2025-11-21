import torch
from PIL import Image
from .device import get_device
from .labels import get_label
from .preprocessing import get_transforms

def load_model(model_path, model_class):
    device = get_device()
    model = model_class()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    return model


def predict(img_path, model):
    device = get_device()
    transforms = get_transforms()

    img = Image.open(img_path).convert("RGB")
    img_tensor = transforms(img).unsqueeze(0).to(device)

    model.eval()
    with torch.no_grad():
        output = model(img_tensor)
        prob = torch.sigmoid(output).item()
        pred_idx = 1 if prob > 0.4 else 0

    return get_label(pred_idx), pred_idx
