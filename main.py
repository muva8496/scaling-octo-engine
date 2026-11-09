# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import engine, Base
from models import ItemModel
from dependency import get_db  # Matches your dependency.py file

app = FastAPI(title="Quickmart Retail API", version="1.0.0")

# --- Pydantic Schemas for Validation ---
class ItemCreate(BaseModel):
    id: str # Allow passing "P0031"
    name: str
    price: float
    stock: int

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int | None = None


# --- 1. CREATE Endpoint ---
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = ItemModel(name=item.name, price=item.price, stock=item.stock)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return {"message": "Item created successfully", "data": db_item}


# --- 2. READ ALL Endpoint ---
@app.get("/items/", status_code=status.HTTP_200_OK)
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel))
    items = result.scalars().all()
    return items


# --- 3. READ SINGLE Endpoint ---
@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel).where(ItemModel.id == item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# --- 4. UPDATE Endpoint ---
@app.put("/items/{item_id}", status_code=status.HTTP_200_OK)
async def update_item(item_id: int, item_data: ItemUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel).where(ItemModel.id == item_id))
    db_item = result.scalars().first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item_data.name is not None:
        db_item.name = item_data.name
    if item_data.price is not None:
        db_item.price = item_data.price
    if item_data.stock is not None:
        db_item.stock = item_data.stock

    await db.commit()
    await db.refresh(db_item)
    return {"message": "Item updated successfully", "data": db_item}


# --- 5. DELETE Endpoint ---
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel).where(ItemModel.id == item_id))
    db_item = result.scalars().first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    await db.delete(db_item)
    await db.commit()
    return None