from sqlalchemy import create_engine
import pandas as pd
import pymongo
import settings

MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
url = 'mysql+pymysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@127.0.0.1/nosql'

sqlEngine = create_engine(url, pool_recycle=3600) #root = l'user de votre workbench, password votre mot de pase et nosql la db
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

# while True:
#     dblist = myclient.list_database_names()
#     if "database" in dblist:
#         db = myclient.database
#         print("The database exists.")
#         df_mongo = pd.DataFrame(list(db['datalifecycle'].find()))
#         clean_df =  df_mongo [['Id','Event_type', 'Date_creation', 'Date_ajout', 'Version_file', 'Graph_id', 'nature','Object_name','object_path' ]]
#         clean_frame = frame[['Id','Event_type', 'Date_creation', 'Date_ajout', 'Version_file', 'Graph_id', 'nature','Object_name','object_path' ]]
#         df = pd.concat([clean_frame, clean_df])
#         df.drop_duplicates(keep=False)
#     else:
#         df = frame
#         db = myclient["database"]
#         print("MongoDB database is created.")

#     collection = db['datalifecycle']
#     df.reset_index(inplace=True)
#     data_dict = df.to_dict("records")
#     # Insert collection
#     collection.insert_many(data_dict)
#     time.sleep(30)