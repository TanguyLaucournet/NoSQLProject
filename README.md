1. [Initialisation](#initialisation)
    1. [Installation](#installation)
    2. [Lancement et création BDD](#lancement)
2. [Projection](#projection)
    1. [Vers Redis](#versRedis)
    2. [Vers MongoDB](#versMongo)
3. [Analyses](#analyses)
    1. [Avec Redis](#avecRedis)
    2. [Avec MongoDB](#avecMongo)

# Initialisation <a name="initialisation"></a>

## Installation <a name="installation"></a>

A la racine exécuter ```npm i``` pour installer tous les packages json et les modules nodes puis ```pip install -r requirements.txt``` pour les librairies python.

## Lancement et création BDD <a name="lancement"></a>

Avant tout il va falloir créer un nouveau Schemas dans MySQL : pour ce faire ouvrir et exécuter toutes les lignes du script [schema.sql](schema.sql)

**RENSEIGNER DANS UN DOC EXTERIEUR (.ENV PEUT ETRE) L'IDENTIFIANT ET MOT DE PASSE DE SA BASE MYSQL ??**

Une fois les deux commandes précédentes éxécutées, lancer ```npm run dev``` pour déployer le serveur local se chargant de créer et remplir une base de donnée MySQL avec des données issus d'une requête qu'elle reçoit.

Pour envoyer cette requête lancer le script python [fill_mysql.py](fill_mysql.py) qui, en se connectant au serveur, va lui envoyer une requête contenant notre jeu de données sous une certaine forme.

# Projection <a name="projection"></a>

## Vers Redis <a name="versRedis"></a>

Le code se chargant d'importer les données de la base MySQL à Redis est [mysql_to_redis.py](mysql_to_redis.py), il faut bien entendu lancer redis au préalable.

**Attention** : A une certaine ligne **```r.flushdb()```** vide toutes les données dans Redis, à commenter si ce n'est pas déjà le cas.

## Vers MongoDB <a name="versMongo"></a>

[mysql_to_mongo.py](mysql_to_mongo.py)
Pour la projection de MySQL vers Mongo nous avons tenté d'implémenter un scheduler permettant de mettre à jour la base de données MongoDB.
Pour cela nous importons les données des deux bases dans des dataframes pandas, ensuite nous concatènons ces deux dataframes pour utiliser la fonction de pandas drop_duplicates avec comme arguments 'Keep = False' pour supprimer tous les duplicats.
Cependant les tests que nous avons fait n'ont pas été concluants.
La projection de MySQL vers Mongo ce fait donc d'une seule traite sans scheduler.

Il faut donc attendre que la base de donnée MySQL soit rempli par fill_mysql avant d'éxécuter mysql_to_mongo.

# Analyses <a name="analyses"></a>

## Avec Redis <a name="avecRedis"></a>

[redis_analysis.py](redis_analysis.py)

## Avec MySQL <a name="avecMysql"></a>

[mongo_analysis.py](mongo_analysis.py)4dcffccc-4440-46ce-a9fa-fc9787de191c
