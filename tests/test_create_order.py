import allure
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

    @allure.title("Проверка создания нового заказа без авторизации")
    @allure.description("Тест проверяет успешное создание нового заказа без авторизации.")
    def test_create_order_not_auth_success_true(self):
        with allure.step("Вызов функции создания заказа"):
            order_response = self.create_order_api.create_order(create_ingredients_list())
        with allure.step("Проверка статуса ответа"):
            assert order_response.status_code == 200
        with allure.step("Проверка тела ответе"):
            response_data = order_response.json()
            assert response_data.get("success") is True

    @allure.title("Проверка создания нового заказа с авторизацией")
    @allure.description("Тест проверяет успешное создание нового заказа без авторизации.")
    def test_create_order_with_auth_success_true(self):
        with allure.step("Вызов функции логина в систему"):
            login_response = self.login_api.login_user(email=user_email, password=user_password)
            result = login_response.status_code
        with allure.step("Проверка статуса ответа"):
            assert result == 200
        with allure.step("Проверка токенов в ответе"):
            response_json = login_response.json()
            assert response_json.get("accessToken") is not None, "missing Access token"
        with allure.step("Вызов функции создания заказа"):
            order_response = self.create_order_api.create_order(create_ingredients_list())
        with allure.step("Проверка статуса ответа"):
            assert order_response.status_code == 200
        with allure.step("Проверка тела ответе"):
            response_data = order_response.json()
            assert response_data.get("success") is True

    @pytest.mark.parametrize("ingredient_ids, expected_status, expected_message", [
        (None, 400, "Ingredient ids must be provided"),
        (["invalid_id"], 500, "Internal Server Error")
    ])
    @allure.title("Проверка создания нового заказа без ингредиентов и с некорректным хешем")
    @allure.description("Тест проверяет, что система вернет ошибку при создании заказа без ингредиентов или с неверным "
                        "хешем ингредиентов")
    def test_create_order_without_ingredients_and_incorrect_hash_success_false(self, ingredient_ids, expected_status,
                                                                               expected_message):
        with allure.step("Вызов функции создания заказа"):
            order_response = self.create_order_api.create_order(ingredient_ids)
        with allure.step("Проверка статуса ответа"):
            assert order_response.status_code == expected_status
        with allure.step("Проверка тела ответе"):
            if expected_status == 500:
                with allure.step("Проверка текста ответа на наличие ошибки"):
                    assert "Internal Server Error" in order_response.text
            else:
                with allure.step("Проверка тела ответе"):
                    response_data = order_response.json()
                    assert response_data.get("message") == expected_message


