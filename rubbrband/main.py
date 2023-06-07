import requests

api_key = None


def init(apikey):
    global api_key
    api_key = apikey


def upload(image, name):
    if api_key is None:
        print("Provide an API key in the init function")

        return False

    response = requests.post("https://block.rubbrband.com/upload_img?api_key=" + api_key)

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
