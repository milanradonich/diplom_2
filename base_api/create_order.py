from http_client import HttpClient, HttpMethods
from base_urls import *


class CreateOrder:
    def __init__(self, base_url):
        self.client = HttpClient(base_url)

    def create_order(self, ingredients=None):
        endpoint = CREATE_ORDER
        data = {
            "ingredients": ingredients
        }

        response = self.client.send_request(HttpMethods.POST, endpoint, json=data)
        return response



