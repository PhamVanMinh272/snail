import logging


from src.common.exceptions import AlreadyExist
from src.common.s3_client import S3Client
from src.common.utils import DictObj
from src.data_repo.general import BaseRepo
from src.schemas.product import NewProductSch, UpdateProductSch, SearchSch
from src.schemas.db_file_models.models import ProductTable
from src.setttings import S3_BUCKET, FILE_PATH_TMP

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ProductRepo(BaseRepo):
    def __init__(self):
        super().__init__("products")
        self.file_path_tmp = f"{FILE_PATH_TMP}{self.file_name}"
        self.s3_client = S3Client(S3_BUCKET)
        self.product_data = []


    def search_list(self, search: SearchSch) -> list:
        data_list = self.get_list()
        response = []

        search_fields = {}
        search_dumps = search.model_dump()
        for key, value in search_dumps.items():
            if search_dumps[key]:
                search_fields.update({key: value})

        for i in data_list:
            pass_filter = True
            if search.category_id:
                if i.category_id != search.category_id:
                    pass_filter = False
            if search.name:
                if search.name.lower() not in i.name.lower():
                    pass_filter = False
            if search.min_price !=0 or search.max_price != 10000000:
                if not search.max_price >= i.price >= search.min_price:
                    pass_filter = False

            if pass_filter:
                response.append(i)

        return response

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
