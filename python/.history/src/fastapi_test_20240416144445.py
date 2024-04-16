'''
Author: laplace825
Date: 2024-04-12 15:45:16
LastEditors: laplace825
LastEditTime: 2024-04-16 14:44:36
FilePath: /python/src/fastapi_test.py
Description: 

Copyright (c) 2024 by laplace825, All Rights Reserved. 
'''

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import uvicorn
import os
import sys
from datetime import datetime
import infer

app = FastAPI()

# 当前工作区上一级文件夹
# .../python/src/
working_space = os.path.abspath(os.path.dirname(sys.argv[0]))
# 创建推理对象
model = infer.Inference(working_space)
# 用户上传文件的目录
# NOTE: 在该目录下按上传时间新建文件夹,将上传的文件保存到该文件夹
upload_loader = working_space + "/upload_img"


def is_image_file(file: UploadFile) -> bool:
    allow_image = ["jpg", "png", "jpeg"]
    return file.filename.split(".")[-1].lower() in allow_image


@app.get("/")
def index():
    return {"message": "FastAPI !"}


# 提交文件
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not is_image_file(file):
            return JSONResponse(
                status_code=400,
                content={"message": "Only support image file(jpg,png,jpeg)!"},
            )
        # 根据当前上传时间新建文件夹，并把文件保存到该文件夹
        current_time = datetime.now()
        time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        new_folder_path = os.path.join(upload_loader, time_str)
        os.makedirs(new_folder_path, exist_ok=True)

        file_path = os.path.join(new_folder_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 检测和分类结果保存路径
        model.use_pt_det(
            new_folder_path,
            new_folder_path + "/output_img_pt",
        )
        model.use_pt_cls(
            new_folder_path + "/output_img_pt/",
            new_folder_path + "/output_img_pt/0/cls",
        )

        return JSONResponse(content={"message": "Upload file success!"})
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": f"An error occured,{e}"}
        )


if __name__ == "__main__":
    uvicorn.run(app="fastapi_test:app", host="0.0.0.0", port=8000, reload=True)
