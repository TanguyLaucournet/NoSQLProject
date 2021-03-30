import redis

REDIS_SERVER = 'localhost'

def get_data_from_redis():
    r2 = redis.StrictRedis(REDIS_SERVER)
    # LIRE REDIS POUR VERIFIER QUE TOUT EST CORRECTEMENT IMPLEMENTE
    for i in range(1,int(r2.get("datas").decode()) + 1):
            print(i)
            print(r2.hget(i,"id").decode())
            print(r2.hget(i,"object-name").decode())
            # print(r2.hget(i,"path").decode())

def retrieveID(r, target):
    lindex = []
    for i in range(1,int(r.get("datas").decode())+1):
        if r.hget(i,"object-name").decode() == target:
            lindex.append(i)
            print(r.hget(i,"id").decode())
            print(lindex)

    return lindex


def retrieve_cycle(r, lindex):
    cycle_vie = []
    for elem in lindex:
        cycle_vie.append(r.lindex("path",800-elem*8).decode())
        cycle_vie.append(r.lindex("path",800-elem*8+1).decode())
        cycle_vie.append(r.lindex("path",800-elem*8+2).decode())
        cycle_vie.append(r.lindex("path",800-elem*8+3).decode())
        cycle_vie.append(r.lindex("path",800-elem*8+4).decode())
        cycle_vie.append(r.lindex("path",800-elem*8+5).decode())
        cycle_vie.append(r.lindex("path",800-elem*8+6).decode())
        cycle_vie.append(r.lindex("path",800-elem*8+7).decode())
        #etc jusqu'a ce qu'on ait tout le elem possible
    return cycle_vie

def polish_cycle_vie(cycle_vie):
    polished_cycle_vie = [0,0,0,0,0,0,0,0]
    for i in range(len(cycle_vie)):
        if(i%8 == 0):
            if(cycle_vie[i] == '1'):                
                polished_cycle_vie[0] ='To_Be_Purged'
        if(i%8 == 1):
            if(cycle_vie[i] == '1'):  
                polished_cycle_vie[1] ='Purged'
        if(i%8 == 2):
            if(cycle_vie[i] == '1'):  
                polished_cycle_vie[2]= 'Received'
        if(i%8 == 3):
            if(cycle_vie[i] == '1'):  
                polished_cycle_vie[3] = 'Verified'
        if(i%8 == 4):
            if(cycle_vie[i] == '1'):  
                polished_cycle_vie[4]='Processed'
        if(i%8 == 5):
            if(cycle_vie[i] == '1'):   
                polished_cycle_vie[5]='Rejected'
        if(i%8 == 6):
            if(cycle_vie[i] == '1'):  
                polished_cycle_vie[6]='Remedied'
        if(i%8 == 7):
            if(cycle_vie[i] == '1'):  
                polished_cycle_vie[7] = 'Consumed'

    return polished_cycle_vie


def clean_data(array):
    f_arra = []
    for elem in array:
        if elem != 0:
            f_arra.append(elem)
    return f_arra


def set_target():
    target = input("Entrez le status dont vous voulez avoir le nombre d'objet(TO_BE_PURGED,PURGED,RECEIVED,VERIFIED,PROCESSED,REJECTED,REMEDIED, CONSUMED) : ").upper()
    indic = -1
    if target == 'TO_BE_PURGED':
        indic = 0
    if target == 'PURGED':
        indic = 1
    if target == 'RECEIVED':
        indic = 2
    if target == 'VERIFIED':
        indic = 3
    if target == 'PROCESSED':
        indic = 4
    if target == 'REJECTED':
        indic = 5
    if target == 'REMEDIED':
        indic = 6
    if target == 'CONSUMED':
        indic = 7
    return indic

def count_state(r):
    target = set_target()
    count = 0
    i = target
    while(i<r.llen("path")):
        if(r.lindex("path",i).decode() =='1'):
            count = count+1
        i = i + 8
    return count

def verified_life(r):
    life_state_1 = ['To_Be_Purged', 'Purged', 'Received', 'Verified', 'Processed','Consumed']
    life_state_2 = ['To_Be_Purged', 'Purged', 'Received', 'Verified', 'Processed','Rejected']
    life_state_3 =['Received', 'Verified', 'Processed', 'Rejected', 'Remedied', 'To_Be_Purged', 'Purged', 'Consumed']
    life_state_4 = ['Received', 'Verified', 'Processed', 'Rejected', 'Remedied', 'To_Be_Purged', 'Purged']
    count = 0
    already_verified = []
    for i in range(1,int(r.get("datas").decode())+1):
        object_name = r.hget(i,"object-name").decode()
        if object_name not in already_verified:
            already_verified.append(object_name)
            lindex = retrieveID(r,object_name)
            cycle_vie = retrieve_cycle(r,lindex)
            final = clean_data(polish_cycle_vie(cycle_vie))
            if final == life_state_1 or final == life_state_2 or final == life_state_3 or final == life_state_4:
                count = count+1
    print(count)

if __name__ == '__main__':

    # get_data_from_redis()

    r = redis.StrictRedis(REDIS_SERVER)
    ind = retrieveID(r, "File-74")
    cycle_vie = retrieve_cycle(r, ind)
    array = polish_cycle_vie(cycle_vie)
    #print(count_state(r))
    verified_life(r)
