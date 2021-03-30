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

**Pour accéder a votre base de donnée MySQL renseignez dans le fichier [.env](.env) votre identifiant et mot de passe**.

Une fois les deux commandes précédentes éxécutées, lancer ```npm run dev``` pour déployer le serveur local se chargant de créer et remplir une base de donnée MySQL avec des données issus d'une requête qu'elle reçoit.

Pour envoyer cette requête lancer le script python [fill_mysql.py](fill_mysql.py) qui, en se connectant au serveur, va lui envoyer une requête contenant notre jeu de données sous une certaine forme. **30 lignes seront injectées toutes les 30 secondes**, il faudra alors 120s avant que la base de donnée soit entièrement remplie.

# Projection <a name="projection"></a>

## Vers Redis <a name="versRedis"></a>

Le code se chargant d'importer les données de la base MySQL à Redis est [mysql_to_redis.py](mysql_to_redis.py), il faut bien entendu lancer redis au préalable.

**Attention** : A une certaine ligne **```r.flushdb()```** vide toutes les données dans Redis, à commenter si ce n'est pas déjà le cas.

## Vers MongoDB <a name="versMongo"></a>

Pour la projection de MySQL vers Mongo nous avons tenté d'implémenter un scheduler permettant de mettre à jour la base de données MongoDB.  
Pour cela nous importons les données des deux bases dans des dataframes pandas, ensuite nous concatènons ces deux dataframes pour utiliser la fonction de pandas drop_duplicates avec comme arguments 'Keep = False' pour supprimer tous les duplicats.  
Cependant les tests que nous avons fait n'ont pas été concluants.  
La projection de MySQL vers Mongo ce fait donc d'une seule traite sans scheduler.  

**Il faut donc attendre 120 secondes, le temps que la base de donnée MySQL soit rempli par fill_mysql.py avant d'éxécuter [mysql_to_mongo.py](mysql_to_mongo.py)**.

# Analyses <a name="analyses"></a>

## Avec Redis <a name="avecRedis"></a>

Nous avons implémenté 3 des 4 requêtes demandées sur Redis dans le fichier [redis_analysis.py](redis_analysis.py).

La premiere consiste à utiliser **```retrieveID()```** de façon à récuperer l'index ou nous avons stocké les données d'un objet. Nous appelons ensuite **```retrieve_cycle()```** avec l'ID en paramètre et qui va nous renvoyer une liste contenant minimum 8 élément soit des 0 si l'objet n'a pas eu un statut spécifique ou des 1 si il l'a eu.
Afin de rendre l'affichage utilisateur plus compréhensible, nous utilisons **```polish_cycle_vie```** qui va retirer des doublons de status dans le cas ou nous avons plus de 9 élément ainsi que **```clean_data()```** pour retirer les 0 restant

Pour compter le nombre d'objet par statut, l'utilisateur sera ammené à rentrer un statut puis la fonction **```count_state()```** le comptera dans la liste des statuts

Nous n'avons pas réalisé le comptage d'objet selon l'heure car nous trouvions redis peu adapté à ce type de requete et nous avons préféré le faire exclusivement sur MongoDB

Enfin **```verified_life()```** appelera la première des implémentations sur chaque élément de la base de données et la comparera a la des statuts comme ayant respecté l'intégrité du graphe de cycle de vie
 
## Avec MySQL <a name="avecMysql"></a>

Pour l'analyse de la base de données Mongo nous avons implémenter les quatres requêtes demandées dans le fichier [mongo_analysis.py](mongo_analysis.py).


**```get_life_cycle()```** prend en attribut le nom d'un objet et retourne sont cycle de vie 'object_path'.

Les fonctions **```countObjByStatus()```** et **```countObjByStatusLastHour()```** prennent en argument un statut particulier et retourne le nombre d'objets possédant ce statut (uniquement ceux de la dernière heure pour **```countObjByStatusLastHour()```**).
  
La fonction **```countCompleteLife()```** utilise la fonction **```get_life_cycle()```** pour reconstituer le cycle de vie de chacun des objets présents dans la base puis incrémente un compteur dans le cas ou le cycle de vie de cet objet respecte l'intégrité du graphe du cycle de vie, enfin le compteur est retourné.  
