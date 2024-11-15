from pymongo import MongoClient
import datetime
import credential

class Conversacion:
    def __init__(self, number, messageId, username):
        
        self.username = username
        self.number = number
        self.messageId = messageId
        
        # URI de conexión
        self.client = MongoClient(f"mongodb+srv://{credential.user}:{credential.password}@{credential.cluster}.amtem.mongodb.net/{credential.dbname}?retryWrites=true&w=majority")
        self.db = self.client[credential.dbname]
        self.collection = self.db[credential.collect]
        self.collection_userinfo = self.db[credential.collect]
        
    def check_User(self):
        print("dnqijnd")
        user = self.collection.find_one({"numero_id": self.number})
        return user
    
    def check_user_info(self):
        user_info = self.collection_userinfo.find_one({"usuario":self.username})
        pass


    def new_user(self):
        user = {
            "usuario_id": self.username,
            "numero_id": self.number,
            #"fecha_inicio": datetime.datetime.now(datetime.timezone.utc),
            #"fecha_fin": datetime.datetime.now(datetime.timezone.utc) ,
            "mensajes": []
        }
        
        new_user_info = self.collection_userinfo.insert_one(user)
        return new_user_info
    
    def new_userinfo(self,name,numberx,correo):
        user = {
            "usuario_id": self.username,
            "numero_id": self.number,
            "usuario_nombre": name,
            "usuario_numero": numberx,
            "usuario_correo": correo,
            #"fecha_inicio": datetime.datetime.now(datetime.timezone.utc),
            #"fecha_fin": datetime.datetime.now(datetime.timezone.utc) ,
        }
        
        newuser = self.collection.insert_one(user)
        return newuser
    
    def new_message(self, usertype, text):
        
        filtro = {
            "usuario_id": self.username,
            "numero_id": self.number
        }
        
        message = {
            "emisor": usertype,
            "mensaje": text,
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
        }
        
        newmessage = self.collection.update_one(filtro, {"$push": {"mensajes": message}})

    