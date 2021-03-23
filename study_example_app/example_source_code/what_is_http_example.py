import socket

# 서버 소캣을 열기위한 기본 작업입니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST, PORT = '127.0.0.1', 9999
server_socket.bind((HOST, PORT))
server_socket.listen()


# 서버가 계속 Client요청을 받기위해 무한루프
while True:
    # 클라이언트에서 요청이 들어오면 받을수 있게 서버 소캣을 열어두고 대기합니다.
    client_socket, addr = server_socket.accept()

    # 클라이언트가 보낸 패킷을 전부 받습니다(receive).
    data = client_socket.recv(1024)
    print('\n-------------------------------------------')
    print(f'{addr[0]} 클라이언트에서 HTTP 패킷을 보냈습니다.')

    # 수신받은 문자열을 출력합니다.
    print('패킷에 담겨진 데이터들입니다 : ', data)
    print('-------------------------------------------\n')
    # 직접 만든 HTTP 패킷을 Client에게 응답값으로 전달해줍니다.
    client_socket.sendall(b'...')
    client_socket.close()
