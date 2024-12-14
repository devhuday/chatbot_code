from pymongo import MongoClient
from Credentials.credential import *

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

def user_info(number):
    client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.amtem.mongodb.net/{dbname}?retryWrites=true&w=majority")
    db = client[dbname]
    collection = db[collectinfo]

    # Filtro
    filtro = {"numero_id": str(number)}

    # Pipeline de agregación
    pipeline = [
        {"$match": filtro},  # Filtrar por el usuario
        {"$project": {
            "_id":0,
            "usuario_nombre": 1,  # Incluir correo
            "usuario_numero": 1,   # Incluir número
            "usuario_correo": 1,
        }}
    ]

    # Ejecutar el pipeline
    resultado = list(collection.aggregate(pipeline))

    # Imprimir los valores concretos
    if resultado:  # Verificar que el resultado no esté vacío
        print(resultado)
        InfoUser = {
            'correo': resultado[0].get("usuario_correo", 'No disponible'),
            'numero': resultado[0].get("usuario_numero", "No disponible"),
            'nombre': resultado[0].get("usuario_nombre", "No disponible") 
        }
        correo = resultado[0].get("usuario_correo", 'No disponible')
        telefono = resultado[0].get("usuario_numero", "No disponible")
        nombre = resultado[0].get("usuario_nombre", "No disponible") 
        
    else:
        InfoUser = None   
    return nombre, correo, telefono

def historialmessages(resultado, clave):
    i=0
    for mensaj in resultado[0]["mensajes"]:
        if mensaj['mensaje'] == clave:
            return i
        i+=1
    