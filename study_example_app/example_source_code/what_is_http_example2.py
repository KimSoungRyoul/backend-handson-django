import socket

HOST = "127.0.0.1"

# 클라이언트 접속을 대기하는 포트 번호입니다.
PORT = 8006

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(
        b'POST /api/a-model/ HTTP/1.1\r\nContent-Type: application/json\r\nUser-Agent: PostmanRuntime/7.26.8\r\nAccept: */*\r\nPostman-Token: ad20f52c-50d3-4210-9b66-ab451f30db03\r\nHost: 127.0.0.1:9999\r\nAccept-Encoding: gzip, deflate, br\r\nContent-Length: 21\r\n\r\n{\n    \"a_field\":\"aaaaa\" \n}'
    )
    resp = b""
    while temp :=s.recv(2048):

        resp = resp + temp
    print(resp.decode())
