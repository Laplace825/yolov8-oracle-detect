FROM python:3.11

WORKDIR /app

#COPY . .

RUN echo > /etc/apt/sources.list && \
    echo  "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware" >/etc/apt/sources.list && \
    echo  "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware" >>/etc/apt/sources.list && \
    echo  "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware" >>/etc/apt/sources.list && \
    echo  "deb https://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware" >>/etc/apt/sources.list && \
    apt update

RUN apt install -y libgl1-mesa-glx

RUN pip install fastapi uvicorn opencv-python ultralytics tqdm python-multipart -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["python3", "/app/python/src/api.py"]