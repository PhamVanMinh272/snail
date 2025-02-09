from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated, Optional
from src.common.enum import ColumnLabel


def strip_str(s: str):
    return s.strip()


class NewProductSch(BaseModel):
    id: Optional[int] = Field(default=None, alias="id")
    name: Annotated[str, BeforeValidator(strip_str)] = Field(min_length=1)
    price: int


class PathProductSch(BaseModel):
    id: int = Field(alias=ColumnLabel.Product.PRODUCT_ID)


class UpdateProductSch(NewProductSch):
    id: int = Field(alias=ColumnLabel.Product.PRODUCT_ID)
