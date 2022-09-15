[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

# chestTournament

## About The Project

chestTournament est un programme qui peut être lancé depuis une console.

Il permet de créer et d'enregistrer des tournois d'échecs, de les administrer, et de gérer les scores des joueurs.
Chaque tournoi doit comporter 8 joueurs et les matchs sont générés selon le système de tournoi Suisse.

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

- Pour exécuter le programme, utilisez dans votre terminal la commande suivante:
    - `python main.py`

## Features

- Chargement automatique de la sauvegarde à chaque lancement
- Sauvegarde automatique à chaque modification de données
- Limitation de la création de tours tant que le tour actuellement disputé n'est pas clos
- Possibilité de générer un rapport flake8 en tapant la ligne de commande suivante:
    - `flake8 --format=html --htmldir=flake8_rapport --exclude env,.env --max-line-length=119`

## Author

Vpich
