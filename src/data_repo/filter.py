from src.data_repo.general import BaseRepo


class FilterRepo(BaseRepo):
    def __init__(self):
        super().__init__("ref_filters")
