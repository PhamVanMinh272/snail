from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated, Optional
from src.common.enum import ColumnLabel


def strip_str(s: str):
    return s.strip()


class NewProductSch(BaseModel):
    id: Optional[int] = Field(default=None, alias="id")
    name: Annotated[str, BeforeValidator(strip_str)] = Field(min_length=1)
    price: int
    category_id: int = Field(alias=ColumnLabel.Category.CATEGORY_ID)


class PathProductSch(BaseModel):
    id: int = Field(alias=ColumnLabel.Product.PRODUCT_ID)


class UpdateProductSch(NewProductSch):
    id: int = Field(alias=ColumnLabel.Product.PRODUCT_ID)


class UploadImgSch(BaseModel):
    file: bytes
    parent_id: int = Field(alias=ColumnLabel.Product.PRODUCT_ID)
    parent_type: Optional[int] = Field(default=1)


class SearchSch(BaseModel):
    category_id: Optional[int] = Field(default=None, alias=ColumnLabel.Category.CATEGORY_ID)
    name: Annotated[Optional[str], BeforeValidator(strip_str)] = Field(default=None)
    min_price: Optional[int] = Field(default=0, alias=ColumnLabel.Product.MIN_PRICE)
    max_price: Optional[int] = Field(default=10000000, alias=ColumnLabel.Product.MAX_PRICE)
