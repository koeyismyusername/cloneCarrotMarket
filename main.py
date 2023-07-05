from fastapi import FastAPI, Form, UploadFile, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import Annotated
import sqlite3
from fastapi.encoders import jsonable_encoder
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

app = FastAPI()

SECERET = "koeyismyusername"
MANAGER = LoginManager(SECERET, "/login")

CON = sqlite3.connect("database.db", check_same_thread=False)
CON.row_factory = sqlite3.Row
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
cur.execute("""CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL
  )""")
cur.close()

@MANAGER.user_loader()
def queryUser(id):
  cur = CON.cursor()
  result = cur.execute(f"""SELECT * FROM users
                      WHERE id='{id}'""").fetchone()
  cur.close()
  return result

@app.post("/login")
def login(id: Annotated[str, Form()],
          password: Annotated[str, Form()]):
  user = queryUser(id)
  if not user:
    raise InvalidCredentialsException
  elif password != user["password"]:
    raise InvalidCredentialsException
  
  access_token = MANAGER.create_access_token(data= {
    "id": user["id"],
    "name": user["name"],
    "email": user["email"],
  })
  
  return access_token
  
@app.post("/signup")
def signup(id: Annotated[str, Form()],
          password: Annotated[str, Form()],
          name: Annotated[str, Form()],
          email: Annotated[str, Form()]):
  cur = CON.cursor()
  existingId = cur.execute(f"""SELECT id FROM users
                      WHERE id='{id}'""").fetchone()
  
  if existingId:
    print("이미 해당 아이디가 존재합니다.")
    cur.close()
    return "401"
  
  cur.execute(f"""INSERT INTO users (id, name, email, password)
            VALUES ('{id}', '{name}', '{email}', '{password}')""")
  CON.commit()
  cur.close()
  return "200"

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