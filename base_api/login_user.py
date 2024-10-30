from http_client import HttpClient, HttpMethods
from base_urls import *


class LoginUserAPI:
    def __init__(self, base_url):
        self.client = HttpClient(base_url)

    def login_user(self, email=None, password=None):
        endpoint = LOGIN_ENDPOINT
        data = {
            "email": email,
            "password": password,
        }
        response = self.client.send_request(HttpMethods.POST, endpoint, json=data)
        return response
