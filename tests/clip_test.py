from transformers import CLIPProcessor, CLIPModel
from PIL import Image

# loading the model, this downloads it the first time (its kinda big)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

#test image
image_path = "test_image.png"
img = Image.open(image_path)

# these are the categories we're checking against
