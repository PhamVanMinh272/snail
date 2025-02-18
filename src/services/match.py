import logging
from datetime import datetime

from src.common.exceptions import NotFound, InvalidData
from src.common.utils import timer
from src.data_repo import MatchRepo
from src.services.general import BaseService
from src.schemas.match import SearchSch

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

        # params
        search_model = SearchSch(**kwargs)
        logger.info(f"Search by: {search_model.model_dump()}")

        match_repo = MatchRepo()
        match_data = match_repo.search_list(search_model)

        response = {
            "data": match_data,
            "count": len(match_repo.get_list()),
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
