#!/usr/bin/python
## SQL to Redis

# import Redis and MySQL drivers
import redis
import MySQLdb
from collections import Counter

# Mysql server data
MYSQL_IP_ADDRESS_SERVER = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DATABASE_NAME = 'nosql'

# Redis server data
REDIS_SERVER = 'localhost'

# function to get data from mysql and to transfer it to redis
def sql_to_redis():
    r = redis.StrictRedis(REDIS_SERVER)
    print ("")
    print ("Connected to Redis successfully!")

    database = MySQLdb.connect(MYSQL_IP_ADDRESS_SERVER, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE_NAME)
    print ("Connected to MySQL successfully!")
    print ("")

    cursor = database.cursor()
    select = 'SELECT * FROM jsonfile'
    cursor.execute(select)
    data = cursor.fetchall()

    # Clean redis before run again
    # This is for test purpose
    r.delete("all_records")

    # Put all data from MySQL to Redis
    for row in data:

        # print(row)
        # print()

        if( r.dbsize() == 0 ):
            r.hset( 1, "id", row[0])
            r.hset( 1, "event-type", row[1])
            r.hset( 1, "occurredOn", row[2])
            r.hset( 1, "version", row[3])
            r.hset( 1, "graph-id", row[4])
            r.hset( 1, "nature", row[5])
            r.hset( 1, "object-name", row[6])
            r.hset( 1, "path", row[7])

            r.set("datas",1)
        else:              
            datas = int(r.get("datas").decode()) + 1
            r.hset( datas, "id", row[0])
            r.hset( datas, "event-type", row[1])
            r.hset( datas, "occurredOn", row[2])
            r.hset( datas, "version", row[3])
            r.hset( datas, "graph-id", row[4])
            r.hset( datas, "nature", row[5])
            r.hset( datas, "object-name", row[6])
            r.hset( datas, "path", row[7])  

            r.incr("datas")

    # Close connection to DB and Cursor
    cursor.close()
    database.close()



def get_data_from_redis():
    r2 = redis.StrictRedis(REDIS_SERVER)
    # LIRE REDIS POUR VERIFIER QUE TOUT EST CORRECTEMENT IMPLEMENTE



def convertToBin(path):
    res=''
    pathlist = ['TO_BE_PURGED', 'PURGED' ,'RECEIVED', 'VERIFIED', 'PROCESSED', 'REJECTED', 'REMEDIED', 'CONSUMED']
    for elem in pathlist:
        if elem in path:
            res+='1'
        else:
            res+='0'
        res +=' '
    return res



sql_to_redis()
get_data_from_redis()