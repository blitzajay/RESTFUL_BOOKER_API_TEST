import os

BASE_URL = os.getenv(
    "BOOKER_BASE_URL",
    "https://restful-booker.herokuapp.com",
)

DEFAULT_TIMEOUT = int(
    os.getenv("BOOKER_TIMEOUT", "10")
)
