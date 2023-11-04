from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# This route handles a GET request to '/showusers'.
@app.route("/showusers", methods=['GET'])
def get_users():
    """"This function returns a response containing the 'users' data in JSON format with a 200 OK status."""
    return make_response(jsonify(users), 200)

# This route handles a GET request to '/show/<user_name>'.
@app.route('/show/<user_name>', methods=["GET"])
def get_user(user_name):
    """"This function iterates through the 'users' list to find a user with the matching 'user_name'"""
    for _user in users:
        if str(_user['name']) == str(user_name):
            # If a user with a matching 'user_name' is found, it creates a response
            # containing the user's data in JSON format with a 200 OK status and returns it.
            res = make_response(jsonify(_user), 200)
            return res

    # If no matching user is found, it returns a response with an error message
    # in JSON format and a 400 Bad Request status.
    return make_response(jsonify({"error": "User not found"}), 400)


# This route handles a GET request to '/show/reservation/<user_name>'.
@app.route('/show/reservation/user/<user_name>', methods=['GET'])
def get_user_reservation_by_name(user_name):
    """This function get the user's reservation from its name. """
    # Search for the user with the provided 'user_name'.
    for _user in users:
        if str(_user['name']) == str(user_name):
            user_id = _user["id"]
            # Make a request to see if the date is available for the movie
            response = requests.get(f'http://192.168.1.22:3201/bookings/{user_id}')
            if response.status_code == 200:
                # If reservations are found, merge user and reservation data.
                merged_dict = {**_user, **response.json()}
                return make_response(jsonify(merged_dict), 200)
            else:
                # If no reservations are found, return an error response.
                return make_response(jsonify({"error": "Booking information not found"}), 400)

    # If the user with the provided 'user_name' is not found, return an error response.
    return make_response(jsonify({"error": "User not found"}), 400)


# This route handles a GET request to '/users'.
@app.route("/users", methods=['GET'])
def get_json():
    """This function return all the user's data."""
    return make_response(jsonify({"users": users}), 200)

# This route handles a GET request to '/users/<userid>'.
@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    # Search for a user with the provided 'userid'.
    for user in users:
        if str(user["id"]) == str(userid):
            # If found, return user data with a 200 OK status.
            return make_response(jsonify(user), 200)
    # If 'userid' is not found, return an error response.
    return make_response(jsonify({"error": "User ID not found"}), 400)

# This route handles a GET request to '/bookings/<userid>'.
@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    # Make a request to the micro-service booking to get booking data for the user.
    response = requests.get(f"http://192.168.1.22:3201/bookings/{userid}")
    # Return the response from the external service.
    return make_response(response.json(), response.status_code)

# This route handles a GET request to '/movies'.
@app.route("/movies", methods=['GET'])
def get_movies():
    # Make a request to the micro-service movie to get movie data.
    response = requests.get(f"http://192.168.1.22:3200/json")
    return make_response(jsonify(response.json()), response.status_code)


# This route handles a POST request to '/users/<userid>'.
@app.route("/users/<userid>", methods=['POST'])
def add_user(userid):
    # Extract the JSON data from the request.
    req = request.get_json()
    # Check if a user with the provided 'userid' already exists.
    for user in users:
        # If user already exists, return a conflict error response (HTTP status 409).
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User already exists"}), 409)
    # If the user is new, add them to the 'users' list.
    users.append(req)
    # Return the added user data with a 200 OK status.
    res = make_response(jsonify(req), 200)
    return res


# This route handles a POST request to '/bookings/<userid>'.
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    # Extract the JSON data from the request.
    req = request.get_json()
    # Make a request to the micro-service booking to add a booking for the user.
    response = requests.post(f"http://192.168.1.22:3201/bookings/{userid}", json=req)
    # Return the response from the the micro-service booking
    return make_response(response.json(), response.status_code)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    # Start the Flask app on the specified host and port in debug mode.
    app.run(host=HOST, port=PORT, debug=True)
