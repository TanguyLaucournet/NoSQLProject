import redis

REDIS_SERVER = 'localhost'

def get_data_from_redis():
    r2 = redis.StrictRedis(REDIS_SERVER)
    # LIRE REDIS POUR VERIFIER QUE TOUT EST CORRECTEMENT IMPLEMENTE
    for i in range(1,int(r2.get("datas").decode()) + 1):
            print(r2.hget(i,"id").decode())

def retrieveID(r, target):
    lindex = []
    for i in range(1,int(r.get("datas").decode())+1 ):
        if r.hget(i,"object-name").decode() == target:
            lindex.append(i)
    return lindex


def retrieve_cycle(r, lindex):
    cycle_vie = []
    for elem in lindex:
        cycle_vie.append(r.lindex("path",elem).decode())
        cycle_vie.append(r.lindex("path",elem+1).decode())
        cycle_vie.append(r.lindex("path",elem+2).decode())
        cycle_vie.append(r.lindex("path",elem+3).decode())
        cycle_vie.append(r.lindex("path",elem+4).decode())
        cycle_vie.append(r.lindex("path",elem+5).decode())
        cycle_vie.append(r.lindex("path",elem+6).decode())
        cycle_vie.append(r.lindex("path",elem+7).decode())
        #etc jusqu'a ce qu'on ait tout le elem possible
    print(cycle_vie)

if __name__ == '__main__':

    get_data_from_redis()

    r = redis.StrictRedis(REDIS_SERVER)
    ind = retrieveID(r, "File-74")
    retrieve_cycle(r, ind)
