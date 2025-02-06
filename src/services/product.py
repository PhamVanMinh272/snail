import logging

from src.common.exceptions import FileS3NotFound, NotFound
from src.common.utils import timer
from src.data_repo.product import ProductRepo
from src.schemas.product import NewProductSch, UpdateProductSch, PathProductSch
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
        return [{"id": i.id, "name": i.name} for i in data]

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
        return {"id": data.id, "name": data.name}

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
