from transformers import CLIPProcessor, CLIPModel
from PIL import Image

# loading this once when the file is first imported
# not inside a function, so it only happens one time when the program starts
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# these are the categories we sort images into
# note: has to actually cover what youre expecting or it guesses wrong
image_labels = [
    "a screenshot",
    "a meme",
    "a receipt",
    "a photo of a person",
    "a document scan",
    "a nature or landscape photo"
]

def classify_image(filepath):

    img = Image.open(filepath)
    inputs = processor(text=image_labels, images=img, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)

    # find the label with the highest score
    best_index = probs.argmax()
    best_label = image_labels[best_index]

    return best_label

def get_embedding(filepath):

    img = Image.open(filepath)
    inputs = processor(images=img, return_tensors="pt")

    image_features = model.get_image_features(pixel_values=inputs["pixel_values"])

    # transformers 5.x wraps the result in an object instead of returning
    # a plain tensor, this handles both cases so it works either way
    if hasattr(image_features, "pooler_output"):
        image_features = image_features.pooler_output

    return image_features.detach().numpy()[0]