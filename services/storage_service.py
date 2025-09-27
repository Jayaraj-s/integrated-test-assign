from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict
from .auth_service import get_current_user, require_role
from uuid import uuid4

router = APIRouter()

class ItemIn(BaseModel):
    name: str
    value: str

class Item(ItemIn):
    id: str

# In-memory storage (id -> Item)
DB: Dict[str, Item] = {}


@router.post("/items", response_model=Item)
def create_item(item: ItemIn, payload=Depends(get_current_user)):
    item_id = str(uuid4())
    new = Item(id=item_id, **item.model_dump())
    DB[item_id] = new
    return new

@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: str, payload=Depends(get_current_user)):
    item = DB.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return item

@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, item_in: ItemIn, payload=Depends(get_current_user)):
    existing = DB.get(item_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    updated = Item(id=item_id, **item_in.model_dump())
    DB[item_id] = updated
    return updated

@router.delete("/items/{item_id}")
def delete_item(item_id: str, payload=Depends(require_role("admin"))):
    # only admin can delete
    if item_id not in DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    del DB[item_id]
    return {"deleted": True}

@router.get("/items")
def list_items(payload=Depends(get_current_user)):
    return list(DB.values())
