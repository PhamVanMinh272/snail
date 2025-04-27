from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing_extensions import Annotated, Optional, Literal

from src.common.enum import ColumnLabel, SortDirections


def strip_str(s: str):
    return s.strip()


def parse_list_str_to_number(list_str: list[str]):
    # Convert list of strings to list of integers
    if isinstance(list_str, list):
        try:
            return [int(v) for v in list_str]
        except ValueError:
            raise ValueError("All brand_ids must be integers.")
    return list_str



class NewProductSch(BaseModel):
    id: Optional[int] = Field(default=None, alias="id")
    name: Annotated[str, BeforeValidator(strip_str)] = Field(min_length=1)
    price: int
    category_id: int = Field(alias=ColumnLabel.Category.CATEGORY_ID)
    brand_id: int = Field(alias=ColumnLabel.Brand.BRAND_ID)


class PathProductSch(BaseModel):
    id: int = Field(alias=ColumnLabel.Product.PRODUCT_ID)


class UpdateProductSch(NewProductSch):
    id: int = Field(alias=ColumnLabel.Product.PRODUCT_ID)


class UploadImgSch(BaseModel):
    file: bytes
    parent_id: int = Field(alias=ColumnLabel.Product.PRODUCT_ID)
    parent_type: Optional[int] = Field(default=1)


class SearchSch(BaseModel):
    category_id: Optional[int] = Field(
        default=None, alias=ColumnLabel.Category.CATEGORY_ID
    )
    name: Annotated[Optional[str], BeforeValidator(strip_str)] = Field(default=None)
    brand_ids: Annotated[Optional[list[int]], BeforeValidator(parse_list_str_to_number)] = Field(
        default=[], alias=ColumnLabel.Brand.BRAND_IDS
    )
    min_price: Optional[int] = Field(
        default=0, alias=ColumnLabel.Product.MIN_PRICE, ge=0
    )
    max_price: Optional[int] = Field(
        default=10000000, alias=ColumnLabel.Product.MAX_PRICE
    )
    sort_price: Literal[SortDirections.ASC, SortDirections.DESC, None] = Field(
        default=None, alias=ColumnLabel.Product.SORT_PRICE
    )
    limit: Optional[int] = Field(default=20, ge=1)
    page: Optional[int] = Field(default=1, ge=1)


class BrandResponseSch(BaseModel):
    id: int = Field(ColumnLabel.ID)
    name: str = Field(ColumnLabel.NAME)


class ProductResponseSch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(alias=ColumnLabel.ID)
    name: str = Field(alias=ColumnLabel.NAME)
    price: float = Field(alias=ColumnLabel.Product.PRICE)
    brand: BrandResponseSch = Field(alias=ColumnLabel.Brand.BRAND)
    image: list[dict] = Field(alias=ColumnLabel.Product.IMAGES)


