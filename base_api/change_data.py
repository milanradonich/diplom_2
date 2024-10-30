from http_client import HttpClient, HttpMethods
from base_urls import *


class ChangeDataApi:
    def __init__(self, base_url):
        self.client = HttpClient(base_url)

    def change_data(self, email=None, password=None, name=None, token=None):
        endpoint = UPDATE_DATA_ENDPOINT
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        headers = {
            "Authorization": token
        }
        response = self.client.send_request(HttpMethods.PATCH, endpoint, json=data, headers=headers)
        return response
