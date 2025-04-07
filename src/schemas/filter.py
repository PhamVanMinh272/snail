from pydantic import BaseModel
from typing_extensions import Union


class FilterValueResponseSch(BaseModel):
    id: int
    name: Union[int|str]


class FilterResponseSch(BaseModel):
    id: int
    name: str
    values: list[FilterValueResponseSch]
