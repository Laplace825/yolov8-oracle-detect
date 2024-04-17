FROM python:3.11

WORKDIR /app

#COPY . .

RUN apt update && apt install -y libgl1-mesa-glx

RUN pip install fastapi uvicorn opencv-python ultralytics tqdm python-multipart

ENTRYPOINT ["python3", "/app/python/src/api.py"]