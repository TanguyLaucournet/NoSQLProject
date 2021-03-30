import pandas as pd
from datetime import datetime, timedelta
import pymongo



# Récupéré le cycle de vie parcouru
def get_life_cycle(obj_name):
    myquery = { "Object_name": obj_name }
    mydoc = list(mycol.find(myquery))
    life_cycle =[]
    for elem in mydoc:
            path = elem['object_path'].replace("]", "").replace("[", "").replace(" ","").split(',')
            for x in path:
                life_cycle.append(x)
    life_cycle = sorted(set(life_cycle))
    return life_cycle

# Compter le nombre d'objets par status
def countObjByStatus(state):
    myquery = { "object_path": { "$regex": "^.*"+state+".*$" } }
    mydoc = mycol.find(myquery)
    data = list(mydoc)
    print('')
    print("Nombre d'objet ayant le statut '"+state+"': "+str(len(data)))
    print('')
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
    print('')
    print("Nombre d'objet ayant le statut '"+state+"': "+str(len(data)))
    print('')
    return data

def countCompleteLife():
    dist = mycol.distinct('Object_name')
    counter = 0
    pathlist = ['TO_BE_PURGED', 'PURGED' ,'RECEIVED', 'VERIFIED', 'PROCESSED', 'CONSUMED']
    pathlist2 = ['TO_BE_PURGED', 'PURGED' ,'RECEIVED', 'VERIFIED', 'PROCESSED', 'REJECTED']
    pathlist3 = ['CREATED', 'PURGED' , 'PROCESSED', 'REJECTED']
    pathlist4 = ['CREATED', 'PURGED' , 'PROCESSED', 'CONSUMED']
    for itm in dist:
        obj_path = get_life_cycle(itm)
        check = all(element in obj_path for element in pathlist) or all(element in obj_path for element in pathlist2) or all(element in obj_path for element in pathlist3) or all(element in obj_path for element in pathlist4)
        if check:
            counter+=1
    print('')
    print("Le nombre d'objets respectant l'intégrité du cycle de vie est de "+str(counter))
    print('')
    return counter


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient.database
mycol= db["datalifecycle"]

print('Mongo analysis')
print("Sélectionner l'action à éffectuer: ")
print( '1 - Récupérer le cycle de vie parcouru')
print( '2 - Compter le nombre d’objets par status')
print( '3 - Compter le nombre d’objets par status sur la dernière heure')
print( '4 - Compter le nombre d’objets respectant l’intégrité du graphe du cycle de vie')
print( ' Any other key to quit')
print('')
ans = input()

while ans in ['1','2','3','4']:
    if ans == '1' :
        obj_name = input("Nom de l'objet: ")
        print('')
        print(get_life_cycle(obj_name))
        print('')
    elif ans == '2':
        status = input("Nom du statut: ")
        countObjByStatus(status)
    elif ans == '3':
        status = input("Nom du statut: ")
        countObjByStatusLastHour(status)
    elif ans == '4':
        countCompleteLife()
    
    print("Sélectionner l'action à éffectuer: ")
    print( '1 - Récupérer le cycle de vie parcouru')
    print( '2 - Compter le nombre d’objets par status')
    print( '3 - Compter le nombre d’objets par status sur la dernière heure')
    print( '4 - Compter le nombre d’objets respectant l’intégrité du graphe du cycle de vie')
    print( ' Any other key to quit')
    print('')
    ans = input()
    print('')