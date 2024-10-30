import pytest

from base_api.create_order import CreateOrder
from base_api.login_user import LoginUserAPI
from base_urls import MAIN_URL
from helper import create_ingredients_list
from my_data import user_email, user_password


class TestCreateOrder:
    BASE_URL = MAIN_URL
    create_order_api = CreateOrder(BASE_URL)
    login_api = LoginUserAPI(BASE_URL)

    def test_create_order_not_auth_success_true(self):
        order_response = self.create_order_api.create_order(create_ingredients_list())
        assert order_response.status_code == 200
        response_data = order_response.json()
        assert response_data.get("success") is True

    def test_create_order_with_auth_success_true(self):
        login_response = self.login_api.login_user(email=user_email, password=user_password)
        result = login_response.status_code
        assert result == 200
        response_json = login_response.json()
        assert response_json.get("accessToken") is not None, "missing Access token"
        order_response = self.create_order_api.create_order(create_ingredients_list())
        assert order_response.status_code == 200
        response_data = order_response.json()
        assert response_data.get("success") is True

    @pytest.mark.parametrize("ingredient_ids, expected_status, expected_message", [
        (None, 400, "Ingredient ids must be provided"),
        (["invalid_id"], 500, "Internal Server Error")
    ])
    def test_create_order_without_ingredients_and_incorrect_hash_success_false(self, ingredient_ids, expected_status, expected_message):
        order_response = self.create_order_api.create_order(ingredient_ids)
        assert order_response.status_code == expected_status
        if expected_status == 500:
            assert "Internal Server Error" in order_response.text
        else:
            response_data = order_response.json()
            assert response_data.get("message") == expected_message


