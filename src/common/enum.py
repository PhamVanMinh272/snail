class ColumnLabel:
    class Product:
        PRODUCT_ID = "productId"

    class Category:
        CATEGORY_ID = "categoryId"


class Routes:
    class Products:
        REFS_PRODUCT_ID = "/products/{productId}"
        REF_PRODUCTS = "/products"

    class Categories:
        REFS_CATEGORY_ID = "/categories/{categoryId}"
        REF_CATEGORY = "/categories"


class HTTPMethods:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
