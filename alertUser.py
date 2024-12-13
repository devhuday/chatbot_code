from datetime import datetime, timedelta, timezone
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
        self.collection_userAlarm = self.db[collectAlarm]
    
    def message(self,numero_id):
        answer = "¿Sigues interesado en realizar tu proyecto fotovoltaico con Greenglo? Te podriamos mostrar otras opciones que se ajusten a tu presupuesto, presiona Cotizar."
        replyButtonData = buttonReply_Message(numero_id, ["Cotizar"], answer, "Equipo Greenglo", "sed1", None)
        enviar_Mensaje_whatsapp(replyButtonData)
        
    def alertGeneral(self):
        # Obtener todos los números
        numeros = [doc.get("numero_id", "No encontrado") for doc in self.collection.find()]
        print("entrrara?")
        for doc in self.collection.find():
            numero_id = doc.get("numero_id", "Sin número")
            mensajes = doc.get("mensajes", [])[-8:]
            time = mensajes[-1]["timestamp"] 
            print(numero_id)
            print(time)
            if not any("Solicitud enviada ✅" in mensaje.get("mensaje", "") for mensaje in mensajes):
                if time:
                    timestamp = time.replace(tzinfo=timezone.utc) if time.tzinfo is None else time
                    # Calcular la diferencia de tiempo 
                    delta = timedelta(hours=24) 
                    hora_esperada = timestamp + delta
                    timeNow = datetime.now(timezone.utc)

                if timeNow > hora_esperada:
                    self.message(numero_id)

    def check_and_process_recordatory(self):
        # Obtener la hora actual
        current_time = datetime.now(timezone.utc)
        print("check")
        # Buscar documentos con más de 3 minutos desde "fecha_inicio"
        alarms = self.collection_userAlarm.find()
        for alarm in alarms:
            fecha_inicio = alarm.get("fecha_inicio")
            fecha_inicio = fecha_inicio.replace(tzinfo=timezone.utc) if fecha_inicio.tzinfo is None else fecha_inicio
            if fecha_inicio and (current_time - fecha_inicio) > timedelta(minutes=4):
                # Extraer los datos necesarios
                usuario_id = alarm.get("usuario_id")
                numero_id = alarm.get("numero_id")
                print("sale")
                alertt = buttonReply_Message(numero_id, ["Agendar cita 🗓️"], f"{usuario_id}¿Sigues interesado en nuestos servicios? Presiona el botón y podras agendar una cita con uno asesor.", "", "sed1", None)
                enviar_Mensaje_whatsapp(alertt)
                
                # Eliminar el documento
                self.collection_userAlarm.delete_one({"_id": alarm["_id"]})



