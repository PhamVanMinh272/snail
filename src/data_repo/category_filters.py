from src.data_repo.general import BaseRepo


class CategoryFilterRepo(BaseRepo):
    def __init__(self):
        super().__init__("attr_category_filters")
