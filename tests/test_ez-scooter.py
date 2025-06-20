import pytest
import allure

from utils.courier_factory import generate_invalid_courier_payload
from utils.validators import validate_response
from utils.helpers import generate_random_string, generate_order_payload
from models.responses import (
    CreateCourierSuccessResponse,
    ConflictErrorResponse,
    BadRequestErrorResponse,
    CourierLoginResponse,
    NotFoundErrorResponse,
    CreateOrderResponse,
    GetOrdersResponse,
)


class TestCreateCourier:
    @allure.step("Create courier successfully")
    def test_create_courier_success(self, created_courier):
        creds, courier_id = created_courier
        assert courier_id is not None

    @allure.step("Try to create courier with existing login")
    def test_create_courier_conflict(self, api_client, created_courier):
        creds, _ = created_courier
        payload = {
            "login": creds["login"],
            "password": creds["password"],
            "firstName": creds.get("firstName", "Test"),
        }
        response = api_client.post(path="/api/v1/courier", json=payload, headers=api_client.default_headers)
        body = validate_response(response, {409: ConflictErrorResponse})
        assert body.message == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize("missing_field", [["login"], ["password"], ["login", "password"]])
    @allure.step("Create courier with missing fields: {missing_field}")
    def test_create_courier_with_missing_fields(self, api_client, missing_field):
        payload = generate_invalid_courier_payload(missing_field)
        response = api_client.post(path="/api/v1/courier", json=payload)
        body = validate_response(response, {400: BadRequestErrorResponse})
        assert body.message == "Недостаточно данных для создания учетной записи"


class TestLoginCourier:
    @allure.step("Successful login returns courier id")
    def test_successful_login_returns_id(self, api_client, created_courier):
        creds, _ = created_courier
        login_payload = {"login": creds["login"], "password": creds["password"]}
        response = api_client.post(path="/api/v1/courier/login", json=login_payload)
        body = validate_response(response, {200: CourierLoginResponse})
        assert isinstance(body.id, int)

    @pytest.mark.parametrize("missing_field", [["login"], ["password"], ["login", "password"]])
    @allure.step("Login with missing fields: {missing_field}")
    def test_login_missing_fields_returns_error(self, api_client, missing_field, created_courier):
        creds, _ = created_courier
        payload = generate_invalid_courier_payload(missing_field, base_creds=creds)
        response = api_client.post(path="/api/v1/courier/login", json=payload)
        body = validate_response(response, {400: BadRequestErrorResponse})
        assert body.message == "Недостаточно данных для входа"

    @allure.step("Login with wrong password")
    def test_login_with_wrong_password(self, api_client, created_courier):
        creds, _ = created_courier
        password = generate_random_string()
        payload = {"login": creds["login"], "password": password}
        response = api_client.post(path="/api/v1/courier/login", json=payload)
        body = validate_response(response, {404: NotFoundErrorResponse})
        assert body.message == "Учетная запись не найдена"

    @allure.step("Login with nonexistent user")
    def test_login_with_nonexistent_user(self, api_client):
        login = generate_random_string()
        password = generate_random_string()
        payload = {"login": login, "password": password}
        response = api_client.post(path="/api/v1/courier/login", json=payload)
        body = validate_response(response, {404: NotFoundErrorResponse})
        assert body.message == "Учетная запись не найдена"


class TestCreateOrder:
    @pytest.mark.parametrize("colors", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    @allure.step("Create order with colors: {colors}")
    def test_create_order_with_various_colors(self, api_client, colors, created_order):
        payload = generate_order_payload(color=colors)
        response = api_client.post(path="/api/v1/orders", json=payload)
        body = validate_response(response, {201: CreateOrderResponse})
        assert isinstance(body.track, int)


class TestGetOrders:
    @allure.step("Get orders list")
    def test_get_orders_returns_list(self, api_client):
        response = api_client.get(path="/api/v1/orders")
        body = validate_response(response, {200: GetOrdersResponse})
        assert isinstance(body.orders, list)
