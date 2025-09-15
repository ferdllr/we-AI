from typing import Optional


class Author:
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id

    def __repr__(self) -> str:
        return f"{self.name} (ID: {self.id})"


class Movie:
    def __init__(
        self, name: str, movie_id: int, rating: float, author: Optional[Author]
    ) -> None:
        self.name = name
        self.id = movie_id
        self.rating = rating
        self.author = author

    def __repr__(self) -> str:
        return f"filme: {self.name}\navaliação: {self.rating:.1f}\nautor: {self.author.name if self.author else 'desconhecido'}\n"
