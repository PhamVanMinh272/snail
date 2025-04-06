import logging

import pandas as pd
from jmespath import search

from src.common.exceptions import FileS3NotFound, NotFound
from src.common.utils import timer
from src.data_repo.category import CategoryRepo
from src.data_repo.filter import FilterRepo
from src.data_repo.category_filters import CategoryFilterRepo
from src.schemas.category import NewCategorySch, UpdateCategorySch, PathCategorySch
from src.schemas.filter import FilterResponseSch
from src.services.general import BaseService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CategoryService(BaseService):
    def __init__(self):
        super().__init__()

    @timer
    def get_list(self, **kwargs) -> dict:
        """
        Get all products list
        """
        category_repo = CategoryRepo()
        data = category_repo.get_list()
        return {
            "data": [{"id": i.id, "name": i.name, "parent": i.parent_id} for i in data],
            "count": len(category_repo.get_list()),
            "limit": 20,
            "page": 0,
        }

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
        return {"data": {"id": data.id, "name": data.name, "parent": data.parent_id}}

    @timer
    def create(self, **kwargs) -> dict:
        """
        Create new Product
        """
        logger.info("Creating category ...")
        new_item = NewCategorySch(**kwargs)
        category_repo = CategoryRepo()
        item_id = category_repo.add_new(new_item)
        return {"data": {"id": item_id}}

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
        return {"data": {"id": item_id}}

    def delete(self, **kwargs) -> dict:
        pass

    @staticmethod
    def get_filters(**kwargs) -> dict:
        """Get list filters of a category"""
        category_id = PathCategorySch(**kwargs).id

        filters_df = FilterRepo().get_data_as_df()
        category_filters_df = CategoryFilterRepo().get_data_as_df()

        # filter by category id
        category_filters_df = category_filters_df[category_filters_df["category_id"]==category_id]
        filters_df: pd.DataFrame = filters_df[filters_df["id"].isin(category_filters_df["filter_id"].to_list())]

        response = [
            FilterResponseSch(**row).model_dump()
            for row in filters_df.to_dict(orient="records")
        ]
        return {"data": response}
