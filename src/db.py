from pymongo import MongoClient
from dotenv import load_dotenv
import os

class ArbDB:
    def __init__(self):
        load_dotenv('.env')
        self.name = os.getenv("dbName")
        self.port = int(os.getenv("dbPort"))
        self.addr = os.getenv("dbAddr")
        self.collections = {"main":"arbs", "sports":"sport_keys"}
    
    def insert_arb(self, arb):
        client = self.get_client()
        db = client[self.name]
        arb_coll = db[self.collections["main"]]
        arb_coll.insert_one(arb)
        client.close()
    
    def insert_sports(self, sport_keys):
        client = self.get_client()
        db = client[self.name]
        sports_coll = db[self.collections["sports"]]
        for sk in sport_keys:
            sports_coll.insert_one({"key": sk})
        client.close()

    def get_client(self):
        return MongoClient(self.addr, self.port)

