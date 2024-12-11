# Shared-Grocery-Cart-Prototype
Year 2 project, SSH Shared Groceries Cart prototype

## Overview
This application manages shared grocery carts for multiple users, allowing students to add, view, and pay for items collaboratively.

## Features
- Add and manage students.
- Add products to a shared cart.
- Calculate payments individually or collectively.
- Logging for observability and debugging.

## Setup and Run
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install PySide6

## Prerequisites
- Docker installed
- Python 3.10+ installed (if running locally without Docker)

## Run unit test locally: 
python -m unittest discover -s tests -p "*.py"

## Run the application directly: 
python skeleton.py

## How to Run Locally:

1. **Build the Docker Image:**
   docker build . --file Dockerfile --tag shared-groceries-app:latest

## Run the Docker Container:
docker run -d --name shared-groceries-app-container -p 8080:8080 shared-groceries-app:latest

## Check Application Logs: 
docker logs shared-groceries-app-container
## Run the test inside the container : 
docker run --rm shared-groceries-app:latest python3 -m unittest /app/skeleton_unit_testing.py


## Stop and Clean Up:
docker stop shared-groceries-app-container
docker rm shared-groceries-app-container

