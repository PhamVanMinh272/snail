import json


def make_success_response(body: dict, status_code: int = 200):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",  ## Allow from anywhere
            "Access-Control-Allow-Methods": "*",  ## Allow only GET request,
            "Content-Type": "application/json; charset=utf-8",
            "Cache-Control": "max-age=3600",
        },
        "body": json.dumps(body, ensure_ascii=False),
    }


def make_error_response(message: str, status_code: int = 500):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",  ## Allow from anywhere
            "Access-Control-Allow-Methods": "GET",  ## Allow only GET request
        },
        "body": json.dumps({"message": message}),
    }
