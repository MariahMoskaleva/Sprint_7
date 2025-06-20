import random
import string

from pydantic import ValidationError

from models.responses import CreateCourierSuccessResponse
from api_client.api_wrapper import ApiClient
import logging


def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    api_client = ApiClient()
    response = api_client.post(path="/api/v1/courier", json=payload, headers=api_client.default_headers)

    if response.status_code == 201:
        try:
            body = CreateCourierSuccessResponse.parse_obj(response.json())
            logging.info(f"Created courier. Status: {response.status_code}, Response: {body}")
            creds = {
                "login": login,
                "password": password,
                "first_name": first_name
            }
            return response, creds
        except ValidationError as e:
            logging.error(f"Response schema validation failed: {e}")
            return response, None
    else:
        logging.error(f"Courier creation failed: {response.status_code}, {response.text}")
        return response, None


def generate_invalid_courier_payload(missing_fields: list[str], base_creds: dict[str, str] = None):
    import random
    import string

    def generate_random_string(length):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    if base_creds:
        payload = {
            "login": base_creds.get("login"),
            "password": base_creds.get("password")
        }
    else:
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

    for field in missing_fields:
        payload.pop(field, None)

    return payload

