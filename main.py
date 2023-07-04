from fastapi import FastAPI, Form, UploadFile, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import Annotated
import sqlite3
from fastapi.encoders import jsonable_encoder

app = FastAPI()

CON = sqlite3.connect("database.db", check_same_thread=False)
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
  IMG_BYTES = await image.read()
  
  cursor.execute(f"""INSERT INTO items (image, price, place, title, description, insertAt)
                  VALUES ('{IMG_BYTES.hex()}', {price}, '{place}', '{title}', '{description}', {insertAt})""")
  cursor.close()
  CON.commit()
  return "200"

@app.get("/items")
def readItems():
  CON.row_factory = sqlite3.Row
  cursor = CON.cursor()
  rows = cursor.execute("""SELECT * FROM items
                        ORDER BY insertAt DESC""").fetchall()  
  cursor.close()
  return JSONResponse(jsonable_encoder(dict(row) for row in rows))

@app.get("/images/{item_id}")
def readImage(item_id):
  cursor = CON.cursor()
  IMAGE_HEX = cursor.execute(f"""SELECT image FROM items
                  WHERE id={int(item_id)}""").fetchone()[0]
  cursor.close()
  return Response(content=bytes.fromhex(IMAGE_HEX), media_type="image/*")

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")