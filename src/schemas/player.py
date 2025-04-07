from pydantic import BaseModel, Field
from typing_extensions import Optional


class SearchSch(BaseModel):
 # match_date: Optional[date] = Field(default=None, alias=ColumnLabel.Player.MATCH_DATE)
 limit: Optional[int] = Field(default=20, ge=1)
 page: Optional[int] = Field(default=1, ge=1)
