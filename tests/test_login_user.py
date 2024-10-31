import allure
import pytest

from base_api.login_user import LoginUserAPI
from base_urls import MAIN_URL
from my_data import user_email, user_password, user_name


class TestLoginUser:
    BASE_URL = MAIN_URL
    login_api = LoginUserAPI(BASE_URL)

    @allure.title("Проверка корректного логина юзера")
    @allure.description("Тест проверяет успешный вход юзера в систему.")
    def test_login_user(self):
        with allure.step("Вызов функции логина в систему"):
            response = self.login_api.login_user(email=user_email, password=user_password)
            result = response.status_code
        with allure.step("Проверка статуса ответа"):
            assert result == 200
        with allure.step("Проверка токенов в ответе"):
            response_json = response.json()
            assert response_json.get("accessToken") is not None, "missing Access token"
            assert response_json.get("refreshToken") is not None, "missing Refresh token"
        with allure.step("Проверка тела в ответе"):
            user_data = response_json.get("user")
            assert user_data is not None, "missing user data"
            assert user_data.get("email") == user_email, "user email does not match"
            assert user_data.get("name") == user_name, "user name does not match"

    @pytest.mark.parametrize("email, password, expected_status, expected_message", [
        ("mradonich90@gmail.com", "01234", 401, "email or password are incorrect"),
        ("mradonich90@gmail.coms", "1234", 401, "email or password are incorrect"),
        ("dmradonich90@gmail.com", "1234f", 401, "email or password are incorrect")
    ])
    @allure.title("Проверка логина с невалидными данными юзера")
    @allure.description("Тест проверяет неуспешный вход юзера в систему.")
    def test_login_user_with_incorrect_login_and_password_get_error(self, email, password, expected_status,
                                                                    expected_message):
        with allure.step("Вызов функции логина в систему"):
            result = self.login_api.login_user(email=email, password=password)
        with allure.step("Проверка статуса ответа"):
            assert result.status_code == expected_status
        with allure.step("Проверка тела ответа"):
            assert result.json()["message"] == expected_message


