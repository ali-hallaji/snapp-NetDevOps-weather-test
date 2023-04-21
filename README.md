# Project purpose

This project is a FastAPI application that retrieves weather data from the OpenWeatherMap API and stores it in a PostgreSQL database. The application provides an API endpoint that allows users to get weather data for a specific city.

# How to start the project

To start the project, follow these steps:

1. Install Docker and Docker Compose on your Linux server.
2. Clone this repository to your server.
3. Change to the project directory: cd snapp-NetDevOps-weather-test
4. Copy the env-example file to .env: cp env-example .env
5. Edit the .env file and update the variables with your own values, such as the OpenWeatherMap API key.
6. Build the Docker images: docker-compose build
7. Start the containers in the background: docker-compose up -d
8. The API should now be accessible at http://localhost/docs    # It's swagger and you'll be able to try it.

# Requirements

To run this project, you need the following:

- A Linux server with Docker and Docker Compose installed.
- An OpenWeatherMap API key.

# Changing the OpenWeatherMap API key

To change the OpenWeatherMap API key, edit the .env file and update the WEATHER_API_KEY variable with your own API key.

# Running tests

To run the tests, follow these steps:

1. Make sure the containers are running: docker-compose up -d
2. Start a Bash shell in the app container: docker-compose exec app bash
3. Run the tests: pytest -vv -rP
4. Exit the container: exit

The tests should now run and output the results in the terminal.

# Example Usage:

For getting the token you need to login to the service:
```
curl -X POST "http://localhost/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=root" \
     -d "password=12345678" 
```

then extract the access_token from the response.
And to get data for specific city do this in the following:
```
curl -X GET "http://localhost:8000/v1/weather?city=Tehran" \
     -H "Authorization: Bearer <access_token>"
```