import pandas as pd
from src.schemas.match import SearchMatchDetailsSch
from src.data_repo.general import BaseRepo

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
