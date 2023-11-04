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

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

# This route handles a GET request to '/movies/<movieid>'.
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    # Search for a movie with the provided 'movieid'.
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            # If found, return the movie data with a 200 OK status.
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)



# This route handles a GET request to '/moviesbytitle'.
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        # Get the title of the movie.
        req = request.args
        # Search for a movie with the provided title.
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(json),200)
    return res

# This route handles a POST request to '/movies/<movieid>'.
@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()
    # Check if a movie with the provided 'movieid' already exists.
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)
    # If the movie is new, add it to the 'movies' list.
    movies.append(req)
    # Return a success response with a 200 OK status.
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

# This route handles a POST request to '/movies/<movieid>/<rate>'.
@app.route("/movies/<movieid>/<rate>", methods=['POST'])
def update_movie_rating(movieid, rate):
    # Search for a movie with the provided 'movieid'.
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            # Update the movie's rating and return the updated movie data with a 200 OK status.
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

# This route handles a POST request to '/movies/<movieid>'.
@app.route("/movies/<movieid>", methods=['POST'])
def del_movie(movieid):
    # Search for a movie with the provided 'movieid'.
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            # Remove the movie from the 'movies' list and return the deleted movie data with a 200 OK status.
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
