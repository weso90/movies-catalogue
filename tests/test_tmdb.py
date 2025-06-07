import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import Mock
import requests

import tmdb_client

def test_get_poster_url_uses_default_size():
    poster_api_path = "some-poster-path"
    expected_default_size = 'w342'
    poster_url = tmdb_client.get_poster_url(poster_api_path=poster_api_path)
    assert expected_default_size in poster_url

def test_get_movies_list_type_popular():
    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list is not None

def test_get_movies_list(monkeypatch):
    mock_movies_list = ['movie 1', 'movie 2']

    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_movies_list
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list == mock_movies_list

### TESTS FOR get_single_movie function

def test_get_single_movie_success(monkeypatch):
    movie_id = 100
    mock_movie_data = {
        'id': movie_id,
        'title': 'Rocky',
        'overview': 'movie about boxer',
        'poster_path': 'some_poster.jpg',
        'release_date': '1990-01-01'
    }

    requests_mock = Mock()
    response_mock = requests_mock.return_value
    response_mock.json.return_value = mock_movie_data
    response_mock.raise_for_status.return_value = None

    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    get_single_movie = tmdb_client.get_single_movie(movie_id)
    
    assert get_single_movie == mock_movie_data
    assert get_single_movie['title'] == 'Rocky'
    assert get_single_movie['id'] == 100

def test_get_single_movie_not_found(monkeypatch):
    movie_id = 111111111111111111111111
    requests_mock = Mock()
    response_mock = requests_mock.return_value
    response_mock.raise_for_status.side_effect = requests.exceptions.HTTPError("404")

    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    with pytest.raises(requests.exceptions.HTTPError) as info:
        tmdb_client.get_single_movie(movie_id)

    assert "404" in str(info.value)

def test_get_single_movie_empty(monkeypatch):
    movie_id = 1
    requests_mock = Mock()
    response_mock = requests_mock.return_value
    response_mock.json.return_value = {}
    response_mock.raise_for_status.return_value = None

    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    result = tmdb_client.get_single_movie(movie_id)

    assert result == {}


### TESTS FOR get_movie_images FUNCTION

def test_get_movie_images_success(monkeypatch):
    movie_id = 1
    mock_images_data = {
        'id': movie_id,
        'backdrops': [{'file_path': '/1.jpg', 'width': 1920, 'height': 1000}],
        'posters': [{'file_path': '/2.jpg', 'width': 100, 'height': 50}]
    }
    requests_mock = Mock()
    response_mock = requests_mock.return_value
    response_mock.json.return_value = mock_images_data
    response_mock.raise_for_status.return_value = None

    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    get_movie_images = tmdb_client.get_movie_images(movie_id)

    assert get_movie_images == mock_images_data
    assert 'backdrops' in get_movie_images
    assert 'posters' in get_movie_images

def test_get_movie_images_no_images(monkeypatch):
    movie_id = 1
    mock_images_data = {
        'id': movie_id,
        'backdrops': [],
        'posters': []
    }
    requests_mock = Mock()
    response_mock = requests_mock.return_value
    response_mock.json.return_value = mock_images_data

    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    get_movie_images = tmdb_client.get_movie_images(movie_id)

    assert get_movie_images == mock_images_data
    assert len(get_movie_images['backdrops']) == 0
    assert len(get_movie_images['posters']) == 0

def test_get_movie_images_http_error(monkeypatch):
    movie_id = 111111111111111111
    requests_mock = Mock()
    response_mock = requests_mock.return_value
    response_mock.raise_for_status.side_effect = requests.exceptions.HTTPError("404")

    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    with pytest.raises(requests.exceptions.HTTPError) as info:
        tmdb_client.get_movie_images(movie_id)
        
    assert "404" in str(info.value)

### TESTS FOR get_single_movie_cast FUNCTION

def test_get_single_movie_cast_success(monkeypatch):
    movie_id = 1
    mock_cast_data = {
        'id': movie_id,
        'cast': [
            {'adult': False, 'gender': 1, 'id': 1, 'name': 'Pol Lol', 'original_name': 'Original Name', 'character': 'bad'},
            {'adult': True, 'gender': 2, 'id': 2, 'name': 'Lol Pol', 'original_name': 'Name Original', 'character': 'good'}
        ],
        'crew': []
    }

    requests_mock = Mock()
    response_mock = requests_mock.return_value
    response_mock.json.return_value = mock_cast_data
    response_mock.raise_for_status.return_value = None

    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    get_single_movie_cast = tmdb_client.get_single_movie_cast(movie_id)
    
    assert len(get_single_movie_cast) == 2
    assert get_single_movie_cast[0]['name'] == 'Pol Lol'
    assert get_single_movie_cast[1]['adult'] == True
    assert get_single_movie_cast == mock_cast_data['cast']

def test_get_single_movie_cast_empty(monkeypatch):
    movie_id = 1
    mock_cast_data = {
        'id': movie_id,
        'cast': [],
        'crew': []
    }

    requests_mock = Mock()
    response_mock = requests_mock.return_value
    response_mock.json.return_value = mock_cast_data
    response_mock.raise_for_status.return_value = None

    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    get_single_movie_cast = tmdb_client.get_single_movie_cast(movie_id)
    
    assert len(get_single_movie_cast) == 0