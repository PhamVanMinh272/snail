from pydantic import BaseModel


class BrandResSch(BaseModel):
    id: int
    name: str
