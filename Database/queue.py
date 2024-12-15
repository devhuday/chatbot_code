import Database.history as history
import datetime
from pymongo import MongoClient
from ChatFlow.services import *
import Database.database as database
import ChatFlow.flow as flow
from Credentials.credential import *

class Queue:
	def __init__(self):
		self.client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.amtem.mongodb.net/{dbname}?retryWrites=true&w=majority")
		self.db = self.client[dbname]
		self.collection_message = self.db[collectqueue]
  
	def load_message (self,name,number,messageid,text):
			print("mensaje")
			user = {
				"usuario_id": name,
				"numero_id": number,
				"mensage_id": messageid,
				"mensage": text,
				"fecha_inicio": datetime.datetime.now(datetime.timezone.utc)
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
				print("mensaje enviado")
				result = self.collection_message.delete_one(doc)
				break

	def verify_queue(self):
			return self.collection_message.count_documents({}) 
