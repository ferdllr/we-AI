# tmdbclient.py
import requests
from typing import Optional, List
from models import Movie, Author


class TMDBClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def _fetch_director(self, movie_id: int) -> Optional[Author]:
        endpoint = f"{self.base_url}/movie/{movie_id}/credits"
        params = {"api_key": self.api_key}
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            credits_data = response.json()
            for member in credits_data.get("crew", []):
                if member.get("job") == "Director":
                    director_id = member.get("id")
                    director_name = member.get("name")
                    if director_id and director_name:
                        return Author(id=director_id, name=director_name)
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar diretor: {e}")
            return None

    def find_movie(self, name: str) -> Optional[Movie]:
        print(f"Buscando '{name}'...")
        endpoint = f"{self.base_url}/search/movie"
        params = {"api_key": self.api_key, "query": name, "language": "pt-BR"}
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get("results"):
                print("Filme não encontrado.")
                return None

            movie_data = data["results"][0]
            movie_id = movie_data.get("id")

            if not movie_id:
                print("ID do filme não encontrado nos resultados.")
                return None

            director = self._fetch_director(movie_id)

            return Movie(
                name=movie_data.get("title"),
                movie_id=movie_id,
                rating=movie_data.get("vote_average", 0.0),
                author=director,
            )
        except requests.exceptions.RequestException as e:
            print(f"Erro na busca: {e}")
            return None

    def get_recommendations(self, movie_id: int) -> List[Movie]:
        """Busca as recomendações do TMDB para um filme."""
        endpoint = f"{self.base_url}/movie/{movie_id}/recommendations"
        params = {"api_key": self.api_key, "language": "pt-BR"}
        recommendations = []
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            for movie_data in data.get("results", []):
                recommendations.append(
                    Movie(
                        name=movie_data.get("title"),
                        movie_id=movie_data.get("id"),
                        rating=movie_data.get("vote_average", 0.0),
                        author=None,
                    )
                )
            return recommendations
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar recomendações: {e}")
            return []

    def get_movies_by_director(self, director_id: int) -> List[Movie]:
        endpoint = f"{self.base_url}/person/{director_id}/movie_credits"
        params = {"api_key": self.api_key, "language": "pt-BR"}
        filmography = []
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            for movie_data in data.get("crew", []):
                if movie_data.get("job") == "Director":
                    filmography.append(
                        Movie(
                            name=movie_data.get("title"),
                            movie_id=movie_data.get("id"),
                            rating=movie_data.get("vote_average", 0.0),
                            author=None,
                        )
                    )
            return filmography
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar filmes do diretor: {e}")
            return []
