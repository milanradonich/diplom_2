import pytest

from base_api.change_data import ChangeDataApi
from base_urls import MAIN_URL
from helper import create_new_user_and_return_email_password_name
from my_data import new_name, new_email, new_password, user_email, user_name, user_password


class TestChangeData:
    BASE_URL = MAIN_URL
    change_data_api = ChangeDataApi(BASE_URL)

    @pytest.mark.parametrize("email, password, name, expected_status", [
        (new_email, None, None, 200),
        (None, new_password, None, 200),
        (None, None, new_name, 200)
    ])
    def test_change_data_auth_user_return_new_data(self, email, password, name, expected_status):
        status_code, response_data, login_pass = create_new_user_and_return_email_password_name()
        if status_code == 200:
            access_token = response_data.get("accessToken")
            correct_email = response_data['user']['email']
            correct_password = login_pass[1]
            correct_name = response_data['user']['name']
            change_response = self.change_data_api.change_data(
                email=email if email is not None else correct_email,
                password=password if password is not None else correct_password,
                name=name if name is not None else correct_name,
                token=access_token
            )
            assert change_response.status_code == expected_status
            updated_data = change_response.json()
            if name is not None:
                assert updated_data['user']['name'] == name
            if email is not None:
                assert updated_data['user']['email'] == email
            if password is not None:
                pass
        else:
            print("Не удалось создать нового пользователя")

    @pytest.mark.parametrize("email, password, name, expected_status, expected_message", [
        (new_email, user_password, user_name, 401, "You should be authorised"),
        (user_email, new_password, user_name, 401, "You should be authorised"),
        (user_email, user_password, new_name, 401, "You should be authorised")
    ])
    def test_change_data_no_auth_user_return_error(self, email, password, name, expected_status, expected_message):
        change_response = self.change_data_api.change_data(
            email=email,
            password=password,
            name=name
        )
        assert change_response.status_code == expected_status
        assert change_response.json()["message"] == expected_message
