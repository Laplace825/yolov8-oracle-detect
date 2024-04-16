'''
Author: laplace825
Date: 2024-04-12 15:45:16
LastEditors: laplace825
LastEditTime: 2024-04-15 23:07:02
FilePath: /python/fastapi_test.py
Description: 

Copyright (c) 2024 by laplace825, All Rights Reserved. 
'''
from fastapi import FastAPI
import uvicorn
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


class Client(BaseModel):
    name: str
    age: int
    email: str
    phone: str


clients: dict[int, Client] = {}


@app.get("/")
def index():
    return {"message": "FastAPI !"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/people/{item_id}")
def create_client(item_id: int, client: Client):
    age = client.age
    name = client.name
    email = client.email
    phone = client.phone
    clients[item_id] = {"name": name, "age": age, "email": email, "phone": phone}
    msg = f"{name} is {age} years old, email: {email}, phone: {phone}"
    return {"success": True, "message": msg}


@app.get("/people/{item_id}")
def get_client(item_id: int):
    return {f"client_{item_id}": clients[item_id]}


if __name__ == "__main__":
    uvicorn.run(app="fastapi_test:app", host="0.0.0.0", port=8000, reload=True)
