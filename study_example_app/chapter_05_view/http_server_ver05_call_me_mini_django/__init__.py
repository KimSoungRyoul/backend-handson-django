"""
  call me http server

"""
import socket

from .http_objects import HTTPRequest
from .urls import url_patterns
from .views import url_not_fount_view




# 서버 소캣을 열기위한 기본 작업입니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST, PORT = '127.0.0.1', 9999
server_socket.bind((HOST, PORT))
server_socket.listen()


print('서버가 실행되었습니다....\n')
while True:
    # 클라이언트에서 요청이 들어오면 받을수 있게 서버 소캣을 열어두고 대기합니다.
    client_socket, addr = server_socket.accept()

    print('\n------------------------------')
    # 브라우저에서 접속했습니다.
    print(f'{addr} 클라이언트에서 HTTP 패킷을 보냈습니다.')
    # 클라이언트가 보낸 패킷을 전부 받습니다(receive).
    data: bytes = client_socket.recv(1024)

    # tcp 소켓으로 받은 패킷을 http 패킷이라고 가정하고 분석해서 객체에 저장합니다.
    http_request = HTTPRequest(http_request_packet=data)

    # http response 의 body 정보를 웹브라우저가 보내준 http_path 에 따라서 다르게 작성해줍니다
    try:
        view_function = url_patterns[http_request.http_path]
        print(f'우리 서버의 url_patterns은 {http_request.http_path}을 알고있습니다 이에 맞는 응답을 전송하겠습니다.')
    except KeyError as e:
        print(f'우리 서버의 url_patterns은 {http_request.http_path}를 따로 정의해준적이 없기 때문에 KeyError가 발생했습니다,')
        view_function = url_not_fount_view

    http_response = view_function(request=http_request)
    print('------------------------------')

    # 직접 만든 HTTP 패킷을 Client에게 응답값으로 전달해줍니다.
    client_socket.sendall(http_response.serialize())
    client_socket.close()
