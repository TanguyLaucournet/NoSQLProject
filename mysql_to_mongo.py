from sqlalchemy import create_engine
import pymysql
import pandas as pd
import pymongo

 

sqlEngine       = create_engine('mysql+pymysql://root:password@127.0.0.1/nosql', pool_recycle=3600) #root = l'user de votre workbench, password votre mot de pase et nosql la db
dbConnection    = sqlEngine.connect()
frame           = pd.read_sql("select * from jsonfile", dbConnection); #jsonfile doit etre remplacé en fonction du nom de la table
pd.set_option('display.expand_frame_repr', False)
print(frame)

 dbConnection.close()


#Insert in mongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dblist = myclient.list_database_names()
if "database" in dblist:
    db = myclient.mydatabase
    print("The database exists.")
else:
    db = myclient["database"]
    print("The database is created.")

collection = db['collection_name']
frame2.reset_index(inplace=True)
data_dict = frame2.to_dict("records")
# Insert collection
collection.insert_many(data_dict)
