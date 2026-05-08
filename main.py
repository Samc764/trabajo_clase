from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float

mock_items = [
    Item(id=1, name="Camiseta", description="Camiseta de algodón", price=19.99),
    Item(id=2, name="Libreta", description="Libreta para apuntes", price=7.5),
    Item(id=3, name="Mochila", description="Mochila escolar", price=34.0),
]

@app.get("/", tags=["home"])
def read_root() -> dict:
    return {"message": "FastAPI está funcionando correctamente."}

@app.get("/items", response_model=List[Item], tags=["items"])
def get_items() -> List[Item]:
    return mock_items

@app.get("/items/{item_id}", response_model=Item, tags=["items"])
def get_item(item_id: int) -> Item:
    for item in mock_items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item no encontrado")

@app.post("/items", response_model=Item, tags=["items"])
def create_item(item: Item) -> Item:
    if any(existing.id == item.id for existing in mock_items):
        raise HTTPException(status_code=400, detail="El id del item ya existe")
    mock_items.append(item)
    return item
