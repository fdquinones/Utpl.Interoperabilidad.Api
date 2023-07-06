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
    client_id='c8519595485648c3949369793de3e366',
    client_secret='d266e54ea24346a7b278445be87cd400'
))

description = """
Utpl tnteroperabilidad API ayuda a describir las capacidades de un directorio. 🚀

## Personas

Tu puedes crear una persona.
Tu puedes listar personas.


## Artistas

You will be able to:

* **Crear artista** (_not implemented_).
"""

tags_metadata = [
    {
        "name":"personas",
        "description": "Permite realizar un crud completo de una persona (listar)"
    },
    {
        "name":"artistas",
        "description": "Permite realizar un crud completo de un artista"
    },
]

app = FastAPI(
    title="Utpl Interoperabilidad APP 2",
    description= description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Felipe Quiñonez",
        "url": "http://x-force.example.com/contact/",
        "email": "fdquinones@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags = tags_metadata
)

#para agregar seguridad a nuestro api
security = HTTPBasic()

#configuracion de mongo
cliente = pymongo.MongoClient("mongodb+srv://utplinteroperabilidad:0b1Fd3PFZZInSuZK@cluster0.susnphb.mongodb.net/?retryWrites=true&w=majority")
database = cliente["directorio"]
coleccion = database["persona"]

class PersonaRepositorio (BaseModel):
    id: str
    nombre: str
    edad: int
    identificacion: Optional[str] = None
    ciudad: Optional[str] = None

class PersonaEntrada (BaseModel):
    nombre:str
    edad:int
    ciudad: Optional[str] = None

class PersonaEntradaV2 (BaseModel):
    nombre:str
    edad:int
    identificacion:str
    ciudad: Optional[str] = None


personaList = []

@app.post("/personas", response_model=PersonaRepositorio, tags = ["personas"])
@version(1, 0)
async def crear_persona(personE: PersonaEntrada):
    itemPersona = PersonaRepositorio (id= str(uuid.uuid4()), nombre = personE.nombre, edad = personE.edad, ciudad = personE.ciudad)
    resultadoDB =  coleccion.insert_one(itemPersona.dict())
    return itemPersona

@app.post("/personas", response_model=PersonaRepositorio, tags = ["personas"])
@version(2, 0)
async def crear_personav2(personE: PersonaEntradaV2):
    itemPersona = PersonaRepositorio (id= str(uuid.uuid4()), nombre = personE.nombre, edad = personE.edad, ciudad = personE.ciudad, identificacion = personE.identificacion)
    resultadoDB =  coleccion.insert_one(itemPersona.dict())
    return itemPersona

@app.get("/personas", response_model=List[PersonaRepositorio], tags=["personas"])
@version(1, 0)
def get_personas():
    print ("llego a consultar todas las personas")
    items = list(coleccion.find())
    print (items)
    return items

@app.get("/personas/{persona_id}", response_model=PersonaRepositorio , tags=["personas"])
@version(1, 0)
def obtener_persona (persona_id: str):
    item = coleccion.find_one({"id": persona_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

@app.delete("/personas/{persona_id}", tags=["personas"])
@version(1, 0)
def eliminar_persona (persona_id: str):
    result = coleccion.delete_one({"id": persona_id})
    if result.deleted_count == 1:
        return {"mensaje": "Persona eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

@app.get("/pista/{pista_id}", tags = ["artistas"])
@version(1, 0)
async def obtener_pista(pista_id: str):
    track = sp.track(pista_id)
    return track
    
@app.get("/artistas/{artista_id}", tags = ["artistas"])
@version(1, 0)
async def get_artista(artista_id: str):
    artista = sp.artist(artista_id)
    return artista


@app.get("/")
def read_root():
    return {"Hello": "Interoperabilidad 8"}

app = VersionedFastAPI(app)