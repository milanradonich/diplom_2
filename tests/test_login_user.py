import pytest

from base_api.login_user import LoginUserAPI
from base_urls import MAIN_URL
from my_data import user_email, user_password, user_name


class TestLoginUser:
    BASE_URL = MAIN_URL
    login_api = LoginUserAPI(BASE_URL)

    def test_login_user(self):
        response = self.login_api.login_user(email=user_email, password=user_password)
        result = response.status_code
        assert result == 200
        response_json = response.json()
        assert response_json.get("accessToken") is not None, "missing Access token"
        assert response_json.get("refreshToken") is not None, "missing Refresh token"
        user_data = response_json.get("user")
        assert user_data is not None, "missing user data"
        assert user_data.get("email") == user_email, "user email does not match"
        assert user_data.get("name") == user_name, "user name does not match"

    @pytest.mark.parametrize("email, password, expected_status, expected_message", [
        ("mradonich90@gmail.com", "01234", 401, "email or password are incorrect"),
        ("mradonich90@gmail.coms", "1234", 401, "email or password are incorrect"),
        ("dmradonich90@gmail.com", "1234f", 401, "email or password are incorrect")
    ])
    def test_login_user_with_incorrect_login_and_password_get_error(self, email, password, expected_status,
                                                                    expected_message):
        result = self.login_api.login_user(email=email, password=password)
        assert result.status_code == expected_status
        assert result.json()["message"] == expected_message


