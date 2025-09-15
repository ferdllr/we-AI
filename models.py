import requests
import os
from dotenv import load_dotenv
from typing import Optional
from movie import Movie


class TMDBClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def _fetch_director(self, movie_id: int) -> Optional[str]:
        endpoint = f"{self.base_url}/movie/{movie_id}/credits"
        params = {"api_key": self.api_key}
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            credits_data = response.json()
            for member in credits_data.get("crew", []):
                if member.get("job") == "Director":
                    return member.get("name")
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
            rating = movie_data.get("vote_average", 0.0)

            if not movie_id:
                print("ID do filme não encontrado nos resultados.")
                return None

            director = self._fetch_director(movie_id)

            return Movie(
                name=movie_data.get("title"),
                movie_id=movie_id,
                rating=rating,
                author=director,
            )

        except requests.exceptions.RequestException as e:
            print(f"Erro na busca: {e}")
            return None


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("Chave da API não encontrada. Verifique seu arquivo .env")
    else:
        service = TMDBClient(base_url="https://api.themoviedb.org/3", api_key=api_key)

        movie = service.find_movie("Tá Dando Onda")

        if movie:
            print("Busca concluída com sucesso!")
            print(movie)
        else:
            print("Não foi possível obter os dados do filme.")
