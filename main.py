import os
import dotenv

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = "https://api.themoviedb.org/3"
