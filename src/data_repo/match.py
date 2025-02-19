import pandas as pd
from datetime import date
from src.schemas.match import SearchSch, NewMatchSch
from src.data_repo.general import BaseRepo
from src.schemas.db_file_models.models import MatchTable
from src.setttings import logger

class MatchRepo(BaseRepo):
    def __init__(self):
        super().__init__("matches")

    def search_list(self, search: SearchSch):
        matches_df = self.get_data_as_df()
        matches_df['match_date'] = pd.to_datetime(matches_df['match_date']).dt.date
        matches_df = matches_df[matches_df["match_date"]>= date.today()]
        matches_df.sort_values("match_date", inplace=True)
        matches_df = matches_df.head(search.limit)
        matches_df['match_date'] = matches_df['match_date'].astype(str)
        return matches_df.to_dict(orient="records")

    def get_list(self):
        return self.data.values()

    def add_new(self, match: NewMatchSch) -> int:
        """
        Add new match
        :param match:
        :return:
        """
        # new data
        match.id = self.get_new_id()
        match_dict = match.model_dump()

        match_row = MatchTable(**match_dict)

        # save
        self.upload_data(match_row.model_dump())
        logger.info(f"Added new product name {match_row.match_date}")
        return match_row.id
