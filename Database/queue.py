from datetime import datetime, timedelta, timezone
import Database.history as history
from Credentials.credential import *
from pymongo import MongoClient
from ChatFlow.services import *
import Database.database as database
import MessageTools.flow as flow

class Queue:
	def __init__(self):
		self.client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.amtem.mongodb.net/{dbname}?retryWrites=true&w=majority")
		self.db = self.client[dbname]
		self.collection = self.db[collect]
		self.collection_message = self.db[collectqueue]

	def load_message(self,name,number,messageid,text):
		user = {
			"usuario_id": name, 
			"numero_id": number,
			"mensage_id": messageid,
			"mensage": text,
			"fecha_inicio": datetime.datetime.now(datetime.timezone.utc),
		}
		newuser = self.collection_message.insert_one(user)
		return newuser

	def send_message(self):
		for doc in self.collection_message.find():
			name=doc.get("usuario_id", None)
			number=doc.get("numero_id", None)
			messageId = doc.get("mensage_id", None)
			text = doc.get("mensage", None)
			flow.administrar_chatbot(text, number, messageId, name)

	def verify_queue(self):
			return self.collection_message
