# Initialisation

## Installation

A la racine exécuter ```npm i``` pour installer tous les packages json et les modules nodes puis ```pip install -r requirements.txt``` pour les librairies python.

## Lancement et création BDD

Avant tout il va falloir créer un nouveau Schemas dans MySQL : pour ce faire ouvrir et exécuter toutes les lignes du script [schema.sql](schema.sql)

**RENSEIGNER DANS UN DOC EXTERIEUR (.ENV PEUT ETRE) L'IDENTIFIANT ET MOT DE PASSE DE SA BASE MYSQL ??**

Une fois les deux commandes précédentes éxécutées, lancer ```npm run dev``` pour déployer le serveur local se chargant de créer et remplir une base de donnée MySQL avec des données issus d'une requête qu'elle reçoit.

Pour envoyer cette requête lancer le script python [fill_mysql.py](fill_mysql.py) qui, en se connectant au serveur, va lui envoyer une requête contenant notre jeu de données sous une certaine forme.

# Projection

## Vers Redis

Le code se chargant d'importer les données de la base MySQL à Redis est [mysql_to_redis.py](mysql_to_redis.py), il faut bien entendu lancer redis au préalable.

**Attention** : A une certaine ligne **```r.flushdb()```** vide toutes les données dans Redis, à commenter si ce n'est pas déjà le cas.

## Vers MongoDB

[mysql_to_mongo.py](mysql_to_mongo.py)

# Analyses

## Avec Redis

[redis_analysis.py](redis_analysis.py)

## Avec MySQL

[mongo_analysis.py](mongo_analysis.py)