from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
DEFAULT_HEADERS = {"Content-Type": "application/json"}