from sqlalchemy import create_engine
import pandas as pd
import pymongo


sqlEngine = create_engine('mysql+pymysql://root:password@127.0.0.1/nosql', pool_recycle=3600) #root = l'user de votre workbench, password votre mot de pase et nosql la db
dbConnection = sqlEngine.connect()
frame = pd.read_sql("select * from jsonfile", dbConnection); #jsonfile doit etre remplacé en fonction du nom de la table


dbConnection.close()


# Insert in mongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dblist = myclient.list_database_names()
if "database" in dblist:
    db = myclient.mydatabase
    print("The database exists.")
else:
    db = myclient["database"]
    print("MongoDB database is created.")

collection = db['datalifecycle']
frame.reset_index(inplace=True)
data_dict = frame.to_dict("records")
# Insert collection
collection.insert_many(data_dict)
