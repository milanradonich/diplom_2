from http_client import HttpClient, HttpMethods
from base_urls import *


class GetOrderApi:
    def __init__(self, base_url):
        self.client = HttpClient(base_url)

    def get_order(self, token=None):
        endpoint = GET_ORDER

        headers = {
            "Authorization": token
        }
        response = self.client.send_request(HttpMethods.GET, endpoint, headers=headers)
        return response
