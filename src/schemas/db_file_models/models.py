from datetime import date

from pydantic import BaseModel, Field, field_serializer
from typing_extensions import Optional

from src.common.config import DATE_STR_FORMAT


class ImagesTable(BaseModel):
    id: int
    name: str
    parent_id: int
    parent_type: int


class ProductTable(BaseModel):
    id: int
    name: str
    price: int
    category_id: int
    brand_id: int


class CategoryTable(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = Field(default=None)


class MatchTable(BaseModel):
    id: int
    match_date: date

    @field_serializer("match_date")
    def serialize_match_date(self, match_date: date, _info):
        return match_date.strftime(DATE_STR_FORMAT)


class MatchPlayerTable(BaseModel):
    id: str
    player_id: int
    match_date: date

    @field_serializer("match_date")
    def serialize_match_date(self, match_date: date, _info):
        return match_date.strftime(DATE_STR_FORMAT)
