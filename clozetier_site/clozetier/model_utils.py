# # clozetier/model_utils.py

# import torch
# from torchvision import transforms, models
# from torchvision.models import efficientnet_b0
# import torch.nn as nn
# from PIL import Image

# model = models.efficientnet_b0(weights='IMAGENET1K_V1')

# num_classes = 14
# model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

# state_dict = torch.load('Clothing_AI_Model.pt', map_location=torch.device('cpu'), weights_only=True)

# model.load_state_dict(state_dict)

# model.eval()

# def run_image_through_model(image_path):
#     # Define the transformations
#     transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
# ])

#     # Load the image
#     image = Image.open(image_path).convert('RGB')

#     # Apply transformations
#     input_tensor = transform(image).unsqueeze(0)

#     # Pass the image through the model
#     with torch.no_grad():
#         output = model(input_tensor)

#     return output.argmax(dim=1).item()


# clozetier/model_utils.py

# clozetier/model_utils.py

# model_utils.py

import torch
print(torch.__version__)
from torchvision import transforms, models
from torchvision.models import efficientnet_b0
import torch.nn as nn
from PIL import Image

# Load clothing model
clothing_model = models.efficientnet_b0(weights='IMAGENET1K_V1')
clothing_model.classifier[1] = nn.Linear(clothing_model.classifier[1].in_features, 14)
clothing_model.load_state_dict(torch.load('Clothing_AI_Model.pt', map_location=torch.device('cpu'), weights_only=True))
clothing_model.eval()

# Load color model
color_model = models.efficientnet_b0(weights='IMAGENET1K_V1')
color_model.classifier[1] = nn.Linear(color_model.classifier[1].in_features, 23)
color_model.load_state_dict(torch.load('C:/Users/Aiden/Software_Engineering_Project/github repo/clozetier/color_classifier.pth', map_location='cpu'), strict=False)
color_model.eval()

# Define transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Color categories
index_to_color = {
    0: 'Black',
    1: 'White',
    2: 'Dark-Gray',
    3: 'Gray',
    4: 'Light-Gray',
    5: 'Dark-Blue',
    6: 'Blue',
    7: 'Light-Blue',
    8: 'Dark-Brown',
    9: 'Brown',
    10: 'Cream',
    11: 'Dark-Red',
    12: 'Red',
    13: 'Light-Red',
    14: 'Pink',
    15: 'Purple',
    16: 'Dark-Green',
    17: 'Green',
    18: 'Light-Green',
    19: 'Yellow',
    20: 'Orange',
    21: 'Peach',
    22: 'Gold'
}

color_labels = list(index_to_color.values())

def classify_color(rgb_values):
    """ Match the RGB values to the closest color category based on ranges. """
    for color_name, (min_rgb, max_rgb) in index_to_color.items():
        if all(min_rgb[i] <= rgb_values[i] <= max_rgb[i] for i in range(3)):
            return color_name
    
    return "Unknown"

def run_image_through_models(image_path):
    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    input_tensor = transform(image).unsqueeze(0)
    
    # Get clothing type prediction
    with torch.no_grad():
        clothing_output = clothing_model(input_tensor)
    clothing_result = clothing_output.argmax(dim=1).item()
    
    # Get color prediction as a class label
    with torch.no_grad():
        color_output = color_model(input_tensor)
    color_class_index = color_output.argmax(dim=1).item()
    color_result = color_labels[color_class_index]  # Map index to color name
    
    return clothing_result, color_result



