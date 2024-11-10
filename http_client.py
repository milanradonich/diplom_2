import json
from enum import Enum

import requests


class HttpMethods(str, Enum):
    GET = 'GET'
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class HttpClient:
    def __init__(self, url):
        self.base_url = url

    def send_request(self, method: HttpMethods, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"

        if kwargs:
            if "data" in kwargs and isinstance(kwargs["data"], dict):
                kwargs["data"] = json.dumps(kwargs["data"])
        try:
            response = requests.request(method, url, **kwargs)
        except requests.RequestException as e:
            f"Запрос {method} не может быть отправлен по {url}. Ошибка {e}"
        else:
            return response

