from datetime import date
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated, Optional
from src.common.enum import ColumnLabel


class SearchSch(BaseModel):
 # match_date: Optional[date] = Field(default=None, alias=ColumnLabel.Player.MATCH_DATE)
 in_coming_only: bool = Field(default=True, alias=ColumnLabel.Match.IN_COMING_ONLY)
 limit: Optional[int] = Field(default=5, ge=1)
 page: Optional[int] = Field(default=1, ge=1)

class SearchMatchDetailsSch(BaseModel):
    match_date: Optional[date] = Field(default=None, alias=ColumnLabel.Player.MATCH_DATE)


class NewMatchSch(BaseModel):
    id: Optional[int] = Field(default=None)
    match_date: date = Field(alias=ColumnLabel.Player.MATCH_DATE)
    court: str


class NewMatchPlayerSch(BaseModel):
    player_id: int
    match_date: date = Field(default=None, alias=ColumnLabel.Player.MATCH_DATE)


class MatchRegisterSch(BaseModel):
    match_id: int = Field(alias=ColumnLabel.Match.MATCH_ID)
    player_ids: list[int] = Field(alias=ColumnLabel.Match.PLAYER_IDS)
