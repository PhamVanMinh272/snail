class ColumnLabel:
    class Product:
        PRODUCT_ID = "productId"

        # query params
        MIN_PRICE = "minPrice"
        MAX_PRICE = "maxPrice"

    class Category:
        CATEGORY_ID = "categoryId"

    class Image:
        IMAGE_ID = "imageId"

    class Brand:
        BRAND_ID = "brandId"
        BRAND_IDS = "brandIds"

    class Player:
        MATCH_DATE = "matchDate"


class Routes:
    class Products:
        REF_PRODUCT_ID = "/products/{productId}"
        REF_PRODUCT_UPLOAD_IMAGE = "/products/{productId}/upload-img"
        REF_PRODUCTS = "/products"
        REF_PRODUCTS_BRANDS = "/products/brands"

    class Categories:
        REF_CATEGORY_ID = "/categories/{categoryId}"
        REF_CATEGORY = "/categories"

    class Images:
        REF_IMAGE_ID = "/images/{imageId}"
        REF_IMAGE = "/images"

    class Brands:
        REF_BRAND_ID = "/brands/{brandId}"
        REF_BRAND = "/brands"

    class Players:
        REF_PLAYER = "/players"


class HTTPMethods:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
