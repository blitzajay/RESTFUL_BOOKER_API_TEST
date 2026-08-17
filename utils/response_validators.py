def assert_status_code(response, expected_status):
    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, "
        f"but received {response.status_code}. "
        f"Response: {response.text}"
    )


def assert_json_content_type(response):
    content_type = response.headers.get("Content-Type", "")

    assert "application/json" in content_type, (
        f"Expected JSON content type, but received: {content_type}"
    )
