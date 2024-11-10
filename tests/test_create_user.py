import allure
import pytest

from base_api.create_user import UserAPI
from base_urls import MAIN_URL
from helper import create_new_user_and_return_email_password_name
from my_data import *


class TestCreateUser:
    BASE_URL = MAIN_URL
    user_api = UserAPI(BASE_URL)

    @allure.title("Проверка создания нового уникального юзера")
    @allure.description("Тест проверяет успешное создание нового юзера.")
    def test_create_new_user_success(self):
        with allure.step("Вызов функции создания юзера с рандомными данными"):
            status_code, response_data, login_pass = create_new_user_and_return_email_password_name()
        with allure.step("Проверка статуса ответа"):
            assert status_code == 200
        with allure.step("Проверка получения токена в ответе"):
            assert response_data.get("accessToken") is not None, "missing Access token"
            assert response_data.get("refreshToken") is not None, "missing Refresh token"

    @allure.title("Проверка создания зарегистрированного юзера")
    @allure.description("Тест проверяет, что нельзя создать уже зарегистрированного юзера.")
    def test_create_user_is_already_registered_get_error(self):
        with allure.step("Вызов функции создания юзера со старыми данными"):
            response = self.user_api.create_user(email=user_email, password=user_password,
                                                 name=user_name)
            result = response.status_code
            result_answer = response.json()
        with allure.step("Проверка статуса ответа"):
            assert result == 403
        with allure.step("Проверка тела ответе"):
            assert result_answer['message'] == "User already exists"

    @pytest.mark.parametrize("email, password, name", [
        (user_email, user_password, None),
        (user_email, None, user_name),
        (None, user_password, user_name)])
    @allure.title("Проверка создания юзера без одного параметра")
    @allure.description("Тест проверяет, что нельзя создать юзера без одного из параметров.")
    def test_create_user_without_one_required_fields_get_error(self, email, password, name):
        with allure.step("Вызов функции создания юзера без одного из параметров"):
            response = self.user_api.create_user(email=email, password=password, name=name)
            result = response.status_code
        with allure.step("Проверка статуса ответа"):
            assert result == 403
        with allure.step("Проверка тела ответе"):
            assert response.json()["message"] == "Email, password and name are required fields"
