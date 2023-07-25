import io
import re

import PIL
import PIL.PngImagePlugin
import requests

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

    if type(image) == str and is_url(image):
        image_url_response = requests.get(image)
        if image_url_response.status_code != 200 or image_url_response.content is None:
            return False
        image = image_url_response.content

    if type(image) == PIL.PngImagePlugin.PngImageFile:
        image = image_to_byte_array(image)

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

    return True
