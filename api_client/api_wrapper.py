from utils.config import BASE_URL, DEFAULT_HEADERS
import requests
import logging
import allure


class ApiClient:

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.default_headers = DEFAULT_HEADERS

    def _full_url(self, path):
        return f"{self.base_url}{path}"

    def post(self, path: str, json=None, headers=None, **kwargs):
        url = self._full_url(path)
        response = requests.post(url=url, json=json, headers=headers)
        self._log_request_response("POST", url, json, response)
        return response

    def get(self, path: str, headers=None, **kwargs):
        url = self._full_url(path)
        response = requests.get(url=url, headers=headers)
        self._log_request_response("GET", url, None, response)
        return response

    def delete(self, path: str, headers=None, **kwargs):
        url = self._full_url(path)
        response = requests.delete(url=url, headers=headers)
        self._log_request_response("DELETE", url, None, response)
        return response

    def _log_request_response(self, method, url, data, response):
        logging.info(f"{method} {url}")
        if data:
            logging.info(f"Request: {data}")
        logging.info(f"Response [{response.status_code}]: {response.text}")
