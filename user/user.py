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


@app.route("/showusers", methods=['GET'])
def get_users():
    return make_response(jsonify(users), 200)


@app.route('/show/<user_name>', methods=["GET"])
def get_user(user_name):
    for _user in users:
        if str(_user['name']) == str(user_name):
            res = make_response(jsonify(_user), 200)
            return res
    return make_response(jsonify({"error": "User not found"}), 400)


@app.route('/show/reservation/user/<user_name>', methods=['GET'])
def get_user_reservation_by_name(user_name):
    ## Get the id with the name
    for _user in users:
        if str(_user['name']) == str(user_name):
            user_id = _user["id"]
            # Make a request to see if the date is available for the movie
            response = requests.get(f'http://192.168.1.22:3201/bookings/{user_id}')
            if response.status_code == 200:
                merged_dict = {**_user, **response.json()}
                return make_response(jsonify(merged_dict), 200)
            else:
                return make_response(jsonify({"error": "Booking information not found"}), 400)

    return make_response(jsonify({"error": "User not found"}), 400)


@app.route("/users", methods=['GET'])
def get_json():
    return make_response(jsonify({"users": users}), 200)


@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "User ID not found"}), 400)


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    response = requests.get(f"http://192.168.1.22:3201/bookings/{userid}")
    return make_response(response.json(), response.status_code)


@app.route("/movies", methods=['GET'])
def get_movies():
    response = requests.get(f"http://192.168.1.22:3200/json")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/users/<userid>", methods=['POST'])
def add_user(userid):
    req = request.get_json()
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User already exists"}), 409)
    users.append(req)
    res = make_response(jsonify(req), 200)
    return res


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    req = request.get_json()
    response = requests.post(f"http://192.168.1.22:3201/bookings/{userid}", json=req)
    return make_response(response.json(), response.status_code)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))

    app.run(host=HOST, port=PORT, debug=True)
