# Project Bloc 2

## Présentation
Vous êtes embauché en tant qu'ingénieur data dans une entreprise qui souhaite moderniser
son infrastructure de gestion de données.
Votre mission consiste à concevoir et mettre en œuvre une infrastructure data sur le Cloud,
à collecter et intégrer des données provenant de diverses sources, et à fournir des analyses
et visualisations interactives pour soutenir la prise de décision.
Le projet comprend plusieurs phases :
1. Mise en place de l'infrastructure Cloud
2. Création d'un pipeline de collecte et de traitement des données
3. Exploration et visualisation des données
4. Documentation complète du processus.

## Structure du github
- **MAIN**
  - Dernière version du code stable
- **DATA-OBSERVATION**
  - Actuellement la dernière version à jour. C'est là qu'est stocké mon fichier **data.ipynb** avec mes observations.
- **RDS-MANAGER**
  - Le RDS Manager pour stocker mes données structurées sur AWS. La fonctionnalité ne fonctionne pas encore à cause d'un problème de lien.

## Installation
```bash
python -m venv venv
cd venv
```

Installation des dépendances :
```bash
pip install -r requirements.txt
```

## Commands
Fetch and save page data
```bash
py app.py --FS_page_data
```

Fetch and save api data
```bash
py app.py --FS_api_data
```
