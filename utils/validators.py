from pydantic import ValidationError
from models.responses import (
    CreateCourierSuccessResponse,
    CourierLoginResponse,
    CreateOrderResponse,
    GetOrdersResponse,
    BadRequestErrorResponse,
    ConflictErrorResponse,
    NotFoundErrorResponse,
)
import logging


class ResponseValidationError(Exception):
    pass


def validate_response(response, expected_models_by_status: dict):
    """
    Универсальный валидатор: принимает response и словарь моделей по статусу
    Пример:
        validate_response(response, {
            201: CreateCourierSuccessResponse,
            400: BadRequestErrorResponse,
            409: ConflictErrorResponse
        })
    """
    status = response.status_code
    data = response.json()

    model_class = expected_models_by_status.get(status)
    if not model_class:
        raise ResponseValidationError(f"Unexpected status code {status} with body: {data}")

    try:
        return model_class.parse_obj(data)
    except ValidationError as e:
        logging.error(f"Response schema validation error: {e}")
        raise ResponseValidationError(f"Schema validation failed: {e}")
