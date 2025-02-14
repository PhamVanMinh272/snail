import copy
import pandas as pd
from src.setttings import logger
import botocore
from src.common.s3_client import S3Client
from src.setttings import S3_BUCKET, FILE_PATH_TMP
from src.common.utils import DictObj



class BaseRepo:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.init_table_content = {"table_name": table_name, "data": {}}
        self.data = {}
        self.s3_client = S3Client(S3_BUCKET)
        self.file_name = f"{table_name}.json"
        self.file_path_tmp = f"{FILE_PATH_TMP}{self.file_name}"
        self.s3_client = S3Client(S3_BUCKET)

    def set_file_data(self, data: dict):
        self.init_table_content["data"] = data
        file_data = copy.deepcopy(self.init_table_content)
        file_data["data"] = data
        return file_data

    def get_data(self) -> dict:
        """
        Get all data
        :return:
        """
        try:
            logger.info(f"Get all {self.table_name} data ...")
            if not self.data:
                self.data = self.s3_client.get_object_content(self.file_name)
            return copy.deepcopy(self.data)
        except botocore.exceptions.ClientError as e:
            return {}
            # raise FileS3NotFound(f"Not found files {self.file_name} in S3")

    def get_list(self) -> list:
        """
        Get all products list
        """
        try:
            logger.info(f"Get list {self.table_name} ...")
            self.get_data()
            data_list = [DictObj(p) for p in self.data.values()]
            return data_list
        except botocore.exceptions.ClientError as e:
            return []
            # raise FileS3NotFound(f"Not found files {self.file_name} in S3")

    def get_data_as_df(self):
        """Return data as a Dataframe"""
        self.get_data()
        return pd.DataFrame(self.data.values())

    def get_detail_by_id(self, item_id: int):
        """
        Get detail by id
        :param item_id:
        :return:
        """

        data = self.get_data()
        item = data.get(str(item_id))
        return DictObj(item)

    def check_exist_by_name(self, name: str, item_id: int = None):
        """
        Return True if name already exist
        :param name: product name
        :param item_id: provide id if we want to check for updating purpose
        """
        data = self.get_data()
        data = list(data.values())
        for i in data:
            if i["name"] == name and (item_id is None or item_id != i["id"]):
                return True
        return False

    def get_new_id(self):
        """
        Return new id for insert
        """
        data_dict = self.get_data()
        ids = [int(i) for i in data_dict.keys()]
        if not ids:
            return 1
        return max(ids) + 1

    def upload_data(self, single_data: dict):
        key_id = single_data.get("id") or self.get_new_id()
        # update new data to file data
        data_dict = self.get_data()
        data_dict[str(key_id)] = single_data
        file_data = self.set_file_data(data_dict)

        # upload to s3
        logger.info("Uploading data ...")
        self.s3_client.put_object_content(self.file_name, file_data)
