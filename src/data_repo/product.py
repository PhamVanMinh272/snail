import logging

import pandas as pd

from src.common.exceptions import AlreadyExist
from src.data_repo.general import BaseRepo
from src.schemas.db_file_models.models import ProductTable
from src.schemas.product import NewProductSch, UpdateProductSch, SearchSch
from src.common.enum import SortDirections

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ProductRepo(BaseRepo):
    def __init__(self):
        super().__init__("products")
        self.product_data = []

    def search_list(self, search: SearchSch) -> list:
        """Return list"""
        product_df = self.search_as_df(search)
        return product_df.to_dict("records")

    def search_as_df(self, search: SearchSch) -> pd.DataFrame:
        """Search then return df"""
        product_df = self.get_data_as_df()

        if search.category_id:
            product_df = product_df[product_df["category_id"] == search.category_id]
        if search.name:
            product_df = product_df[
                product_df["name"].str.contains(search.name.lower(), case=False)
            ]
        if search.min_price != 0 or search.max_price != 10000000:
            product_df = product_df[
                product_df["price"].between(search.min_price, search.max_price)
            ]
        if search.brand_ids:
            product_df = product_df[product_df["brand_id"].isin(search.brand_ids)]

        # sort
        if search.sort_price:
            logger.info(f"Sort price {search.sort_price}")
            product_df.sort_values(
                by="price",
                ascending=True if search.sort_price == SortDirections.ASC else False,
                inplace=True,
            )

        return product_df

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

        updated_data = ProductTable(**product.model_dump()).model_dump()
        self.upload_data(updated_data)
        logger.info(f"Updated {product.name}")

        return product.id
