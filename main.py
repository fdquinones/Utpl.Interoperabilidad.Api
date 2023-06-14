from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import spotipy

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
    client_id='926560c38be7457d82a4a191450d60b5',
    client_secret='1540ff683c5640429701be0900ceba6f'
))

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "personas",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)

class Persona (BaseModel):
    id: int
    nombre: str
    edad: int
    ciudad: Optional[str] = None

personaList = []

@app.post("/personas", response_model=Persona)
def crear_persona(person: Persona):
    personaList.append(person)
    return person

@app.get("/personas", response_model=List[Persona])
def get_personas():
    return personaList

@app.get("/personas/{persona_id}", response_model=Persona)
def obtener_persona (persona_id: int):
    for persona in personaList:
        if persona.id == persona_id:
            return persona
    raise HTTPException(status_code=404, detail="Persona no encontrada")

@app.delete("/personas/{persona_id}")
def eliminar_persona (persona_id: int):
    persona = next((p for p in personaList if p.id == persona_id), None)
    if persona:
        personaList.remove(persona)
        return {"mensaje": "Persona eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

@app.get("/tracks/{track_id}")
async def get_track(track_id: str):
    track = sp.track(track_id)
    return track
    
@app.get("/")
def read_root():
    return {"Hello": "Interoperabilidad 8"}
