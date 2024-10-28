import json
from base_urls import *
from http_client import HttpClient, HttpMethods


class UserAPI:
    def __init__(self, base_url):
        self.client = HttpClient(base_url)

    def create_user(self, email=None, password=None, name=None):
        endpoint = CREATE_USER_ENDPOINT
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        response = self.client.send_request(HttpMethods.POST, endpoint, json=data)
        return response

