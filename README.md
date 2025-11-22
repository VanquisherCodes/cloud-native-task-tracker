# Cloud Native Task Tracker API

A simple **cloud-native task tracker** REST API built with **Python (FastAPI)** and **MongoDB**, containerized using **Docker** and orchestrated with **Docker Compose**. The project includes a **GitHub Actions CI pipeline** that runs tests and builds the Docker image on every push.

## Features

- REST API for managing tasks (create, list, get by ID, delete)
- Built with **FastAPI** (automatic interactive docs at `/docs`)
- Uses **MongoDB** as database
- Configuration via environment variables:
  - `MONGO_URL` 
  - `MONGO_DB_NAME` 
- Fully containerized with **Docker**
- **Docker Compose** setup for API + MongoDB
- **GitHub Actions CI**:
  - Installs dependencies
  - Runs tests with `pytest`
  - Builds Docker image

## Tech Stack

- Python 3 + FastAPI
- MongoDB
- Docker & Docker Compose
- Pytest
- GitHub Actions (CI)

## Project Structure

```text
cloud-native-task-tracker/
├── app/
│   └── main.py              # FastAPI application (CRUD for tasks + MongoDB)
├── tests/
│   └── test_dummy.py        # Basic pytest test to validate CI
├── Dockerfile               # Docker image for the API
├── docker-compose.yml       # API + MongoDB services
├── requirements.txt         # Python dependencies
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI pipeline
└── .gitignore

##How to deploy my application (Docker needs to be installed beforehand!) 

Run the command :
docker run -p 8000:8000 kanishk1105/task-tracker-api:latest

