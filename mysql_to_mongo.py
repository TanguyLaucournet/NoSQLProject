from sqlalchemy import create_engine
import pymysql
import pandas as pd

 

sqlEngine       = create_engine('mysql+pymysql://root:password@127.0.0.1/nosql', pool_recycle=3600) #root = l'user de votre workbench, password votre mot de pase et nosql la db
dbConnection    = sqlEngine.connect()
frame           = pd.read_sql("select * from jsonfile", dbConnection); #jsonfile doit etre remplacé en fonction du nom de la table
pd.set_option('display.expand_frame_repr', False)
print(frame)

 

dbConnection.close()
