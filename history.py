from pymongo import MongoClient
from credential import *

# Conexión a la base de datos
client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.amtem.mongodb.net/{dbname}?retryWrites=true&w=majority")
db = client[dbname]
collection = db[collect]

# Identificar al usuario por su usuario_id o numero_id
filtro = {"usuario_id": "Hudaay✨"}  # Puedes usar otro campo si lo prefieres

# Proyección para obtener los tres últimos mensajes
pipeline = [
    {"$match": filtro},  # Filtrar por el usuario
    {"$project": {
        "mensajes": {"$slice": ["$mensajes", -3]}  # Obtener los últimos tres elementos del array
    }}
]

# Ejecutar la consulta
resultado = list(collection.aggregate(pipeline))

if resultado:
    
    print("+++++++++----------++++++++++++")
    for mensaje in resultado[0]["mensajes"]:
        print(f"Emisor: {mensaje['emisor']}")
        print(f"Mensaje: {mensaje['mensaje']}")
        print(f"Timestamp: {mensaje['timestamp']}")
        print("----------")
    print("+++++++++----------++++++++++++")
    check = None
    for mensaj in resultado[0]["mensajes"]:
        if mensaj['mensaje'] == "agendar cita 🗓️":
            check = "se envia el correo"
    print(check) if check else print("No se envia el correo")
else:
    print("No se encontraron resultados.")