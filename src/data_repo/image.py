from src.common.exceptions import AlreadyExist
from src.common.s3_client import S3Client
from src.data_repo.general import BaseRepo
from src.schemas.db_file_models.models import ImagesTable
from src.schemas.image import NewImageSch, UpdateImageSch
from src.settings import logger


class ImageRepo(BaseRepo):
    def __init__(self):
        super().__init__("images")
        self.s3_client_image = S3Client("www.snail.com")
        self.image_s3_folder = "public"

    def add_new(self, image: NewImageSch) -> int:
        """
        Add new image
        :param image:
        :return:
        """
        # check exist
        if self.check_exist_by_name(image.name):
            raise AlreadyExist(f"Images {image.name} already exist")
        logger.info("Validated data")

        # new data
        image.id = self.get_new_id()
        image_row = ImagesTable(**image.model_dump())
        dict_data = image_row.model_dump()

        # save
        self.upload_data(dict_data)
        logger.info(f"Added new image name {image_row.name}")
        return image_row.id

    def update_data(self, image: UpdateImageSch) -> int | None:
        """ """
        data = self.get_data()
        single_obj = data.get(str(image.id))
        if not single_obj:
            return None

        # check unique
        if self.check_exist_by_name(image.name, image.id):
            raise AlreadyExist(f"Name {image.name} already exist")

        updated_data = ImagesTable(**image.model_dump()).model_dump()
        self.upload_data(updated_data)
        logger.info(f"Updated {image.name}")

        return image.id

    def upload_image(self, image_data_str: bytes, image_name: str):
        self.s3_client_image.put_image(
            f"{self.image_s3_folder}/{image_name}", image_data_str
        )

    def download_image(self, image_name: str) -> bytes:
        """
        I want to return image bytes here
        image_name: just name, not an url
        """
        image_bytes = self.s3_client_image.get_image(
            f"{self.image_s3_folder}/{image_name}"
        )
        return image_bytes

    def remove_image(self, image_name: str):
        """Delete image on s3"""
        self.s3_client_image.remove_image(f"{self.image_s3_folder}/{image_name}")
