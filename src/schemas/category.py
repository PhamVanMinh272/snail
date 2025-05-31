from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated, Optional

from src.common.enum import ColumnLabel


def strip_str(s: str):
    return s.strip()


class NewCategorySch(BaseModel):
    id: Optional[int] = Field(default=None, alias="id")
    name: Annotated[str, BeforeValidator(strip_str)] = Field(min_length=1)
    parent_id: Optional[int] = Field(default=None)


class PathCategorySch(BaseModel):
    id: int = Field(alias=ColumnLabel.Category.CATEGORY_ID)


class UpdateCategorySch(NewCategorySch):
    id: int = Field(alias=ColumnLabel.Category.CATEGORY_ID)


class CategoryResSch(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = Field(default=None, alias="parentId")
