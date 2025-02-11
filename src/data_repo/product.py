import logging
from copy import deepcopy

import botocore

from src.common.exceptions import AlreadyExist
from src.common.s3_client import S3Client
from src.common.utils import DictObj
from src.data_repo.general import BaseRepo
from src.schemas.product import NewProductSch, UpdateProductSch
from src.setttings import S3_BUCKET, FILE_PATH_TMP

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ProductRepo(BaseRepo):
    def __init__(self):
        super().__init__("products")
        self.file_path_tmp = f"{FILE_PATH_TMP}{self.file_name}"
        self.s3_client = S3Client(S3_BUCKET)
        self.product_data = []

    def add_new(self, product: NewProductSch) -> int:
        """
        Add new product
        :param product:
        :return:
        """
        # check exist
        if self.check_exist_by_name(product.name):
            raise AlreadyExist(f"Product {product.name} already exist")
        logger.info("Validated data")

        # new data
        product.id = self.get_new_id()
        product_dict = product.model_dump()

        # save
        self.upload_data(product_dict)
        logger.info(f"Added new product name {product.name}")
        return product.id

    def update_data(self, product: UpdateProductSch) -> int | None:
        """ """
        data = self.get_data()
        product_obj = data.get(str(product.id))
        if not product_obj:
            return None

        # check unique
        if self.check_exist_by_name(product.name, product.id):
            raise AlreadyExist(f"Name {product.name} already exist")

        updated_data = {"id": product.id, "name": product.name, "price": product.price}
        self.upload_data(updated_data)
        logger.info(f"Updated {product.name}")

        return product.id
