from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
#Importar Mongo

import pymongo
import spotipy

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
    client_id='43db35ef5cb14129ae36b4eae0ce8b25 ',
    client_secret='a755432558574a318edffb505e5969d8',
))

description = """
Utpl tnteroperabilidad API ayuda a clasificar productos en una tienda. 🚀

## Productos

Tu puedes crear un producto.
Tu puedes listar productos.
## Artistas

You will be able to:

* **Crear artista** (_not implemented_).
"""

tags_metadata = [
    {
        "name":"productos",
        "description": "Permite realizar un crud completo de un producto (listar)"
    },
    {
        "name":"artistas",
        "description": "Permite realizar un crud completo de un artista"
    },
]
app = FastAPI(
    title="Utpl Interoperabilidad Tarea",
    description= description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Marlyn Troya",
        "url": "http://x-force.example.com/contact/",
        "email": "matroya7@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags = tags_metadata
)
#configuración de mongo 
producto = pymongo.MongoProducto("mongodb+srv://MarTroya:123456marlyn>@cluster0.jtcw0qx.mongodb.net/?retryWrites=true&w=majority")
database = producto["biblioteca"]
coleccion = database["productos"]

class Producto (BaseModel):
    id: int
    nombre: str
    cantidad: int
    detalle: Optional[str] = None

productoList = []

@app.post("/productos", response_model=Producto)
def crear_producto(product: Producto):
    productoList.append(product)
    return product

@app.get("/productos", response_model=List[Producto])
def get_productos():
    return productoList

@app.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto (producto_id: int):
    for producto in productoList:
        if producto.id == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrada")

@app.delete("/productos/{producto_id}")

def eliminar_producto (producto_id: int):

    producto = next((p for p in productoList if p.id == producto_id), None)

    if producto:

        productoList.remove(producto)

        return {"mensaje": "Producto eliminado exitosamente"}

    else:

        raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.get("/pista/{pista_id}")

async def obtener_pista(pista_id: str):

    track = sp.track(pista_id)

    return track

@app.get("/")
def read_root():
    return {"Bienvenido": "Usuario/NombreApellido1"}
