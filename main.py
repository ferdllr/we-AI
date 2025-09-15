import os
from dotenv import load_dotenv
from tmdbclient import TMDBClient


def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("API_KEY não encontrada no .env")
        return

    service = TMDBClient(base_url="https://api.themoviedb.org/3", api_key=api_key)
    filmes_favoritos = ["Homem-Aranha 2", "The Batman", "Tá Dando Onda"]

    dataset_recomendacoes = {}

    for filme_nome in filmes_favoritos:
        movie = service.find_movie(filme_nome)

        if not movie:
            print(f"sem dados para '{filme_nome}'.\n")
            continue

        tmdb_recs = service.get_recommendations(movie.id)

        director_recs = []
        if movie.author:
            all_director_movies = service.get_movies_by_director(movie.author.id)
            director_recs = [m for m in all_director_movies if m.id != movie.id]
        else:
            print(f"diretor não encontrado de '{movie.name}'.")

        tmdb_recs.sort(key=lambda m: m.rating, reverse=True)
        director_recs.sort(key=lambda m: m.rating, reverse=True)
        print("-------")
        print(f"filme: {movie.name}")
        print(f"top 3 TMDB: {[r.name for r in tmdb_recs[:3]]}")
        print(f"top 3 diretor: {[r.name for r in director_recs[:3]]}")

        combined_recs = tmdb_recs[:3] + director_recs[:3]

        unique_recs = {rec.id: rec for rec in combined_recs}
        final_list = list(unique_recs.values())

        final_list.sort(key=lambda m: m.rating, reverse=True)

        dataset_recomendacoes[movie.name] = final_list

        print(f"\nrecomendações finais para '{movie.name}':")
        for rec in final_list:
            print(f"  - {rec.name} (nota: {rec.rating:.1f})")
        print("-" * 50)


if __name__ == "__main__":
    main()
