import json

from src.common.api_utils import exception_handler
from src.common.enum import Routes, HTTPMethods
from src.services.player import PlayerService
from src.settings import logger


@exception_handler
def lambda_handler(event, context):
    verb = event.get("httpMethod", "GET")
    resource = event.get("resource")
    logger.info(f"Event: {event}")
    logger.info(f"{verb} {resource}")

    service = PlayerService()
    get_routes = {Routes.Players.REF_PLAYER: service.get_list}

    verb_paths = {HTTPMethods.GET: get_routes}

    paths = verb_paths.get(verb)
    func = paths.get(resource)

    # prepare params
    path_params = event.get("pathParameters") if event.get("pathParameters") else {}
    query_params = (
        event.get("queryStringParameters") if event.get("queryStringParameters") else {}
    )
    body = event.get("body", "{}") if event.get("body") else "{}"
    data = {}
    data.update(path_params)
    data.update(query_params)
    data.update(json.loads(body))

    # run func
    data = func(**data)
    logger.info("Done")
    return data


if __name__ == "__main__":
    # event = {
    #     "resource": "/products/init",
    #     "method": "POST"
    # }
    event = {
        "resource": Routes.Players.REF_PLAYER,
        "httpMethod": HTTPMethods.GET,
        "pathParameters": {"categoryId": "5"},
        "queryStringParameters": {"matchDate": "2025-02-18"},
        "body": json.dumps({"name": "Ong Cau long", "parent": None}),
    }
    rs = lambda_handler(event, None)
    body_rs = json.loads(rs["body"])
    print(json.dumps(body_rs, indent=4))
