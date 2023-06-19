import io
import uuid

import PIL
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


def upload(image, prompt, metadata={}):
    if api_key is None:
        print("Provide an API key in the init function")

        return False

    if type(image) == PIL.PngImagePlugin.PngImageFile:
        image = image_to_byte_array(image)

    metadata["prompt"] = prompt
    name = str(uuid.uuid4()) + ".jpg"

    response = requests.post(
        "https://block.rubbrband.com/upload_img?api_key=" + api_key,
        json={"metadata": metadata},
    )

    if response is None:
        return False

    response = response.json()

    if "url" not in response:
        return False

    response = response["url"]

    files = {"file": (name, image)}
    http_response = requests.post(response["url"], data=response["fields"], files=files)

    if http_response.status_code == 204:
        print(f"Successfully uploaded {name}")
    else:
        print(f"Upload failed: {http_response.text}")
