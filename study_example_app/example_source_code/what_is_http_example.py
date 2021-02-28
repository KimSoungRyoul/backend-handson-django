# 접속할 서버 주소입니다. 여기에서는 루프백(loopback) 인터페이스 주소 즉 localhost를 사용합니다.
import socket

HOST = "127.0.0.1"

# 클라이언트 접속을 대기하는 포트 번호입니다.
PORT = 9999


# 소켓 객체를 생성합니다.
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 포트 사용중이라 연결할 수 없다는
# WinError 10048 에러 해결를 위해 필요합니다.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
# HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
# 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
# PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.
server_socket.bind((HOST, PORT))

# 서버가 클라이언트의 접속을 허용하도록 합니다.
server_socket.listen()


# 무한루프를 돌면서
while True:
    # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다.
    client_socket, addr = server_socket.accept()

    # 접속한 클라이언트의 주소입니다.
    print("Connected by", addr)
    # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다.
    data = client_socket.recv(1024)

    # 빈 문자열을 수신하면 루프를 중지합니다.
    if not data:
        break

    print("----")
    # 수신받은 문자열을 출력합니다.
    print("Received from", addr, data)
    # 받은 문자열을 다시 클라이언트로 전송해줍니다.(에코)
    client_socket.sendall(
        b'POST /sdfd HTTP/1.1\r\nContent-Type: application/json\r\nUser-Agent: PostmanRuntime/7.26.8\r\nAccept: */*\r\nPostman-Token: da3b562c-d93f-477b-9e69-cc48a2ed1406\r\nHost: 127.0.0.1:9999\r\nAccept-Encoding: gzip, deflate, br\r\nContent-Length: 21\r\n\r\n{\n    "abc":"aaaaa"\n}'
    )
    client_socket.close()
