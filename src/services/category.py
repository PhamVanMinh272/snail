import logging

from src.common.exceptions import FileS3NotFound, NotFound
from src.common.utils import timer
from src.data_repo.category import CategoryRepo
from src.schemas.category import NewCategorySch, UpdateCategorySch, PathCategorySch
from src.services.general import BaseService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CategoryService(BaseService):
    def __init__(self):
        super().__init__()

    @timer
    def get_list(self, **kwargs) -> list:
        """
        Get all products list
        """
        data = CategoryRepo().get_list()
        return [{"id": i.id, "name": i.name, "parent": i.parent_id} for i in data]

    def get_detail_by_id(self, **kwargs) -> dict:
        """
        Get details by id
        :return:
        """
        item_id = PathCategorySch(**kwargs).id
        category_repo = CategoryRepo()
        data = category_repo.get_detail_by_id(item_id)
        if not data:
            raise NotFound(f"Not found category {item_id}")
        return {"id": data.id, "name": data.name, "parent": data.parent_id}

    @timer
    def create(self, **kwargs) -> dict:
        """
        Create new Product
        """
        logger.info("Creating category ...")
        new_item = NewCategorySch(**kwargs)
        category_repo = CategoryRepo()
        item_id = category_repo.add_new(new_item)
        return {"id": item_id}

    def update(self, **kwargs) -> dict:
        """
        Update a product
        :param kwargs:
        :return:
        """
        logger.info("Updating product ...")
        update_category = UpdateCategorySch(**kwargs)
        category_repo = CategoryRepo()
        item_id = category_repo.update_data(update_category)
        if not item_id:
            logger.info(f"Not found category {update_category.id}")
            raise NotFound(f"Not found category {update_category.id}")
        return {"id": item_id}

    def delete(self, **kwargs) -> dict:
        pass


