import os
import json
import requests
from azure.functions import HttpRequest
from function_app import main
import pytest

def test_function_app():
    cosmos_db_connection_string = os.environ.get("COSMOSDB_CONNECTION_STRING")
   # Check if cosmos_db_connection_string is set 
    if not cosmos_db_connection_string:
        raise ValueError("COSMOSDB_CONNECTION_STRING environment variable is not set.")

    # Simulate an HTTP GET request
    req = HttpRequest(method="GET", url="/api/main", body=None, headers={}, params={})
    response = main(req)

    # Assert the response status code
    assert response.status_code == 200, "Expected HTTP status code 200 OKAY"

    # Assert the response content type
    assert response.headers["Content-Type"] == "application/json", "Expected Content-Type to be application/json"

    # Assert the count has been incremented assuming count is greater than 0
    response_body = json.loads(response.get_body())
    assert "count" in response_body, "Response body should contain 'count'"
    new_count = int(response_body["count"])
    assert new_count > 0, "Count should be greater than 0"