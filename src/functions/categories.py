import json

from src.common.api_utils import exception_handler
from src.common.enum import Routes, HTTPMethods
from src.services.category import CategoryService
from src.settings import logger


@exception_handler
def lambda_handler(event, context):
    verb = event.get("httpMethod", "GET")
    resource = event.get("resource")
    logger.info(f"Event: {event}")
    logger.info(f"{verb} {resource}")

    category_service = CategoryService()
    get_routes = {
        Routes.Categories.REF_CATEGORY: category_service.get_list,
        Routes.Categories.REF_CATEGORY_ID: category_service.get_detail_by_id,
        Routes.Categories.REF_CATEGORY_FILTERS: category_service.get_filters
    }
    post_routes = {
        Routes.Categories.REF_CATEGORY: category_service.create,
    }

    put_routes = {Routes.Categories.REF_CATEGORY_ID: category_service.update}

    verb_paths = {
        HTTPMethods.GET: get_routes,
        HTTPMethods.POST: post_routes,
        HTTPMethods.PUT: put_routes,
    }

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
        "resource": Routes.Categories.REF_CATEGORY_FILTERS,
        "httpMethod": HTTPMethods.GET,
        "pathParameters": {"categoryId": "1"},
        "body": json.dumps({"name": "Ong Cau long", "parent": None}),
    }
    rs = lambda_handler(event, None)
    body_rs = json.loads(rs["body"])
    print(json.dumps(body_rs, indent=4))
