from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

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
   return make_response(jsonify(users),200)

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
            response = requests.get(f'http://172.16.134.102:3201/bookings/{user_id}')
            if response.status_code == 200:
                merged_dict = {**_user, **response.json()}
                return make_response(jsonify(merged_dict), 200)
            else:
                return make_response(jsonify({"error": "Booking information not found"}), 400)

    return make_response(jsonify({"error": "User not found"}), 400)




if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)

