import pytest

from base_api.create_user import UserAPI
from base_urls import MAIN_URL
from helper import create_new_user_and_return_email_password_name
from my_data import *


class TestCreateUser:
    BASE_URL = MAIN_URL
    user_api = UserAPI(BASE_URL)

    def test_create_new_user_success(self):

        status_code, response_data, login_pass = create_new_user_and_return_email_password_name()
        assert status_code == 200
        assert response_data.get("accessToken") is not None, "missing Access token"
        assert response_data.get("refreshToken") is not None, "missing Refresh token"

    def test_create_user_is_already_registered_get_error(self):
        response = self.user_api.create_user(email=user_email, password=user_password,
                                             name=user_name)
        result = response.status_code
        result_answer = response.json()
        assert result == 403
        assert result_answer['message'] == "User already exists"

    @pytest.mark.parametrize("email, password, name", [
        (user_email, user_password, None),
        (user_email, None, user_name),
        (None, user_password, user_name)
    ])
    def test_create_user_without_one_required_fields_get_error(self, email, password, name):
        response = self.user_api.create_user(email=email, password=password, name=name)
        result = response.status_code
        assert result == 403
        assert response.json()["message"] == "Email, password and name are required fields"


