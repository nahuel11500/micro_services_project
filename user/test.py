import time
import socket
import requests
import json
# URL where our Flask app is running

ip_address = socket.gethostbyname(socket.gethostname())
app_url = "http://127.0.0.1:3203"
# Sample data for testing
user_name = "Chris%20Rivers"
user_id = "chris_rivers"

# Define the endpoints to test
endpoints = [
    "/",
    "/showusers",
    f"/show/{user_name}",
    f"/show/reservation/user/{user_name}",
    "/users",
    f"/bookings/{user_id}",
    "/movies",
]

# Send GET requests to the specified endpoints
for endpoint in endpoints:
    url = f"{app_url}{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Request to {url} successful:")
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=4))  # Pretty print JSON
        except ValueError:  # JSON parsing failed
            print(response.content)
    else:
        print(f"Request to {url} failed with status code {response.status_code}:")
        print(response.content)
    time.sleep(4)

# Sending POST request to add a new user
new_user_data = {"id": 3, "name": "Alice"}
user_creation_url = f"{app_url}/users/3"
response = requests.post(user_creation_url, json=new_user_data)

if response.status_code == 200:
    print("New user created successfully:")
    print(response.json())
else:
    print(f"Failed to create a new user with status code {response.status_code}:")
    print(response.json())
