**# Weather API**

This API allows you to access weather data for various stations and date. The data can be filtered by station name and Date. The API also provides statistical information on the weather data.

**# Installation**

Install the required packages

pip install -R requirements.txt


**# Data Ingestion:**

Run the below script for ingesting all the weather data and weathre statistics data to sql database

python datadump.py

**# Execution:**

Run the following command to access the weather api's through swagger 

python .\manage.py runserver

**# EndPoints:**

**Swagger :**

http://localhost:8000/swagger/

**Weather Data Api :**

GET /api/weather/

This endpoint returns a paginated list of weather records. You can filter the results by date and station id using query parameters:

GET /api/weather/?station_id=USC00110072&date=1987-01-01

**Weather Statistics Api :**

GET /api/weather/stats/

This endpoint returns statistical information about the weather data. You can filter the results by year and station id using query parameters.

GET /api/weather/stats/?station_id=USC00110072&year=1987


**# Testing :**

Run the tests

python test_data.py


**# Deployment:**

These are steps followed to deploy the service in aws 
1. Create the Docker file 
2. Build the image based on the docker file
3. Store the image into AWS ECR Repository
4. Run the container in AWS ECS Service based on image
5. Monitor the logs using AWS Cloud Watch
These are the aws services pointing to my container 
- aws s3 for storing/fetching the files
- aws RDS for ingest/retrieve the data from the database
Using AWS cloud front and Application Load balancer for routing the traffic to api running in different containers for scalable and durabiliity