# image_transform.py
from PIL import Image

def transform_image(image):
    # Image transformation logic
    # Example: Resize the image
    image = Image.open(image)
    image = image.resize((300, 300))
    return image
