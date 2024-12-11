import datetime
import credential
import history
from credential import *
from pymongo import MongoClient
from services import *

class Alerts:

    def __init__(self):
        self.client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.amtem.mongodb.net/{dbname}?retryWrites=true&w=majority")
        self.db = self.client[dbname]
        self.collection = self.db[collect]
        self.collection_userAlarm = self.db[credential.collectAlarm]

    def message(self,numero_id):
        answer = "¿Sigues interesado en realizar tu proyecto fotovoltaico con Greenglo? Te podriamos mostrar otras opciones que se ajusten a tu presupuesto, presiona Cotizar."
        replyButtonData = buttonReply_Message(numero_id, ["Cotizar"], answer, "Equipo Greenglo", "sed1", None)
        enviar_Mensaje_whatsapp(replyButtonData)
        
    def alert(self):
        # Obtener todos los números
        numeros = [doc.get("numero_id", "No encontrado") for doc in self.collection.find()]

        for doc in self.collection.find():
            numero_id = doc.get("numero_id", "Sin número")
            mensajes = doc.get("mensajes", [])[-8:]
            time = mensajes[-1]["timestamp"] 
            if not any("Solicitud enviada ✅" in mensaje.get("mensaje", "") for mensaje in mensajes):
                if time:
                    time = time if isinstance(time, datetime.datetime) else time["$date"]
                    time = datetime.datetime.fromisoformat(time.replace("Z", "+00:00"))
                current_time = datetime.datetime.now(datetime.timezone.utc)
                delta_24_hours = datetime.timedelta(minutes=1)

                if (current_time - time) > delta_24_hours:
                    self.message(numero_id)

    def check_and_process_recordatory(self):
        # Obtener la hora actual
        current_time = datetime.datetime.now(datetime.timezone.utc)
        
        # Buscar documentos con más de 3 minutos desde "fecha_inicio"
        alarms = self.collection_userAlarm.find()
        for alarm in alarms:
            fecha_inicio = alarm.get("fecha_inicio")
            if fecha_inicio and (current_time - fecha_inicio).total_seconds() > 180:
                # Extraer los datos necesarios
                usuario_id = alarm.get("usuario_id")
                numero_id = alarm.get("numero_id")
                
                # Realizar la acción (puedes reemplazar esto con tu lógica específica)
                print(f"Procesando alarma de usuario: {usuario_id}, número: {numero_id}")
                
                # Eliminar el documento
                self.collection_userAlarm.delete_one({"_id": alarm["_id"]})



