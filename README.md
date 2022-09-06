[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

# chestTournament

## About The Project

chestTournament est un programme qui peut être lancé depuis une console. Il permet de créer et d'enregistrer des
tournois d'échecs, de les administrer, ainsi que leurs joueurs.

## Technologies

- Python 3.10

## Getting Started

### Installation (Windows)

1. Pour installer Python, vous pouvez vous rendre sur https://wiki.python.org/moin/BeginnersGuide/Download
2. Pour créer un environnement virtuel, saisissez dans votre terminal à l'endroit où vous souhaitez le créer:
    - `python -m venv env`
3. Pour activer votre environnement, saisissez:
    - `source env/Scripts/activate`
4. Il vous faudra ensuite installer les packages dans votre environnement avec la commande ci-dessous
    - `pip install -r requirements.txt`

### Usage

- Pour exécuter le web scraping, utilisez dans votre terminal la commande suivante:
    - `python main.py`

## Features

[comment]: <> (- A compléter et modifier les exclusions pour le rapport flake8)

- pour générer le rapport flake8:
  flake8 --format=html --htmldir=flake8_rapport --exclude env,.env,wip_controllers --max-line-length=119

## Author

Vpich
