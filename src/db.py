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
    
    def insert_sports(self, sports_data):
        client = self.get_client()
        db = client[self.name]
        sports_coll = db[self.collections["sports"]]
        for sport_key, title, desc in sports_data:
            doc = {"_id": sport_key, "title":title, "desc":desc}
            sports_coll.insert_one(doc)
        client.close()

    def get_client(self):
        return MongoClient(self.addr, self.port)

