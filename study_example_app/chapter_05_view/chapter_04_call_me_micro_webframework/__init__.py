"""
  call me http server

"""
import socket

from .apps import url_not_fount_view
from .urls import url_patterns


# 서버 소캣을 열기위한 기본 작업입니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST, PORT = '127.0.0.1', 9999
server_socket.bind((HOST, PORT))
server_socket.listen()


print('서버가 실행되었습니다....\n')
# 서버가 계속 Client요청을 받기위해 무한루프

while True:
    # 클라이언트에서 요청이 들어오면 받을수 있게 서버 소캣을 열어두고 대기합니다.
    client_socket, addr = server_socket.accept()

    # 브라우저에서 접속했습니다.
    print(f'{addr} 클라이언트에서 HTTP 패킷을 보냈습니다.')
    # 클라이언트가 보낸 패킷을 전부 받습니다(receive).
    data: bytes = client_socket.recv(1024)

    print('----')
    http_request_packets = data.decode('utf-8').split('\r\n')

    for idx, packet in enumerate(http_request_packets):
        if idx == 0:
            http_method, http_path, http_version = packet.split(' ')

    # http response 의 body 정보를 웹브라우저가 보내준 http_path 에 따라서 다르게 작성해줍니다
    try:
        view_function = url_patterns[http_path]
        print(f'서버에서 이러한 {http_path}을 알고있습니다 이에 맞는 응답을 전송하겠습니다.')
    except KeyError as e:
        print(f'서버에서 url_patterns에 이러한 {http_path}를 따로 정의해준적이 없기때문에 KeyError가 발생했습니다,')
        view_function = url_not_fount_view

    http_response = view_function(http_request_packet=http_request_packets)

    # view_function에서 만들어준  HTTP 패킷을 Client에게 응답값으로 전달해줍니다.
    client_socket.sendall(http_response)
    client_socket.close()
