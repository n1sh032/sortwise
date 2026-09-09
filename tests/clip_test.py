from transformers import CLIPProcessor, CLIPModel
from PIL import Image

# loading the model, this downloads it the first time (its kinda big)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

#test image
image_path = "test_image.png"
img = Image.open(image_path)

# these are the categories we're checking against
# clip doesnt need training examples, just descriptions
labels = ["a screenshot", "a meme", "a receipt", "a photo of a person", "a document scan", "a nature or landscape photo"]

inputs = processor(text=labels, images=img, return_tensors="pt", padding=True)
outputs = model(**inputs)

# this turns the raw scores into probabilities that add up to 1
probs = outputs.logits_per_image.softmax(dim=1)

for label, prob in zip(labels, probs[0]):
    print(label, "-", round(prob.item()*100, 2), "%")