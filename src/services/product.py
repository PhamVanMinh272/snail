import logging
from datetime import datetime

from src.common.exceptions import NotFound, InvalidData
from src.common.utils import timer
from src.data_repo import CategoryRepo, ProductRepo, ImageRepo, BrandRepo
from src.schemas.image import NewImageSch
from src.schemas.product import (
    NewProductSch,
    UpdateProductSch,
    PathProductSch,
    UploadImgSch,
    SearchSch,
    ProductResponseSch,
)
from src.services.general import BaseService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ProductService(BaseService):
    def __init__(self):
        super().__init__()

    @timer
    def get_list(self, **kwargs) -> dict:
        """
        Get all products list
        """

        # params
        search_model = SearchSch(**kwargs)

        product_repo = ProductRepo()
        products = product_repo.search_list(search_model)

        all_img_df = ImageRepo().get_data_as_df()
        brands_df = BrandRepo().get_data_as_df()
        data_return = [
            ProductResponseSch(
                **i,
                brand=brands_df[brands_df["id"] == i["brand_id"]].iloc[0].to_dict(),
                image=all_img_df[all_img_df["parent_id"] == i["id"]]
                .sort_values(by=["id"], ascending=False)
                .to_dict(orient="records"),
            ).model_dump(by_alias=True)
            for i in products
        ]

        response = {
            "data": data_return,
            "count": len(data_return),
            "limit": search_model.limit,
            "page": search_model.page,
        }
        return response

    def get_detail_by_id(self, **kwargs) -> dict:
        """
        Get details by id
        :return:
        """
        product_id = PathProductSch(**kwargs).id
        product_repo = ProductRepo()
        data = product_repo.get_detail_by_id(product_id)
        category_df = CategoryRepo().get_data_as_df()
        all_img_df = ImageRepo().get_data_as_df()
        brands_df = BrandRepo().get_data_as_df()
        if not data:
            raise NotFound(f"Not found product {product_id}")
        return {
            "data": {
                "id": data.id,
                "name": data.name,
                "price": data.price,
                "images": all_img_df[
                    (all_img_df["parent_id"] == data.id)
                    & (all_img_df["parent_type"] == 1)
                ].to_dict(orient="records"),
                "brand": brands_df[brands_df["id"] == data.brand_id].iloc[0].to_dict(),
                "category": category_df[category_df["id"] == data.category_id]
                .iloc[0]
                .to_dict(),
            }
        }

    @timer
    def create(self, **kwargs) -> dict:
        """
        Create new Product
        """
        logger.info("Creating product ...")
        new_product = NewProductSch(**kwargs)
        product_repo = ProductRepo()

        # check category exist
        category_repo = CategoryRepo()
        category = category_repo.get_detail_by_id(new_product.category_id)
        if not category:
            raise InvalidData(f"Category {new_product.category_id} doesn't exist")

        product_id = product_repo.add_new(new_product)
        return {"data": {"id": product_id}}

    def update(self, **kwargs) -> dict:
        """
        Update a product
        :param kwargs:
        :return:
        """
        logger.info("Updating product ...")
        update_product = UpdateProductSch(**kwargs)
        product_repo = ProductRepo()

        # check category exist
        category_repo = CategoryRepo()
        category = category_repo.get_detail_by_id(update_product.category_id)
        if not category:
            raise InvalidData(f"Category {update_product.category_id} doesn't exist")

        product_id = product_repo.update_data(update_product)
        if not product_id:
            logger.info(f"Not found product {update_product.id}")
            raise NotFound(f"Not found product {update_product.id}")
        return {"data": {"id": product_id}}

    def delete(self, **kwargs) -> dict:
        pass

    def upload_img(self, **kwargs):
        logger.info("Creating image ...")
        new_upload = UploadImgSch(**kwargs)

        # update data
        img_name = f"product_{new_upload.parent_id}_{datetime.utcnow().strftime(format='%Y-%m-%dT%H:%M:%SZ')}.jpg"
        img_repo = ImageRepo()
        new_img = NewImageSch(
            name=img_name,
            parent_id=new_upload.parent_id,
            parent_type=new_upload.parent_type,
        )
        item_id = img_repo.add_new(new_img)

        # upload image
        img_repo.upload_image(kwargs.get("file"), img_name)
        return {"data": {"id": item_id}}

    def get_brands(self, **kwargs):
        brands_df = BrandRepo().get_data_as_df()
        # products_df = ProductRepo().get_data_as_df()

        # products_df.merge(brands_df, how="left", left_on="brand_id", right_on="id")

        return {"data": brands_df.to_dict(orient="records")}
