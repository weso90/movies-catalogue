import requests

def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZWZkOTYzZjY1ODRiZDJkYzQyZDVjYzg0N2I0ZmQ2MCIsIm5iZiI6MTc0NzMzNjUwOS4wMDMsInN1YiI6IjY4MjYzZDNjMjE4NmQ1YWU3ZWFkYTQzMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.o8ManlL1HSBqt2w12oLaGvB46_jfjq_x-SbVXBGH3SE"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_movies(how_many):
    data = get_popular_movies()
    return data["results"][:how_many]