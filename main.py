from fastapi import FastAPI, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

app = FastAPI()

CON = sqlite3.connect("database.db")
cur = CON.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY NOT NULL,
  image BLOB,
  price INTEGER NOT NULL,
  place TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  insertAt INTEGER NOT NULL
  )""")
cur.close()

@app.post("/items")
async def createItem(
              image: UploadFile, 
              price: Annotated[int, Form()], 
              place: Annotated[str, Form()], 
              title: Annotated[str, Form()], 
              description: Annotated[str, Form()], 
              insertAt: Annotated[int, Form()]):
  cursor = CON.cursor()
  IMG_BINARY = await image.read()
  
  cursor.execute(f"""INSERT INTO items (image, price, place, title, description, insertAt)
                  VALUES ('{IMG_BINARY.hex()}', {price}, '{place}', '{title}', '{description}', {insertAt})""")
  cursor.close()
  CON.commit()
  return "200"

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")