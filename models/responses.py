from pydantic import BaseModel, conint
from typing import List, Optional


class CreateCourierSuccessResponse(BaseModel):
    ok: bool


class CourierLoginResponse(BaseModel):
    id: int


class CreateOrderResponse(BaseModel):
    track: int


class Order(BaseModel):
    id: int
    firstName: Optional[str]
    lastName: Optional[str]
    address: Optional[str]
    metroStation: Optional[str]
    phone: Optional[str]
    rentTime: Optional[int]
    deliveryDate: Optional[str]
    track: Optional[int]
    status: Optional[int]
    color: Optional[List[str]]


class GetOrdersResponse(BaseModel):
    orders: List[Order]


class BadRequestErrorResponse(BaseModel):
    message: str  # Пример: "Недостаточно данных для создания учетной записи"


class NotFoundErrorResponse(BaseModel):
    message: str  # Пример: "Учетная запись не найдена"


class ConflictErrorResponse(BaseModel):
    message: str  # Пример: "Этот логин уже используется. Попробуйте другой."
