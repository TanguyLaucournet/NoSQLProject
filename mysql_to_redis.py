# import Redis and MySQL drivers
import redis
import MySQLdb
import settings

# Mysql server data
MYSQL_IP_ADDRESS_SERVER = 'localhost'
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_DATABASE_NAME = 'nosql'

# Redis server data
REDIS_SERVER = 'localhost'

# function to get data from mysql and to transfer it to redis
def sql_to_redis():
    r = redis.StrictRedis(REDIS_SERVER)
    print ()
    print ("Connected to Redis successfully!")

    database = MySQLdb.connect(MYSQL_IP_ADDRESS_SERVER, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE_NAME)
    print ("Connected to MySQL successfully!")
    print ()

    cursor = database.cursor()
    select = 'SELECT * FROM jsonfile'
    cursor.execute(select)
    data = cursor.fetchall()

    # Clean redis before run again
    # This is for test purpose
    # r.flushdb()

    # Put all data from MySQL to Redis
    for row in data:

        s = row[8][1:-1]
        l = s.split(', ')
        sbin = convertToBin(l)
        pathbin = sbin.split(' ')

        if( r.dbsize() == 0 ):
            r.hset(1, "id", row[0])
            r.hset(1, "event-type", row[1])
            r.hset(1, "occurredOn", row[2])
            r.hset(1, "addedOn", row[3])
            r.hset(1, "version", row[4])
            r.hset(1, "graph-id", row[5])
            r.hset(1, "nature", row[6])
            r.hset(1, "object-name", row[7])

            for i in range(-1, -9, -1):
                r.lpush("path", pathbin[i])

            r.set("datas",1)
        else:              
            datas = int(r.get("datas").decode()) + 1
            r.hset(datas, "id", row[0])
            r.hset(datas, "event-type", row[1])
            r.hset(datas, "occurredOn", row[2])
            r.hset(datas, "addedOn", row[3])
            r.hset(datas, "version", row[4])
            r.hset(datas, "graph-id", row[5])
            r.hset(datas, "nature", row[6])
            r.hset(datas, "object-name", row[7])

            for i in range(-1, -9, -1):
                r.lpush("path", pathbin[i])

            r.incr("datas")

    # Close connection to DB and Cursor
    cursor.close()
    database.close()


def convertToBin(path):
    res=''
    pathlist = ['TO_BE_PURGED', 'PURGED' ,'RECEIVED', 'VERIFIED', 'PROCESSED', 'REJECTED', 'REMEDIED', 'CONSUMED']
    for elem in pathlist:
        if elem in path:
            res+='1'
        else:
            res+='0'

        if elem != 'CONSUMED':
            res +=' '
    return res



if __name__ == '__main__':

    sql_to_redis()
    print("Projection to Redis SUCCESS")