from pymongo import MongoClient
from dotenv import load_dotenv
import os

def get_db_config():
    load_dotenv('.env')
    name = os.getenv("dbName")
    port = int(os.getenv("dbPort"))
    addr = os.getenv("dbAddr")
    return {"name": name, 
            "port": port, 
            "addr": addr, 
            }
    
def init_db_conn():
    db_info = get_db_config()
    client = MongoClient(db_info["addr"], db_info["port"])
    db = client[db_info["name"]]
    return db, client

def main():
    db, client = init_db_conn()
    main_coll = db["arbs"]

    sample_data = {"ev": 5, "home": "gimble", "away": "brimble"}
    main_coll.insert_one(sample_data)

    client.close()

if __name__ == '__main__':
    main()
