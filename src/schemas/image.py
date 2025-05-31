from pydantic import BaseModel, Field, BeforeValidator, model_validator
from typing_extensions import Annotated, Optional, Self

from src.common.enum import ColumnLabel
from src.settings import S3_BUCKET_IMAGES_URL


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


class ImagesResSch(BaseModel):
    id: int = Field()
    name: str = Field(default=None)
    url: str = Field(default=None)

    @model_validator(mode="after")
    def make_url(self) -> Self:
        self.url = S3_BUCKET_IMAGES_URL + self.name
        return self
