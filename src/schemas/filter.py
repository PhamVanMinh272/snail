from datetime import date
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated, Optional, Union
from src.common.enum import ColumnLabel

class FilterValueResponseSch(BaseModel):
    id: int
    name: Union[int|str]


class FilterResponseSch(BaseModel):
    id: int
    name: str
    values: list[FilterValueResponseSch]
