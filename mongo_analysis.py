import pandas as pd
from datetime import datetime, timedelta
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient.database
mycol= db["collection_name"]

# Récupéré le cycle de vie parcouru
def get_life_cycle(obj_name):
    myquery = { "Object_name": obj_name }
    mydoc = list(mycol.find(myquery))
    life_cycle =''
    for x in mydoc:
      lifecycle += str(x['object_path']).replace("]", ",").replace("[", " ")
    return lifecycle

# Compter le nombre d'objets par status
def countObjByStatus(state):
    myquery = { "object_path": { "$regex": "^.*"+state".*$" } }
    mydoc = mycol.find(myquery)
    data = list(mydoc)
    print(len(data))
    return len(data)

# Compter le nombre d'objets par status
def countObjByStatusLastHour(state):
    start = mettre datetime.now() - timedelta(hours=1, minutes=0)
    myquery = {
        "$and" : [
               { "object_path": { "$regex": "^.*"+state+".*$" }},
               { "Date_ajout" : { "$gte" : start }},
                ]
              }
    mydoc = mycol.find(myquery)
    data = list(mydoc)
    print(len(data))
    return len(data)

