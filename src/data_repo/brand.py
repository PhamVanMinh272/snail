from src.data_repo.general import BaseRepo


class BrandRepo(BaseRepo):
    def __init__(self):
        super().__init__("brands")
