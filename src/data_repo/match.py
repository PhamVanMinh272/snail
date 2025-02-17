import pandas as pd
from src.schemas.player import SearchSch
from src.data_repo.general import BaseRepo

class MatchRepo(BaseRepo):
    def __init__(self):
        super().__init__("matches")

    def search_list(self, search: SearchSch):
        players_df = pd.DataFrame(self.data.values())
        return players_df.to_dict(orient="records")

    def get_list(self):
        return self.data.values()
