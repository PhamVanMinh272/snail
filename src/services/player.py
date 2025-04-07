import logging

from src.common.utils import timer
from src.data_repo import PlayerRepo
from src.schemas.player import SearchSch
from src.services.general import BaseService

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

        player_repo = PlayerRepo()
        player_df = player_repo.get_data_as_df()

        data_return = [
            {
                "id": row["id"],
                "name": row["name"]
            }
            for _, row in player_df.iterrows()
        ]

        response = {
            "data": data_return,
            "count": len(player_repo.get_list()),
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
