import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from typing import List
from tmdbclient import TMDBClient
from models import Movie

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY não encontrada no .env")

app = FastAPI()
service = TMDBClient(base_url="https://api.themoviedb.org/3", api_key=API_KEY)


@app.get("/recommendations", response_model=List[Movie])
async def get_recommendations_for_movie(movie_name: str):
    movie = service.find_movie(movie_name)

    if not movie:
        raise HTTPException(
            status_code=404, detail=f"Filme '{movie_name}' não encontrado."
        )

    tmdb_recs = service.get_recommendations(movie.id)

    director_recs = []
    if movie.author:
        all_director_movies = service.get_movies_by_director(movie.author.id)
        director_recs = [m for m in all_director_movies if m.id != movie.id]
    else:
        print(f"Diretor não encontrado para '{movie.name}'.")

    tmdb_recs.sort(key=lambda m: m.rating, reverse=True)
    director_recs.sort(key=lambda m: m.rating, reverse=True)

    combined_recs = tmdb_recs[:3] + director_recs[:3]

    unique_recs = {rec.id: rec for rec in combined_recs}
    final_list = list(unique_recs.values())

    final_list.sort(key=lambda m: m.rating, reverse=True)

    return final_list
