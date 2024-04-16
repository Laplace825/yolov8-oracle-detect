'''
Author: laplace825
Date: 2024-04-12 15:45:16
LastEditors: laplace825
LastEditTime: 2024-04-16 13:00:51
FilePath: /python/fastapi_test.py
Description: 

Copyright (c) 2024 by laplace825, All Rights Reserved. 
'''

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import uvicorn
from typing import Optional
from pydantic import BaseModel
import os

app = FastAPI()


class Client(BaseModel):
    name: str
    age: int
    email: str
    phone: str


clients: dict[int, Client] = {}
upload_loader = "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/test_img/"

@app.get("/")
def index():
    return {"message": "FastAPI !"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(upload_loader, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(content={"message": "Upload file success!"})
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": "An error occured, upload_file"}
        )


if __name__ == "__main__":
    uvicorn.run(app="fastapi_test:app", host="0.0.0.0", port=8000, reload=True)
