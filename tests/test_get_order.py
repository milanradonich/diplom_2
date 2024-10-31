import allure

from base_api.get_order import GetOrderApi
from base_api.login_user import LoginUserAPI
from base_urls import MAIN_URL
from my_data import user_email, user_password


class TestCreateOrder:
    BASE_URL = MAIN_URL
    get_order_api = GetOrderApi(BASE_URL)
    login_api = LoginUserAPI(BASE_URL)

    @allure.title("Проверка получения заказа конкретного юзера")
    @allure.description("Тест проверяет успешное получение заказа(ов) юзера.")
    def test_get_order_user(self):
        with allure.step("Вызов функции логина в систему"):
            login_response = self.login_api.login_user(email=user_email, password=user_password)
        with allure.step("Проверка статуса ответа"):
            result = login_response.status_code
            assert result == 200
        with allure.step("Проверка получения токена в ответе"):
            response_json = login_response.json()
            assert response_json.get("accessToken") is not None, "missing Access token"
            token = response_json.get("accessToken")
        with allure.step("Вызов функции получения заказов"):
            get_order_response = self.get_order_api.get_order(token)
        with allure.step("Проверка статуса ответа"):
            assert get_order_response.status_code == 200
        with allure.step("Проверка тела ответе"):
            assert get_order_response.json().get("success") is True

    @allure.title("Проверка получения заказа неавторизованного юзера")
    @allure.description("Тест проверяет неуспешное получение заказа(ов) юзера.")
    def test_get_order_non_auth_user(self):
        with allure.step("Вызов функции получения заказов"):
            get_order_response = self.get_order_api.get_order()
        with allure.step("Проверка статуса ответа"):
            assert get_order_response.status_code == 401
        with allure.step("Проверка тела ответа"):
            assert get_order_response.json().get("message") == "You should be authorised"


