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
        self.table_name = "products"
        self.file_name = f"{self.table_name}.json"
        self.file_path_tmp = f"{FILE_PATH_TMP}{self.file_name}"
        self.s3_client = S3Client(S3_BUCKET)
        self.product_data = []
        super().__init__(self.table_name)

    def get_list(self) -> list:
        """
        Get all products list
        """
        try:
            logger.info("Get list products ...")
            if not self.product_data:
                self.product_data = self.s3_client.get_object_content(self.file_name)
            products_list = [DictObj(p) for p in self.product_data.values()]
            return products_list
        except botocore.exceptions.ClientError as e:
            return []
            # raise FileS3NotFound(f"Not found files {self.file_name} in S3")

    def get_data(self) -> dict:
        """
        Get all product data
        :return:
        """
        try:
            logger.info("Get all products data ...")
            if not self.product_data:
                self.product_data = self.s3_client.get_object_content(self.file_name)
            return deepcopy(self.product_data)
        except botocore.exceptions.ClientError as e:
            return {}
            # raise FileS3NotFound(f"Not found files {self.file_name} in S3")

    def get_detail_by_id(self, product_id: int):
        """
        Get detail by id
        :param product_id:
        :return:
        """

        data = self.get_data()
        product = data.get(str(product_id))
        return DictObj(product)

    def check_exist_by_name(self, name: str, product_id: int = None):
        """
        Return True if name already exist
        :param name: product name
        :param product_id: provide id if we want to check for updating purpose
        """
        data = self.get_data()
        data = list(data.values())
        for i in data:
            if i["name"] == name and (product_id is None or product_id != i["id"]):
                return True
        return False

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
        product.id = self._get_new_id()
        product_dict = product.model_dump()

        # update new data to file data
        data_dict = self.get_data()
        data_dict[str(product.id)] = product_dict
        file_data = self.set_file_data(data_dict)

        # upload to s3
        logger.info("Uploading data ...")
        self.s3_client.put_object_content(self.file_name, file_data)
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

        data[str(product.id)] = {"id": product.id, "name": product.name}
        file_data = self.set_file_data(data)
        self.s3_client.put_object_content(self.file_name, file_data)

        return product.id

    def _get_new_id(self):
        """
        Return new id for insert
        """
        data_dict = self.get_data()
        ids = [int(i) for i in data_dict.keys()]
        if not ids:
            return 1
        return max(ids) + 1
