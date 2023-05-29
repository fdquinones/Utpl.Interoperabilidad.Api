from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

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

@app.get("/")
def read_root():
    return {"Bienvenido": "Usuario/Nombre"}
