import pandas as pd
from datetime import date

from src.common.exceptions import AlreadyExist
from src.schemas.match import SearchMatchDetailsSch, NewMatchPlayerSch
from src.data_repo.general import BaseRepo
from src.common.config import DATE_STR_FORMAT
from src.schemas.db_file_models.models import MatchPlayerTable
from src.settings import logger

class MatchPlayerRepo(BaseRepo):
    def __init__(self):
        super().__init__("match_player")

    def search_list(self, search: SearchMatchDetailsSch):
        players_df = self.get_data_as_df()
        if search.match_date:
            players_df = players_df[players_df["match_date"] == search.match_date.strftime(format="%Y-%m-%d")]
        return players_df.to_dict(orient="records")

    def get_list(self):
        return self.data.values()

    def add_new_list(self, match_date: str, player_ids: list[int]):

        self.get_data()
        new_data = []
        for i in player_ids:
            key = f"{match_date}-{i}"
            if self.data.get(key):
                raise AlreadyExist(f"Player {i} already register")
            new_data.append(MatchPlayerTable(id=key, player_id=i, match_date=match_date).model_dump())

        # save
        self.upload_list_data(new_data)
        logger.info(f"Added new players to match {match_date}")
        return 1
