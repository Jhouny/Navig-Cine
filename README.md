# Navig-Cine
This system is an application of knowledge graphs for movie recommendation and exploration. It leverages a local GraphDB server to store and query movie data, and a Flask-based frontend to provide an interactive user interface.

## Running the Application

### Launch Local GraphDB Server

- Launch Docker : `docker compose up --build -d`

### Launch Frontend Flask Server

- Create venv : `python3 -m venv .venv`
- Download requirement : `pip install -r requirements.txt`
- Launch server : `python3 app/app.py`