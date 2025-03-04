from src.common.exceptions import AlreadyExist
from src.data_repo.general import BaseRepo
from src.schemas.category import NewCategorySch, UpdateCategorySch
from src.settings import logger


class CategoryRepo(BaseRepo):
    def __init__(self):
        super().__init__("categories")

    def add_new(self, category: NewCategorySch) -> int:
        """
        Add new category
        :param category:
        :return:
        """
        # check exist
        if self.check_exist_by_name(category.name):
            raise AlreadyExist(f"Category {category.name} already exist")
        logger.info("Validated data")

        # new data
        category.id = self.get_new_id()
        category_dict = category.model_dump()

        # save
        self.upload_data(category_dict)
        logger.info(f"Added new category name {category.name}")
        return category.id

    def update_data(self, category: UpdateCategorySch) -> int | None:
        """ """
        data = self.get_data()
        product_obj = data.get(str(category.id))
        if not product_obj:
            return None

        # check unique
        if self.check_exist_by_name(category.name, category.id):
            raise AlreadyExist(f"Name {category.name} already exist")

        updated_data = {
            "id": category.id,
            "name": category.name,
            "parent_id": category.parent_id,
        }
        self.upload_data(updated_data)
        logger.info(f"Updated {category.name}")

        return category.id
