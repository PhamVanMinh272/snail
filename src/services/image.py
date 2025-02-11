import base64
import logging
import uuid

from src.common.exceptions import FileS3NotFound, NotFound
from src.common.utils import timer
from src.data_repo.image import ImageRepo
from src.schemas.image import NewImageSch, UpdateImageSch, PathImageSch
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
        pass


