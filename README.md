# Navig-Cine

## TODO LIST

### Frontend

- [ ] Lancer requête initiale pour récupérer les genres principaux et liste de films associés & Stocker
- [ ] Proposer de façon aléatoire les films et demander like/nolike/skip (conserver en mémoire pour ne pas reproposer)

## Application Start

### Launch Local GraphDB Server

- Launch Docker : docker compose up
- Go to localhost:7200, create repository "Gdb-Navig-Cine" and import turtle files

### Launch Frontend Flask Server

- Create venv : python3 -m venv .venv
- Download requirement : pip install -r requirements.txt
- Launch server : python3 app/app.py