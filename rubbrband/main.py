import base64
import io
import os
import re

import requests
from PIL import Image

api_key = None


def init(apikey):
    """Initialize the Rubbrband API key"""
    global api_key
    api_key = apikey


def image_to_jpg_byte_array(image):
    """Convert an image to a JPEG byte array"""
    assert isinstance(image, (Image.Image, bytes)), "Image must be a PIL image or a byte array"

    if isinstance(image, Image.Image):
        # Convert PIL image to JPEG byte array
        image = image.convert("RGB")
        jpg_byte_arr = io.BytesIO()
        image.save(jpg_byte_arr, format="JPEG")
        jpg_byte_arr = jpg_byte_arr.getvalue()
    elif isinstance(image, bytes) and image.startswith(b"\xff\xd8"):
        # The byte array already contains a JPEG header
        jpg_byte_arr = image
    else:
        # Convert other image types to JPEG byte array
        image = Image.open(io.BytesIO(image))
        image = image.convert("RGB")
        jpg_byte_arr = io.BytesIO()
        image.save(jpg_byte_arr, format="JPEG")
        jpg_byte_arr = jpg_byte_arr.getvalue()

    return jpg_byte_arr


def jpg_byte_array_to_b64(jpg_byte_arr):
    """Convert a JPEG byte array to a base64 string"""
    return base64.b64encode(jpg_byte_arr).decode("utf-8")


def is_url(string):
    """Check if a string is a valid URL"""
    regex_pattern = r"^(https?|ftp):\/\/([^\s/$.?#].[^\s]*)$"
    return bool(re.match(regex_pattern, string))


def eval(image, features=["is_deformed"], prompt="No prompt", metadata={}):
    """Evaluate an image and return the response"""
    image_url = None

    # Handle image input
    if isinstance(image, str) and is_url(image):
        # If image is a url, download it
        image_url = image
    elif isinstance(image, str) and os.path.isfile(image):
        # If image is a file path, read it
        with open(image, "rb") as file:
            image = file.read()
    elif isinstance(image, (Image.Image, bytes)):
        pass
    else:
        print("Invalid image type")
        return False

    if image_url:
        response = requests.post(
            "https://api.rubbrband.com/eval",
            json={
                "metadata": metadata,
                "prompt": prompt,
                "image_url": image_url,
                "api_key": api_key,
                "features": features,
            },
            headers={
                "Content-Type": "application/json",
            },
            timeout=5,
        )
    else:
        image = image_to_jpg_byte_array(image)
        base64_image = jpg_byte_array_to_b64(image)
        response = requests.post(
            "https://api.rubbrband.com/eval",
            json={
                "metadata": metadata,
                "prompt": prompt,
                "image": base64_image,
                "api_key": api_key,
                "features": features,
            },
            headers={
                "Content-Type": "application/json",
            },
            timeout=5,
        )

    if response is None:
        return False

    response = response.json()

    return response


def vote_on_image(filename, vote):
    """Vote on an image"""
    if api_key is None:
        print("Provide an API key in the init function")
        return False

    if vote not in [0, 1]:
        print("Invalid vote. Please vote 0 or 1, 0 being bad, 1 being good.")
        return False

    response = requests.post(
        f"https://block.rubbrband.com/vote?api_key={api_key}",
        json={"filename": filename, "api_key": api_key, "vote": vote},
        timeout=5,
    )

    if response is None:
        return False

    if response.status_code != 200:
        print(response.text)

    return True
