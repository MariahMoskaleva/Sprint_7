import random
import string
from datetime import date, timedelta


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_order_payload(color=None):
    return {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "ул. Пушкина, д. 1",
        "metroStation": random.randint(1, 10),
        "phone": "+79999999999",
        "rentTime": random.randint(1, 10),
        "deliveryDate": (date.today() + timedelta(days=2)).isoformat(),
        "comment": "Тест заказ",
        "color": color or []
    }
