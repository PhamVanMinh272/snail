import pandas as pd


from src.data_repo.general import BaseRepo
from src.schemas.player import SearchSch
from src.settings import logger


class PlayerRepo(BaseRepo):
    def __init__(self):
        super().__init__("players")
        self.data = {
            "1": {
                "id": 1,
                "name": "Minh"
            },
            "2": {
                "id": 2,
                "name": "Đạt"
            },
            "3": {
                "id": 3,
                "name": "Tuyến"
            },
            "4": {
                "id": 4,
                "name": "Văn"
            },
            "5": {
                "id": 5,
                "name": "Thảo"
            },
            "6": {
                "id": 6,
                "name": "Tú"
            },
            "7": {
                "id": 7,
                "name": "Thư"
            },
            "8": {
                "id": 8,
                "name": "Thịnh"
            },
            "9": {
                "id": 9,
                "name": "Nam"
            },
            "10": {
                "id": 10,
                "name": "Thi"
            }
        }

    def get_list(self):
        return self.data.values()
