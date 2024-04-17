"""
Author: laplace825
Date: 2024-04-12 15:45:16
LastEditors: laplace825
LastEditTime: 2024-04-16 14:52:38
FilePath: /python/src/fastapi_test.py
Description: 

Copyright (c) 2024 by laplace825, All Rights Reserved. 
"""

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
@app.post("/upload_tapian/")
async def upload_file_tapian(file: UploadFile = File(...)):
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
            new_folder_path + "/output_img_pt/0/",
            new_folder_path + "/output_img_pt/0/cls",
        )

        # 读取目录下的所有分类结果

        cls_result = dict()
        for file in os.listdir(new_folder_path + "/output_img_pt/0/cls"):
            if file.endswith(".txt"):
                with open(
                    os.path.join(new_folder_path + "/output_img_pt/0/cls", file), "r"
                ) as f:
                    # 将单一文件中的所有结果分成二级字典
                    for line in f.readlines():
                        score, cls_name = line.strip().split(" ")
                        cls_result[file.filename] = dict(
                            {f"{cls_name}": float(score)}
                        )

        print(cls_result)

        return JSONResponse(content={"message": "Upload file success!"})
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": f"An error occured,{e}"}
        )


@app.post("/upload_hwrite/")
async def upload_file_hwrite(file: UploadFile = File(...)):
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

        model.use_pt_cls(
            new_folder_path,
            new_folder_path + "/cls",
        )

        return JSONResponse(content={"message": "Upload file success!"})
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": f"An error occured,{e}"}
        )


if __name__ == "__main__":
    uvicorn.run(app="api:app", host="0.0.0.0", port=8000, reload=True)
