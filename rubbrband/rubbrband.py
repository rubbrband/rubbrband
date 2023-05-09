import requests

_api_key = None


def set_api_key(api_key):
    global _api_key
    _api_key = api_key


def start_job(prompt):
    if _api_key is None:
        raise ValueError("API key is not set. Please set the API key using set_api_key() function.")

    endpoint = "http://localhost:4200/add_job"

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {_api_key}"}

    payload = {
        "api_key": _api_key,
        "prompt": prompt,
    }

    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    print(response)
    return True
