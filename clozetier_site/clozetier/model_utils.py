# clozetier/model_utils.py

import torch
from torchvision import transforms, models
from torchvision.models import efficientnet_b0
import torch.nn as nn
from PIL import Image

model = efficientnet_b0(pretrained=True)

num_classes = 14
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

state_dict = torch.load('Clothing_AI_Model.pt', map_location=torch.device('cpu'))

model.load_state_dict(state_dict)

model.eval()

def run_image_through_model(image_path):
    # Define the transformations
    transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

    # Load the image
    image = Image.open(image_path).convert('RGB')

    # Apply transformations
    input_tensor = transform(image).unsqueeze(0)

    # Pass the image through the model
    with torch.no_grad():
        output = model(input_tensor)

    return output.argmax(dim=1).item()
