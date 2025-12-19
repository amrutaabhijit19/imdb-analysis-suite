import requests


def get_movie_details(movie_name, api_key):
    url = "http://www.omdbapi.com/"

    params = {
        "t": movie_name,
        "apikey": api_key
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if data.get("Response") == "False":
        return None

    return {
        "Title": data.get("Title"),
        "Year": data.get("Year"),
        "Genre": data.get("Genre"),
        "Director": data.get("Director"),
        "Actors": data.get("Actors"),
        "Language": data.get("Language"),
        "Runtime": data.get("Runtime"),
        "IMDb Rating": data.get("imdbRating"),
        "Box Office": data.get("BoxOffice"),
        "Plot": data.get("Plot")
    }

