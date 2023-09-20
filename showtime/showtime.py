from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/showtimes", methods = ['GET'])
def get_showtime():
   res = make_response(jsonify(schedule), 200)
   return res

@app.route("/showmovies/<date>", methods = ['GET'])
def get_movie_date(date):
   for dates in schedule:
      if str(dates['date']) == str(date):
         res = make_response(jsonify(dates), 200)
         return res
   return make_response(jsonify({"error": "Date not found"}), 400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
