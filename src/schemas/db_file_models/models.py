from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated, Optional
from src.common.enum import ColumnLabel


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
