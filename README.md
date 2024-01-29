## mdami199.ipynb
This file has Exploratory data analysis, my approach to solving the given problems with findings and justifications.
I have also explained that more could have been done with more time and resources.

## main.py
This file is FastAPI where I have defined the FastAPI instance, created endpoints, and implemented the business logic of your web application

## File myapp.txt 
represents the Dockerfile used to build a Docker image for a FastAPI application

## requirements.txt
dependencies required by the project

## Running the FastAPI Application with Docker
### Step 1: Build a Docker Image

bash
Copy code
docker build -t my-fastapi-app -f myapp.txt .
### Step 2: Run Docker Container

bash
Copy code
docker run -d -p 8000:80 my-fastapi-app
Access the Application

Visit http://localhost:8000 in your web browser to access the FastAPI application.
