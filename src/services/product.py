import logging
import uuid

from src.common.exceptions import FileS3NotFound, NotFound
from src.common.utils import timer
from src.data_repo.product import ProductRepo
from src.data_repo.image import ImageRepo
from src.schemas.product import NewProductSch, UpdateProductSch, PathProductSch, UploadImgSch
from src.schemas.image import NewImageSch
from src.services.general import BaseService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ProductService(BaseService):
    def __init__(self):
        super().__init__()

    @timer
    def get_list(self, **kwargs) -> list:
        """
        Get all products list
        """
        data = ProductRepo().get_list()
        all_img = ImageRepo().get_list()
        img_dict = {}
        for i in all_img:
            img_dict.update({
                i.parent_id: {
                    "id": i.id,
                    "name": i.name
                }
            })
        response = [
            {"id": i.id, "name": i.name, "price": i.price, "image": img_dict.get(i.id)} for i in data]
        return response

    def get_detail_by_id(self, **kwargs) -> dict:
        """
        Get details by id
        :return:
        """
        product_id = PathProductSch(**kwargs).id
        product_repo = ProductRepo()
        data = product_repo.get_detail_by_id(product_id)
        if not data:
            raise NotFound(f"Not found product {product_id}")
        return {"id": data.id, "name": data.name, "price": data.price}

    @timer
    def create(self, **kwargs) -> dict:
        """
        Create new Product
        """
        logger.info("Creating product ...")
        new_product = NewProductSch(**kwargs)
        product_repo = ProductRepo()
        product_id = product_repo.add_new(new_product)
        return {"id": product_id}

    def update(self, **kwargs) -> dict:
        """
        Update a product
        :param kwargs:
        :return:
        """
        logger.info("Updating product ...")
        update_product = UpdateProductSch(**kwargs)
        product_repo = ProductRepo()
        product_id = product_repo.update_data(update_product)
        if not product_id:
            logger.info(f"Not found product {update_product.id}")
            raise NotFound(f"Not found product {update_product.id}")
        return {"id": product_id}

    def delete(self, **kwargs) -> dict:
        pass

    def upload_img(self, **kwargs):
        logger.info("Creating image ...")
        new_upload = UploadImgSch(**kwargs)

        # update data
        img_name = f"{uuid.uuid4()}.jpg"
        img_repo = ImageRepo()
        new_img = NewImageSch(
            name=img_name,
            parent_id=new_upload.parent_id,
            parent_type=new_upload.parent_type
        )
        item_id = img_repo.add_new(new_img)

        # upload image
        img_repo.upload_image(kwargs.get("file"), img_name)
