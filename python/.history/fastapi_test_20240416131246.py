"""
Author: laplace825
Date: 2024-04-12 15:45:16
LastEditors: laplace825
LastEditTime: 2024-04-16 13:00:51
FilePath: /python/fastapi_test.py
Description: 

Copyright (c) 2024 by laplace825, All Rights Reserved. 
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import uvicorn
from typing import Optional
from pydantic import BaseModel
import os
import sys
from datetime import datetime

app = FastAPI()


class Client(BaseModel):
    name: str
    age: int
    email: str
    phone: str


clients: dict[int, Client] = {}
# 当前工作区
upload_loader = os.path.abspath(os.path.dirname(sys.argv[0]))


@app.get("/")
def index():
    return {"message": "FastAPI !"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# 提交文件
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 根据当前上传时间新建文件夹，并把文件保存到该文件夹
        current_time = datetime.now()
        time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        new_folder_path = os.path.join(upload_loader, time_str)
        os.makedirs(new_folder_path, exist_ok=True)

        file_path = os.path.join(new_folder_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(content={"message": "Upload file success!"})
    except Exception as e:
        print(f"error : {e}")
        return JSONResponse(
            status_code=500, content={"message": "An error occured, upload_file"}
        )


if __name__ == "__main__":
    uvicorn.run(app="fastapi_test:app", host="0.0.0.0", port=8000, reload=True)
