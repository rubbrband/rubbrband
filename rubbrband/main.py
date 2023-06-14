import os

import requests

API_KEY = None
ALLOWED_IMG_EXTENSIONS = (".png", ".jpg", ".jpeg")


def init(apiKey):
    global API_KEY
    API_KEY = apiKey


def upload(image, name):
    """Upload an image to the Rubbrband API."""
    assert type(image) == bytes or type(image) == str, "Image must be a bytes object or a path to an image"
    assert type(name) == str, "Name must be a string"

    # Check if image name is valid
    if not name.lower().endswith(ALLOWED_IMG_EXTENSIONS):
        print(f"Invalid image type: {name}. Allowed types: {ALLOWED_IMG_EXTENSIONS}")
        return False

    if type(image) == bytes:
        handle_upload(image, name)
    elif os.path.isfile(image) and name.lower().endswith(ALLOWED_IMG_EXTENSIONS):
        with open(image, "rb") as f:
            handle_upload(f.read(), name)
    elif os.path.isdir(image):
        for file in os.listdir(image):
            if file.lower().endswith(ALLOWED_IMG_EXTENSIONS):
                with open(os.path.join(image, file), "rb") as f:
                    handle_upload(f.read(), file)
    else:
        print(f"Invalid image: {image}")
        return False


def handle_upload(image, name):
    if API_KEY is None:
        print("Provide an API key with the rubbrband.init function")
        return False

    # Get upload URL
    response = requests.post(f"https://block.rubbrband.com/upload_img?api_key={API_KEY}")

    if response is None:
        print("Failed to upload image")
        return False

    # Check if API key is valid
    if response.status_code == 401:
        print(f"Invalid API key: {API_KEY}")
        return False

    response = response.json()

    if "url" not in response:
        print("Failed to upload image")
        return False

    response = response["url"]

    files = {"file": (name, image)}
    http_response = requests.post(response["url"], data=response["fields"], files=files)

    if http_response.status_code == 204:
        print(f"Successfully uploaded {name}")
    else:
        print(f"Upload failed: {http_response.text}")
