from typing import Optional


class Movie:
    def __init__(
        self, name: str, movie_id: int, rating: float, author: Optional[str]
    ) -> None:
        self.name = name
        self.id = movie_id
        self.rating = rating
        self.author = author

    def __repr__(self) -> str:
        return (
            f"filme: {self.name}\navaliação: {self.rating:.1f}\nautor: {self.author}\n"
        )
