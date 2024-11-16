from pymongo import MongoClient
from credential import *

def historialwrite(nameuser,step):
    # Conexión a la base de datos
    client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.amtem.mongodb.net/{dbname}?retryWrites=true&w=majority")
    db = client[dbname]
    collection = db[collect]

    filtro = {"usuario_id": nameuser}  # Puedes usar otro campo si lo prefieres

    pipeline = [
        {"$match": filtro},  # Filtrar por el usuario
        {"$project": {
            "mensajes": {"$slice": ["$mensajes", step]}  # Obtener los últimos tres elementos del array
        }}
    ]

    resultado = list(collection.aggregate(pipeline))
    return resultado

def historialread(resultado, clave):
    check = None
    i = 0
    """
    for mensaje in resultado[0]["mensajes"]:
        print(i)
        print(f"Emisor: {mensaje['emisor']}")
        print(f"Mensaje: {mensaje['mensaje']}")
        print(f"Timestamp: {mensaje['timestamp']}")
        print("----------")
    """
    
    for mensaj in resultado[0]["mensajes"]:
        if mensaj['mensaje'] == clave:
            check = f"se envia el correo + {clave}" 
    print(check) if check else print(f"No se envia el correo + {clave}")

    return check

def historialmessages(resultado, clave):
    i=0
    for mensaj in resultado[0]["mensajes"]:
        if mensaj['mensaje'] == clave:
            return i
        i+=1
    