import torch
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image
import joblib
import numpy as np
from torchvision.transforms import functional as F
import numpy as np
from sklearn.cluster import KMeans
# Define the ColorClassifier
class ColorClassifier(nn.Module):
    def __init__(self):
        super(ColorClassifier, self).__init__()
        self.fc1 = nn.Linear(3, 16)  # Input layer (3 RGB values) to hidden layer (16 neurons)
        self.fc2 = nn.Linear(16, 16)  # Hidden layer (16 neurons) to hidden layer (16 neurons)
        self.fc3 = nn.Linear(16, len(label_encoder.classes_))  # Hidden layer to output layer (number of categories)

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # Apply ReLU activation
        x = torch.relu(self.fc2(x))  # Apply ReLU activation
        x = self.fc3(x)               # Output layer (logits)
        return x

# Load clothing model
clothing_model = models.efficientnet_b0(weights='IMAGENET1K_V1')
clothing_model.classifier[1] = nn.Linear(clothing_model.classifier[1].in_features, 14)
clothing_model.load_state_dict(torch.load('Clothing AI/Clothing_AI_Model_V2.pth', map_location=torch.device('cpu')))
clothing_model.eval()

# Load color model and label encoder
label_encoder = joblib.load('Color_AI_Model/label_encoder_v3.pkl')
color_model = ColorClassifier()
color_model.load_state_dict(torch.load('Color_AI_Model/color_classifier_model_v3.pth'))
color_model.eval()

# Define transformations for clothing model
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Get color labels from the label encoder
color_labels = label_encoder.classes_
def extract_dominant_color(image):
    """Extract the dominant color from the image using KMeans clustering."""
    # Center crop to focus on main area of clothing
    image = F.center_crop(image, output_size=(100, 100))  # Adjust size as needed
    image_np = np.array(image)

    # Reshape image data for clustering
    reshaped_img = image_np.reshape(-1, 3)

    # Apply KMeans to find the dominant color
    kmeans = KMeans(n_clusters=1, random_state=0).fit(reshaped_img)
    dominant_color = kmeans.cluster_centers_[0]  # Dominant color in RGB

    # Ensure values are in the expected range and format for the model
    dominant_color = torch.tensor(dominant_color, dtype=torch.float32)  # Already [0-255] range

    return dominant_color.unsqueeze(0)  # Shape for model input


def run_image_through_models(image_path):
    try:
        # Load and preprocess image for clothing model
        image = Image.open(image_path).convert('RGB')
        input_tensor = transform(image).unsqueeze(0)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None

    # Get clothing type prediction
    with torch.no_grad():
        clothing_output = clothing_model(input_tensor)
    clothing_result = clothing_output.argmax(dim=1).item()

    # Prepare color input from extracted dominant color
    color_input = extract_dominant_color(image)

    # Get color prediction as a class label
    with torch.no_grad():
        color_output = color_model(color_input)
    color_class_index = color_output.argmax(dim=1).item()

    # Ensure index is valid
    color_result = color_labels[color_class_index] if color_class_index < len(color_labels) else None
    
    return clothing_result, color_result
