from pymongo import MongoClient
from Credentials.credential import *
# Conexión con MongoDB
client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.amtem.mongodb.net/{dbname}?retryWrites=true&w=majority")
db = client[dbname]
collection = db[collectinfo]

# Filtro
filtro = {"numero_id": "573058031242"}

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
    print(f"Correo: {InfoUser['correo']}")
    print(f"Número: {InfoUser['numero']}")
    print(f"Nombre: {InfoUser['nombre']}")
else:
    print("No se encontraron documentos con el filtro especificado.")
