class ColumnLabel:
    ID = "id"
    NAME = "name"

    class Product:
        PRODUCT_ID = "productId"

        PRICE = "price"
        IMAGES = "images"

        # query params
        MIN_PRICE = "minPrice"
        MAX_PRICE = "maxPrice"

        SORT_PRICE = "sortPrice"

    class Category:
        CATEGORY_ID = "categoryId"

    class Image:
        IMAGE_ID = "imageId"

    class Brand:
        BRAND_ID = "brandId"
        BRAND_IDS = "brandIds"

        BRAND = "brand"

    class Match:
        MATCH_DATE = "matchDate"
        COURT = "court"
        PLAYERS = "players"
        MATCH_ID = "matchId"
        PLAYER_IDS = "playerIds"
        IN_COMING_ONLY = "inComingOnly"

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
        REF_CATEGORY_FILTERS = "/categories/{categoryId}/filters"

    class Images:
        REF_IMAGE_ID = "/images/{imageId}"
        REF_IMAGE = "/images"

    class Brands:
        REF_BRAND_ID = "/brands/{brandId}"
        REF_BRAND = "/brands"

    class Players:
        REF_PLAYER = "/players"

    class Matches:
        REF_MATCH = "/matches"
        REF_MATCH_REGISTER = "/matches/{matchId}/register"


class HTTPMethods:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class SortDirections:
    DESC = "desc"
    ASC = "asc"


class ImageParentTypes:
    PRODUCT = 1
