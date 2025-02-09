from src.common.exceptions import AlreadyExist
from src.common.s3_client import S3Client
from src.data_repo.general import BaseRepo
from src.schemas.category import NewCategorySch, UpdateCategorySch
from src.setttings import S3_BUCKET, FILE_PATH_TMP
from src.setttings import logger


class CategoryRepo(BaseRepo):
    def __init__(self):
        super().__init__("categories")
        self.file_path_tmp = f"{FILE_PATH_TMP}{self.file_name}"
        self.s3_client = S3Client(S3_BUCKET)
        self.product_data = []

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

        # update new data to file data
        data_dict = self.get_data()
        data_dict[str(category.id)] = category_dict
        file_data = self.set_file_data(data_dict)

        # upload to s3
        logger.info("Uploading data ...")
        self.s3_client.put_object_content(self.file_name, file_data)
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

        data[str(category.id)] = {"id": category.id, "name": category.name, "parent_id": category.parent_id}
        file_data = self.set_file_data(data)
        self.s3_client.put_object_content(self.file_name, file_data)

        return category.id
