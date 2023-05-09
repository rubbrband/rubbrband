_api_key = None


def set_api_key(api_key):
    global _api_key
    _api_key = api_key


def start_job(endpoint, payload):
    if _api_key is None:
        raise ValueError("API key is not set. Please set the API key using set_api_key() function.")

    # headers = {
    #     'Content-Type': 'application/json',
    #     'Authorization': f'Bearer {_api_key}'
    # }

    # response = requests.post(endpoint, json=payload, headers=headers)
    # response.raise_for_status()
    return True
