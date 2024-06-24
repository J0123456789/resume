import os
import logging
import json
from http import HTTPStatus
from azure.cosmos import CosmosClient
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        cosmos_db_connection_string = os.environ.get("COSMOSDB_CONNECTION_STRING")
        if not cosmos_db_connection_string:
            logging.error("COSMOSDB_CONNECTION_STRING environment variable is not set.")
            return func.HttpResponse(
                "COSMOSDB_CONNECTION_STRING environment variable is not set.",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        client = CosmosClient.from_connection_string(conn_str=cosmos_db_connection_string)
        database = client.get_database_client("resume")
        container = database.get_container_client("counter")
        item = container.read_item("1", partition_key="1")
        get_count_value = int(item["count"])
        increment_value = get_count_value + 1
        item["count"] = str(increment_value)
        updated_item = container.upsert_item(item)
        
        return func.HttpResponse(json.dumps(updated_item), status_code=HTTPStatus.OK, headers={"Content-Type": "application/json"})
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return func.HttpResponse("An error occurred", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)