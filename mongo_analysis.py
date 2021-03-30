import pandas as pd
from datetime import datetime, timedelta
import pymongo



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
    myquery = { "object_path": { "$regex": "^.*"+state+".*$" } }
    mydoc = mycol.find(myquery)
    data = list(mydoc)
    print(len(data))
    return len(data)

# Compter le nombre d'objets par status
def countObjByStatusLastHour(state):
    start = datetime.now() - timedelta(hours=1, minutes=0)
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

def countCompleteLife():
    dist = mycol.distinct('Id')
    counter = 0
    pathlist = ['TO_BE_PURGED', 'PURGED' ,'RECEIVED', 'VERIFIED', 'PROCESSED', 'CONSUMED']
    for itm in dist:
        obj_path = []
        myquery = { "Id": itm }
        mydoc = list(mycol.find(myquery))
        for elem in mydoc:
            path = elem['object_path'].replace("]", "").replace("[", "").replace(" ","").split(',')
            for x in path:
                obj_path.append(x)
        check = all(element in obj_path for element in pathlist)
        if check:
            counter+=1
    print(counter)
    return counter


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient.database
mycol= db["collection_name"]

print('Mongo analysis')
print("Sélectionner l'action à éffectuer: ")
print( '1 - Récupérer le cycle de vie parcouru')
print( '2 - Compter le nombre d’objets par status')
print( '3 - Compter le nombre d’objets par status sur la dernière heure')
print( '4 -  Compter le nombre d’objets respectant l’intégrité du graphe du cycle de vie')
ans = input()

while ans in ['1','2','3','4']:
    if ans == '1' :
        obj_name = input("Nom de l'objet: ")
        get_life_cycle(obj_name)
    elif ans == '2':
        status = input("Nom du statut")
        countObjByStatus(status)
    elif ans == '3':
        status = input("Nom du statut")
        countObjByStatusLastHour(status)
    elif ans == '4':
        countCompleteLife()
    
    print("Sélectionner l'action à éffectuer: ")
    print( '1 - Récupérer le cycle de vie parcouru')
    print( '2 - Compter le nombre d’objets par status')
    print( '3 - Compter le nombre d’objets par status sur la dernière heure')
    print( '4 - Compter le nombre d’objets respectant l’intégrité du graphe du cycle de vie')
    ans = input()
