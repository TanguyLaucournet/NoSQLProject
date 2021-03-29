from datetime import datetime
import requests
import json

url = "http://localhost:3000/obj/register"

def fill_db():
    
    with open('jeuDeDonnees_1.log') as file:
        for line in file:
            json_element = json.loads(line)
            body = {"Id":json_element["id"],"Event_type":json_element["event-type"],"Date_creation":json_element["occurredOn"],"Date_ajout":str(datetime.now()),"Version_file":json_element["version"],"Graph_id":json_element["graph-id"],"Nature":json_element["nature"],"Object_name":json_element["object-name"],"Object_path":json_element["path"]}
            requests.post(url,data = body)
    
    print('MYSQL DATABASE FILLED')

if __name__ == '__main__':

    fill_db()
