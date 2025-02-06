import json

from src.common.api_utils import exception_handler
from src.common.enum import Routes, HTTPMethods
from src.services.product import ProductService
from src.setttings import logger


@exception_handler
def lambda_handler(event, context):
    verb = event.get("httpMethod", "GET")
    resource = event.get("resource")
    logger.info(f"Event: {event}")
    logger.info(f"{verb} {resource}")

    product_service = ProductService()
    get_routes = {
        Routes.Products.REF_PRODUCTS: product_service.get_list,
        Routes.Products.REFS_PRODUCT_ID: product_service.get_detail_by_id,
    }
    post_routes = {
        Routes.Products.REF_PRODUCTS: product_service.create,
    }

    put_routes = {Routes.Products.REFS_PRODUCT_ID: product_service.update}

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
        "resource": Routes.Products.REFS_PRODUCT_ID,
        "httpMethod": HTTPMethods.PUT,
        "pathParameters": {"productId": "2"},
        "body": json.dumps({"name": "products 2"}),
    }
    rs = lambda_handler(event, None)
    body_rs = json.loads(rs["body"])
    print(json.dumps(body_rs, indent=4))
