import logging
from datetime import datetime

from src.common.exceptions import NotFound, InvalidData
from src.common.utils import timer
from src.data_repo import PlayerRepo, MatchPlayerRepo
from src.services.general import BaseService
from src.schemas.player import SearchSch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PlayerService(BaseService):
    def __init__(self):
        super().__init__()

    @timer
    def get_list(self, **kwargs) -> dict:
        """
        Get all players list
        """

        # params
        search_model = SearchSch(**kwargs)
        logger.info(f"Search by: {search_model.model_dump()}")

        match_player_repo = MatchPlayerRepo()
        match_player_data = match_player_repo.search_list(search_model)

        player_repo = PlayerRepo()
        player_data = player_repo.get_data_as_df()
        player_data.set_index("id")

        data_return = [
            player_data.iloc[i["player_id"]].to_dict()
            for i in match_player_data
        ]

        response = {
            "data": data_return,
            "count": len(match_player_repo.get_list()),
            "limit": search_model.limit,
            "page": search_model.page,
        }
        return response

    def create(self, **kwargs) -> dict:
        pass

    def update(self, **kwargs) -> dict:
        pass

    def delete(self, **kwargs) -> dict:
        pass
