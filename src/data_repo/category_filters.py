from src.common.s3_client import S3Client
from src.data_repo.general import BaseRepo
from src.schemas.image import NewImageSch, UpdateImageSch
from src.schemas.db_file_models.models import ImagesTable
from src.common.exceptions import AlreadyExist
from src.settings import logger


class CategoryFilterRepo(BaseRepo):
    def __init__(self):
        super().__init__("attr_category_filters")
