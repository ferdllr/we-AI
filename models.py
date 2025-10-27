from typing import Optional
from pydantic import BaseModel


class Author(BaseModel):
    id: int
    name: str


class Movie(BaseModel):
    id: int
    name: str
    rating: float
    author: Optional[Author]
