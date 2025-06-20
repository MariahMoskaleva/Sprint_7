import pytest

from api_client.api_wrapper import ApiClient
from utils.courier_factory import register_new_courier_and_return_login_password
from utils.helpers import generate_order_payload


@pytest.fixture
def api_client():
    api_client = ApiClient()
    return api_client


@pytest.fixture
def created_courier(api_client):
    response, creds = register_new_courier_and_return_login_password()
    login_response = api_client.post(path="/api/v1/courier/login", json={"login": creds["login"], "password": creds["password"]})
    courier_id = None
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
    yield creds, courier_id
    if courier_id:
        api_client.delete(f"/api/v1/courier/{courier_id}")


@pytest.fixture
def created_order(api_client):
    payload = generate_order_payload()
    response = api_client.post(path="/api/v1/orders", json=payload)
    track = response.json().get("track")
    yield track
    if track:
        api_client.delete(f"/api/v1/orders/{track}")
