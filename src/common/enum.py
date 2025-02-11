class ColumnLabel:
    class Product:
        PRODUCT_ID = "productId"

    class Category:
        CATEGORY_ID = "categoryId"

    class Image:
        IMAGE_ID = "imageId"


class Routes:
    class Products:
        REFS_PRODUCT_ID = "/products/{productId}"
        REF_PRODUCTS = "/products"

    class Categories:
        REFS_CATEGORY_ID = "/categories/{categoryId}"
        REF_CATEGORY = "/categories"

    class Images:
        REFS_IMAGE_ID = "/images/{imageId}"
        REF_IMAGE = "/images"


class HTTPMethods:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
