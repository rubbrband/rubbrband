import io
import os
import re
import time

import requests
from PIL import Image

api_key = None


def init(apikey):
    global api_key
    api_key = apikey


def image_to_byte_array(image):
    # BytesIO is a file-like buffer stored in memory
    imgByteArr = io.BytesIO()
    # image.save expects a file-like as a argument
    image.save(imgByteArr, format=image.format)
    # Turn the BytesIO object back into a bytes object
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def is_url(string):
    regex_pattern = r"^(https?|ftp):\/\/([^\s/$.?#].[^\s]*)$"
    return bool(re.match(regex_pattern, string))


def upload(image, prompt, metadata={}):
    if api_key is None:
        print("Provide an API key in the init function")
        return False

    # Handle image input
    if type(image) == str and is_url(image):
        # If image is a url, download it
        image_url_response = requests.get(image)
        if image_url_response.status_code != 200 or image_url_response.content is None:
            return False
        image = image_url_response.content
    elif isinstance(image, Image.Image):
        # If image is a PIL, convert it to bytes
        image = image_to_byte_array(image)
    elif type(image) == str and os.path.isfile(image):
        # If image is a file path, read it
        with open(image, "rb") as f:
            image = f.read()
    elif type(image) == bytes:
        pass
    else:
        print("Invalid image type")
        return False

    metadata["prompt"] = prompt

    response = requests.post(
        "https://block.rubbrband.com/upload_img?api_key=" + api_key,
        json={"metadata": metadata},
    )

    if response is None:
        return False

    response = response.json()

    if "url" not in response:
        return False

    filename = response["filename"]
    response = response["url"]

    files = {"file": (filename, image)}
    requests.post(response["url"], data=response["fields"], files=files)

    return filename


def get_image_metadata(filename, retries=8):
    if api_key is None:
        print("Provide an API key in the init function")
        return False

    for i in range(retries):
        response = requests.get(
            "https://block.rubbrband.com/get_image_metadata?api_key=" + api_key + "&filename=" + filename
        )
        if response is None:
            return False

        if response.status_code != 200:
            print(response.text)

        response = response.json()
        data = response.get("data", None)
        if data is not None and "composition_score" in data:
            return data
        print(f"{retries - i} retries left")
        time.sleep(1)

    print("Failed to get image metadata. Try again later.")
    return False
