from datetime import datetime, timedelta, timezone
import Credentials.credential as credential
import Database.history as history
from Credentials.credential import *
from pymongo import MongoClient
from ChatFlow.services import *
import Database.database as database
import MessageTools.flow as flow

def load_collect():
        client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.amtem.mongodb.net/{dbname}?retryWrites=true&w=majority")
        db = client[dbname]
        collectUsersMessage = db[collectqueue]

        return collectUsersMessage

def load_message(queue,name,number,messageid,text):
        user = {
            "usuario_id": name, 
            "numero_id": number,
            "mensage_id": messageid,
            "mensage": text,
            "fecha_inicio": datetime.datetime.now(datetime.timezone.utc),
        }
        newuser = queue.insert_one(user)
        return newuser

def send_message(queue):
        queueb = load_collect()
        for doc in queue.find():
                name=doc.get("usuario_id", None)
                number=doc.get("numero_id", None)
                messageId = doc.get("mensage_id", None)
                text = doc.get("mensage", None)
                flow.administrar_chatbot(text, number, messageId, name)

def verify_queue():
        collectQueue = load_collect()
        return collectQueue
