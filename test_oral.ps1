# Start the Docker containers, rebuild all them, and run in the background
docker-compose up --build -d
# List the running Docker containers
docker ps
# Sleep for 5 seconds (optional delay)
Start-Sleep -Seconds 5
# Execute a command in the "user_container" Docker container, here is execute the test.py in a python environnement
docker exec -it user_container python test.py
# Stop all running Docker containers
docker stop $(docker ps -q)
# Clean up Docker resources (remove stopped containers, networks, and dangling images)
docker system prune