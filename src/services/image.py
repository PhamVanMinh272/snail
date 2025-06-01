import logging
import uuid
from io import BytesIO

import botocore

from src.common.exceptions import NotFound, InvalidData
from src.common.utils import timer
from src.data_repo.image import ImageRepo
from src.schemas.image import (
    NewImageSch,
    UpdateImageSch,
    PathImageSch,
    ImageNamePathSch,
    ImageDeletionSch,
)
from src.services.general import BaseService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ImageService(BaseService):
    def __init__(self):
        super().__init__()

    @timer
    def get_list(self, **kwargs) -> list:
        """
        Get all products list
        """
        data = ImageRepo().get_list()
        return [{"id": i.id, "name": i.name, "parent": i.parent_id} for i in data]

    def get_detail_by_id(self, **kwargs) -> dict:
        """
        Get details by id
        :return:
        """
        item_id = PathImageSch(**kwargs).id
        category_repo = ImageRepo()
        data = category_repo.get_detail_by_id(item_id)
        if not data:
            raise NotFound(f"Not found category {item_id}")
        return {"id": data.id, "name": data.name, "parent": data.parent_id}

    def get_image_by_name(self, **kwargs) -> bytes:
        """
        name: image name
        """
        image_name = ImageNamePathSch(**kwargs).name
        image_repo = ImageRepo()
        try:
            image_bytes = image_repo.download_image(image_name)
            return image_bytes
        except botocore.errorfactory.NoSuchKey as e:
            logger.exception(e)
            raise InvalidData("Image not found")

    @timer
    def create(self, **kwargs) -> dict:
        """
        Create new image
        """
        logger.info("Creating image ...")
        new_item = NewImageSch(**kwargs)

        # update data
        new_item.name = f"{uuid.uuid4()}.jpg"
        repo = ImageRepo()
        item_id = repo.add_new(new_item)

        # upload image
        repo.upload_image(new_item.image, new_item.name)

        return {"id": item_id}

    def update(self, **kwargs) -> dict:
        """
        Update a product
        :param kwargs:
        :return:
        """
        logger.info("Updating image ...")
        update_data = UpdateImageSch(**kwargs)
        repo = ImageRepo()
        item_id = repo.update_data(update_data)
        if not item_id:
            logger.info(f"Not found image {update_data.id}")
            raise NotFound(f"Not found image {update_data.id}")
        return {"id": item_id}

    def delete(self, **kwargs) -> dict:
        """
        Delete an image on Db and s3
        """
        params = ImageDeletionSch(**kwargs)
        img_repo = ImageRepo()
        if params.id:
            key_id = params.id
            img = img_repo.get_detail_by_id(key_id)
            img_name = img.name
        elif params.name:
            img_df = img_repo.get_data_as_df()
            img = img_df.loc[img_df["name"] == params.name][0].to_dict()
            key_id = img["id"]
            img_name = params.name
        else:
            raise InvalidData("Id or name required")

        # delete record
        img_repo.delete_by_id(key_id)

        # delete on s3
        img_repo.remove_image(img_name)
        return {"data": None}
