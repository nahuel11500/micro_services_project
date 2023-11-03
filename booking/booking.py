from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_booking():
   res = make_response(jsonify(bookings),200)
   return res



@app.route("/bookings/<userid>", methods = ['POST'])
def post_bookingByID(userid):
   if request.args:
      req = request.args
      date = req['date']
      movieId = req['movieID']
      # Make a request to see if the date is available for the movie
      allMoviesJson = requests.get(f'http://172.16.134.102:3202/showmovies/{date}')
      allMoviesData = allMoviesJson.json()
      # Check if the date and movieId are available
      for movie in allMoviesData.get('movies', []):
         if str(movieId) == movie:
            # Add the reservation
            for user_booking in bookings:
               if user_booking['userid'] == userid:
                  for d in user_booking['dates']:
                     if d['date'] == date:
                        d['movies'].append(movieId)
                        return jsonify({"status": "Booking successful"}, 200)
                  # Add new date if not exists
                  user_booking['dates'].append({
                     "date": date,
                     "movies": [movieId]
                  })
                  return jsonify({"status": "Booking successful"}), 200
            return jsonify({"status": "Booking successful"}, 200)
   return (jsonify({"status": "Booking failed"}, 409))

@app.route("/bookings/<userid>", methods = ['GET'])
def get_bookingByID(userid):
   for booking in bookings:
      if str(userid) == str(booking['userid']):
         res = make_response(jsonify(booking),200)
         return res
   return make_response("bad input parameter",400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
