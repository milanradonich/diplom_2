

from http_client import HttpClient, HttpMethods
from base_urls import *


class GetIngredients:
    def __init__(self, base_url):
        self.client = HttpClient(base_url)

    def get_ingredients(self):
        endpoint = GET_INGREDIENTS

        response = self.client.send_request(HttpMethods.GET, endpoint)
        return response

