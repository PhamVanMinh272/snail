import logging
from datetime import datetime
from multiprocessing import Pool
from time import sleep


from src.common.enum import ColumnLabel
from src.common.exceptions import NotFound, InvalidData, AlreadyExist
from src.common.utils import timer
from src.data_repo import MatchRepo, MatchPlayerRepo, PlayerRepo
from src.services.general import BaseService
from src.schemas.match import SearchSch, SearchMatchDetailsSch, NewMatchSch
from src.schemas.player import SearchSch as PlayersSearchSch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MatchService(BaseService):
    def __init__(self):
        super().__init__()

    @timer
    def get_list(self, **kwargs) -> dict:
        """
        Get all players list
        """
        pool = Pool(processes=3)

        # params
        search_model = SearchSch(**kwargs)
        logger.info(f"Search by: {search_model.model_dump()}")

        match_repo = MatchRepo()
        match_data = match_repo.search_list(search_model)

        match_player_repo = MatchPlayerRepo()
        pool.map_async(match_player_repo.get_data, ())
        player_repo = PlayerRepo()
        pool.map_async(player_repo.get_data, ())

        for match in match_data:
            # get match details
            search_details_model = SearchMatchDetailsSch(matchDate=match.get("match_date"))
            match_player_data = match_player_repo.search_list(search_details_model)

            player_data = player_repo.get_data_as_df()
            player_data.set_index("id", inplace=True)

            players = [
                player_data.loc[i["player_id"]].to_dict()
                for i in match_player_data
            ]
            match.update({"players": players})

        return_data = [
            {
                "id": match["id"],
                ColumnLabel.Match.MATCH_DATE: match["match_date"],
                ColumnLabel.Match.COURT: match["court"],
                ColumnLabel.Match.PLAYERS: match["players"]
            }
            for match in match_data
        ]
        response = {
            "data": return_data,
            "count": len(match_repo.get_list()),
            "limit": search_model.limit,
            "page": search_model.page,
        }
        return response

    def create(self, **kwargs) -> dict:
        new_match_params = NewMatchSch(**kwargs)

        # check exist by match date
        match_repo = MatchRepo()

        match_df = match_repo.get_data_as_df()
        if not match_df[match_df["match_date"]==new_match_params.match_date.strftime("%Y-%m-%d")].empty:
            raise AlreadyExist(f"Already exist")

        new_match_id = match_repo.add_new(new_match_params)
        return {"data": {"id": new_match_id}}


    def update(self, **kwargs) -> dict:
        pass

    def delete(self, **kwargs) -> dict:
        pass
