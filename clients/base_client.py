import logging

import requests

from config.settings import BASE_URL, DEFAULT_TIMEOUT


logger = logging.getLogger(__name__)

SENSITIVE_KEYS = {
    "authorization",
    "cookie",
    "password",
    "set-cookie",
    "token",
}

MAX_LOG_LIST_ITEMS = 10
MAX_LOG_TEXT_LENGTH = 1000


def _redact_sensitive_data(value):
    if isinstance(value, dict):
        return {
            key: "***REDACTED***"
            if str(key).lower() in SENSITIVE_KEYS
            else _redact_sensitive_data(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        visible_items = [
            _redact_sensitive_data(item)
            for item in value[:MAX_LOG_LIST_ITEMS]
        ]

        if len(value) > MAX_LOG_LIST_ITEMS:
            visible_items.append(f"... {len(value) - MAX_LOG_LIST_ITEMS} more items")

        return visible_items

    if isinstance(value, str) and len(value) > MAX_LOG_TEXT_LENGTH:
        return f"{value[:MAX_LOG_TEXT_LENGTH]}... [truncated]"

    return value


class BaseClient:

    def __init__(self, base_url=BASE_URL, timeout=DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        timeout = kwargs.pop("timeout", self.timeout)

        request_details = {
            "params": kwargs.get("params"),
            "json": kwargs.get("json"),
            "headers": kwargs.get("headers"),
            "cookies": kwargs.get("cookies"),
        }

        logger.info(
            "API request: %s %s | details=%s",
            method.upper(),
            url,
            _redact_sensitive_data(request_details),
        )

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=timeout,
                **kwargs,
            )
        except requests.RequestException:
            logger.exception("API request failed: %s %s", method.upper(), url)
            raise

        try:
            response_body = response.json()
        except requests.JSONDecodeError:
            response_body = response.text[:1000]

        logger.info(
            "API response: %s %s | status=%s | duration=%.3fs | body=%s",
            method.upper(),
            response.url,
            response.status_code,
            response.elapsed.total_seconds(),
            _redact_sensitive_data(response_body),
        )

        return response

    def close(self):
        self.session.close()
