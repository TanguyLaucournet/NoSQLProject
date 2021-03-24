# -*- coding: utf-8 -*-
"""NoSQLProjection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PlgX6teoRLtntuBB2hLYOAleVyds3359

Check cron table
"""

!pip install pymysql

from sqlalchemy import create_engine

import pymysql

import pandas as pd

 

userVitals = {"UserId":["xxxxx", "yyyyy", "zzzzz", "aaaaa", "bbbbb", "ccccc", "ddddd"],

            "UserFavourite":["Greek Salad", "Philly Cheese Steak", "Turkey Burger", "Crispy Orange Chicken", "Atlantic Salmon", "Pot roast", "Banana split"],

            "MonthlyOrderFrequency":[5, 1, 2, 2, 7, 6, 1],

            "HighestOrderAmount":[30, 20, 16, 23, 20, 26, 9],

            "LastOrderAmount":[21,20,4,11,7,7,7],

            "LastOrderRating":[3,3,3,2,3,2,4],

            "AverageOrderRating":[3,4,2,1,3,4,3],

            "OrderMode":["Web", "App", "App", "App", "Web", "Web", "App"],

            "InMedicalCare":["No", "No", "No", "No", "Yes", "No", "No"]};

 

tableName   = "UserVitals"

dataFrame   = pd.DataFrame(data=userVitals)           

 

sqlEngine       = create_engine('mysql+pymysql://root:@127.0.0.1/test', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

 

try:

    frame           = dataFrame.to_sql(tableName, dbConnection, if_exists='fail');

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s created successfully."%tableName);   

finally:

    dbConnection.close()

from sqlalchemy import create_engine

import pymysql

import pandas as pd

 

sqlEngine       = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

frame           = pd.read_sql("select * from test.uservitals", dbConnection);

 

pd.set_option('display.expand_frame_repr', False)

print(frame)

 

dbConnection.close()

text= "2021-03-07T21:12:12.039020"
import pandas as pd

a = pd.to_datetime(text)

a



from pymongo import MongoClient

client = MongoClient('localhost', 27017)
#client = MongoClient('mongodb://localhost:27017/')

db = client.db_name
collection = db.collection_name

#insert a document into a collection
posts = db.posts
post_id = posts.insert_one(post).inserted_id

# many document
result = posts.insert_many(new_posts)