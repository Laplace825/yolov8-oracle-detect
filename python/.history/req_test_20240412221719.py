import requests
import socket


if __name__ == "__main__":
    sock = socket.socket()
    sock.bind(("127.0.0.1", 8080))
    sock.listen(5)
    # repos = requests.get("http://localhost:8000/people/1")
    # print(repos.json())

    while True:
        conn, addr = sock.accept()
        print(f"Got connection from {addr}")

        data = conn.recv(1024)
        print(f"Received {data.decode()}")

        conn.send(b"HTTP/1.1 200 OK\r\nserver:yuan\r\n\r\nThank you for connecting!")
        conn.close()
