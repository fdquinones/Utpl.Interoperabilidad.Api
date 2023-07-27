from fastapi import FastAPI, HTTPException, Depends 
from pydantic import BaseModel
from typing import List, Optional
import uuid

from fastapi_versioning import VersionedFastAPI, version

from fastapi.security import HTTPBasic, HTTPBasicCredentials

from auth import authenticate

#seccion mongo importar libreria
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

#para agregar seguridad a nuestro api
security = HTTPBasic()

#configuración de mongo 
producto = pymongo.MongoClient("mongodb+srv://utplapi:123456marlyn.@cluster0.jtcw0qx.mongodb.net/?retryWrites=true&w=majority")
database = producto["biblioteca"]
coleccion = database["productos"]

class ProductoRepositorio (BaseModel):
    id: str
    nombre: str
    cantidad: int
    detalle: Optional[str] = None

class ProductoEntrada (BaseModel):
    id: str
    nombre:str
    cantidad:int
    detalle: Optional[str] = None

class ProductoEntradaV2 (BaseModel):
    nombre:str
    cantidad:int
    detalle: str
    codigobarra: Optional[str] = None

productoList = []

@app.post("/productos", response_model=ProductoRepositorio,tags=["productos"])
@version(1, 0)
async def crear_producto(productoE: ProductoEntrada):
    itemProducto = ProductoRepositorio (id= str(uuid.uuid4()), nombre = productoE.nombre, cantidad = productoE.cantidad, detalle = detalleE.detalle)
    resultadoDB =  coleccion.insert_one(itemProducto.dict())
    return itemProducto

@app.post("/productos", response_model=ProductoRepositorio, tags=["productos"])
@version(2, 0)
async def crear_producto2(productoE: ProductoEntradaV2):
    itemProducto = ProductoRepositorio (id= str(uuid.uuid4()), nombre = productoE.nombre, cantidad = productoE.cantidad, detalle = productoE.detalle)
    resultadoDB =  coleccion.insert_one(itemProducto.dict())
    return itemProducto

@app.get("/productos", response_model=List[ProductoRepositorio], tags=["productos"])
@version(1, 0)
def get_productos(credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)
    items = list(coleccion.find())
    print (items)
    return items

@app.get("/productos/{producto_id}", response_model=ProductoRepositorio , tags=["productos"])
@version(1, 0)
def obtener_productos (producto_id: str):
    item = coleccion.find_one({"id": producto_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.delete("/productos/{producto_id}", tags=["productos"])
@version(1, 0)
def eliminar_producto (producto_id: str):

    result = coleccion.delete_one({"id": producto_id})
    if result.deleted_count == 1:
        return {"mensaje": "Producto eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.get("/pista/{pista_id}", tags = ["artistas"])
@version(1, 0)
async def obtener_track(pista_id: str):
    track = sp.track(pista_id)
    return track
    
@app.get("/artistas/{artista_id}", tags = ["artistas"])
@version(1, 0)
async def get_artista(artista_id: str):
    artista = sp.artist(artista_id)
    return artista

@app.get("/")
def read_root():
    return {"Bienvenido": "Usuario/NombreApellido2"}

app = VersionedFastAPI(app)
