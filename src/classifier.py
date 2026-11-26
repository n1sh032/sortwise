from transformers import CLIPProcessor, CLIPModel
from PIL import Image

# loading this once when the file is first imported
# not inside a function, so it only happens one time when the program starts
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
