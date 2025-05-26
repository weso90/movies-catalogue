from flask import Flask, render_template, request
import tmdb_client
import random


app = Flask(__name__)

@app.route('/')
def homepage():
    movies_list = {
        'now_playing': 'Now Playing',
        'popular': 'Popular',
        'top_rated': 'Top Rated',
        'upcoming': 'Upcoming'
    }
    selected_list = request.args.get('list_type', 'upcoming')

    if selected_list not in movies_list:
        selected_list = 'popular'

    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list, movies_list=movies_list, search_query="")

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route('/movie/<movie_id>')
def movie_details(movie_id):

    movies_list = {
        'now_playing': 'Now Playing',
        'popular': 'Popular',
        'top_rated': 'Top Rated',
        'upcoming': 'Upcoming'
    }
    details = tmdb_client.get_single_movie(movie_id)
    casts = tmdb_client.get_single_movie_cast(movie_id)
    movie_image = tmdb_client.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_image["backdrops"])
    return render_template("movie_details.html", movie=details, casts=casts, selected_backdrop=selected_backdrop, movies_list=movies_list)

@app.route('/search')
def search():
    movies_list = {
        'now_playing': 'Now Playing',
        'popular': 'Popular',
        'top_rated': 'Top Rated',
        'upcoming': 'Upcoming'
    }

    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query, movies_list=movies_list)


if __name__ == '__main__':
    app.run(debug=True)