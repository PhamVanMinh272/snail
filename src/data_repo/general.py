import copy


class BaseRepo:
    def __init__(self, table_name: str):
        self.init_table_content = {"table_name": table_name, "data": {}}

    def set_file_data(self, data: dict):
        self.init_table_content["data"] = data
        file_data = copy.deepcopy(self.init_table_content)
        file_data["data"] = data
        return file_data
