import requests
from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
import os
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'
absolute_path = os.path.dirname(__file__)
relative_path = "databases/movies.json"
full_path = os.path.join(absolute_path, relative_path)
with open(full_path, "r") as jsf:

    movies = json.load(jsf)["movies"]


#TMDB API
API_KEY = 'ToChange'


# root message
#this is the welcome message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

#this route shows an html template
@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

#this route return the movies's Json
@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

# This route handles a GET request to '/movies/<movieid>'.
# It return avaible information about given movie (it takes the movie id in the url)
#if the local json file contains the movie it will return the movies's information from the Json
#otherways it will search for it in the tmdb  using the api_key

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    MovieURL = f"https://api.themoviedb.org/3/movie/{movieid}?api_key={API_KEY}"
    response = requests.get(MovieURL)
    if response.status_code != 200:
        return make_response(jsonify({"error": "Movie not found"}), 404)
    movie = response.json()
    return make_response(jsonify(movie),200)




# This route handles a GET request to '/moviesbytitle'.
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        title = str(req["title"])
        for movie in movies:
            if str(movie["title"]) == title:
                json = movie


    if not json:
            URL = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
            response = requests.get(URL)
            search_results = response.json().get("results", [])
            if search_results:
                res = make_response(jsonify(search_results[0]), 200)
            else:
                res = make_response(jsonify({"error": "Movie not found"}), 404)
    else:
        res = make_response(jsonify(json), 200)
    return res


# This route handles a POST request to '/movies/<movieid>'.
#this route is used to add a movie to the movies db
#it the given id already exist it will return an error 409
@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res


# This route handles a POST request to '/movies/<movieid>/<rate>'.
#this route updates a movie rate
#it takes the movie id and the new rate
#it returns the movie with the new given rate

@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie),200)
            return res
    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res


# This route handles a POST request to '/movies/<movieid>'.
# Itdeletes a movie from the local dataBase
#if the movie is is not found it returns an error 400
@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)
    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res


if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
