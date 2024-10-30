from base_api.get_order import GetOrderApi
from base_api.login_user import LoginUserAPI
from base_urls import MAIN_URL
from my_data import user_email, user_password


class TestCreateOrder:
    BASE_URL = MAIN_URL
    get_order_api = GetOrderApi(BASE_URL)
    login_api = LoginUserAPI(BASE_URL)

    def test_get_order_user(self):
        login_response = self.login_api.login_user(email=user_email, password=user_password)
        result = login_response.status_code
        assert result == 200
        response_json = login_response.json()
        assert response_json.get("accessToken") is not None, "missing Access token"
        token = response_json.get("accessToken")
        get_order_response = self.get_order_api.get_order(token)
        assert get_order_response.status_code == 200
        assert get_order_response.json().get("success") is True

    def test_get_order_non_auth_user(self):
        get_order_response = self.get_order_api.get_order()
        assert get_order_response.status_code == 401
        assert get_order_response.json().get("message") == "You should be authorised"


