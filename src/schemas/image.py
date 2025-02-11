from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated, Optional
from src.common.enum import ColumnLabel


def strip_str(s: str):
    return s.strip()


class NewImageSch(BaseModel):
    id: Optional[int] = Field(default=None, alias="id")
    name: Annotated[Optional[str], BeforeValidator(strip_str)] = Field(min_length=1)
    parent_id: int
    parent_type: int  # 1-product


class PathImageSch(BaseModel):
    id: int = Field(alias=ColumnLabel.Image.IMAGE_ID)


class UpdateImageSch(NewImageSch):
    id: int = Field(alias=ColumnLabel.Image.IMAGE_ID)


class SearchSch(BaseModel):
    parent_id: int = Field(default=None)
    parent_type: int = Field(default=None)
