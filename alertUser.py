import credential
import history
from credential import *
from pymongo import MongoClient
from services import *

def alert():
    client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.amtem.mongodb.net/{dbname}?retryWrites=true&w=majority")
    db = client[dbname]
    collect = db[collect]

    # Obtener todos los números
    numeros = [doc.get("numero_id", "No encontrado") for doc in collect.find()]

    # Mostrar la lista de números
    print(numeros)

    for doc in collect.find():
        usuario_id = doc.get("usuario_id", "Sin usuario")
        numero_id = doc.get("numero_id", "Sin número")
        mensajes = doc.get("mensajes", [])
        if not "Solicitud enviada ✅" in mensajes[-1]["mensaje"]:
            answer = "¿Sigues interesado en realizar tu proyecto fotovoltaico con Greenglo? Te podriamos mostrar otras opciones que se ajusten a tu presupuesto, presiona Cotizar."
            replyButtonData = buttonReply_Message(numero_id, ["Cotizar"], answer, "Equipo Greenglo", "sed1", None)
            enviar_Mensaje_whatsapp(replyButtonData)            
            #print(f"Usuario: {usuario_id}, Número: {numero_id}, ultimo mensaje: {mensajes[-1]["mensaje"]}")

    """
        
        alert_message = "*Sigues interesado?*"
    for number in numeros:
        hist = history.historialwrite(name, -1)
        if history.historialread(hist,"agendar cita "):
            enviar_Mensaje_whatsapp(text_Message(number,alert_message))
        
    """






