import base64
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
        Routes.Products.REF_PRODUCT_ID: product_service.get_detail_by_id,
        Routes.Products.REF_PRODUCTS_BRANDS: product_service.get_brands,
    }
    post_routes = {
        Routes.Products.REF_PRODUCTS: product_service.create,
        Routes.Products.REF_PRODUCT_UPLOAD_IMAGE: product_service.upload_img,
    }

    put_routes = {Routes.Products.REF_PRODUCT_ID: product_service.update}

    verb_paths = {
        HTTPMethods.GET: get_routes,
        HTTPMethods.POST: post_routes,
        HTTPMethods.PUT: put_routes,
    }

    paths = verb_paths.get(verb)
    func = paths.get(resource)

    # get params
    path_params = event.get("pathParameters") if event.get("pathParameters") else {}
    query_params = (
        event.get("queryStringParameters") if event.get("queryStringParameters") else {}
    )
    body = event.get("body", "{}") if event.get("body") else "{}"
    content_type = event["headers"].get("content-type") or event["headers"].get(
        "Content-Type"
    )
    if content_type and "multipart/form-data" in content_type:
        """Upload image"""
        body = {"file": event.get("body", "{}").encode("utf-8")}
    else:
        body = json.loads(body)

    # prepare params
    data = {}
    data.update(path_params)
    data.update(query_params)
    data.update(body)

    # run func
    data = func(**data)
    logger.info("Done")
    return data


if __name__ == "__main__":
    event = {"resource": "/products/init", "method": "POST"}
    event = {
        "resource": Routes.Products.REF_PRODUCT_ID,
        "headers": {"content-type": ""},
        "httpMethod": HTTPMethods.GET,
        "pathParameters": {"productId": 1},
        # "body": json.dumps({"name": "Cau Yonex", "categoryId": 1}),
    }
    rs = lambda_handler(event, None)
    body_rs = json.loads(rs["body"])
    print(json.dumps(body_rs, indent=4))

    # import base64
    #
    # with open("resource/products/vot-cau-long-yonex-arcsaber-2-feel-black-green-chinh-hang_1731868152.webp", "rb") as img_file:
    #     encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    #
    # # print(encoded_string)
    # event = {
    #     "resource": Routes.Products.REF_PRODUCT_UPLOAD_IMAGE,
    #     "headers": {'content-type': "multipart/form-data"},
    #     "httpMethod": HTTPMethods.POST,
    #     "pathParameters": {"productId": 12},
    #     "body": json.dumps(encoded_string),
    # }
    # rs = lambda_handler(event, None)
    # body_rs = json.loads(rs["body"])
    # print(json.dumps(body_rs, indent=4))
    #
    #
