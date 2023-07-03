from fastapi import FastAPI, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from typing import Annotated

app = FastAPI()

@app.post("/items")
def createItem(
  image: UploadFile, 
  price: Annotated[int, Form()], 
  place: Annotated[str, Form()], 
  title: Annotated[str, Form()], 
  description: Annotated[str, Form()], 
  insertAt: Annotated[int, Form()]):
  print(image, price, place, title, description, insertAt)
  return

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")