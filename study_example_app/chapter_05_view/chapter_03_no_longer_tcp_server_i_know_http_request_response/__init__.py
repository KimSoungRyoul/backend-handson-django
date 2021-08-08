"""
 http를 모르는 원시적인(tcp)서버

 1. 서버를 실행합니다.  python chapter_00_tcp_server.py
 2. 웹브라우저(Chrome, Safari, Internet Explorer)에 들어가서  http://127.0.0.1:9999 로 접속합니다.
 3. 실행된 서버에 출력되는 로그를 확인합니다.
"""
import socket

from .http_objects import HTTPRequest
from .http_objects import HTTPResponse


# 서버 소캣을 열기위한 기본 작업입니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST, PORT = '127.0.0.1', 9999
server_socket.bind((HOST, PORT))
server_socket.listen()


def hello_function_view(http_request: HTTPRequest) -> HTTPResponse:
    http_request.http_method  # "GET"

    response_body: str = '{"message" : "안녕 나도 반가워 난 TCP/IP 서버야"}'

    return HTTPResponse(headers={'Content-Type': 'application/json'}, response_body=response_body)


def bye_function_view(http_request: HTTPRequest) -> HTTPResponse:
    response_body: str = '{"message" : "그래 잘가 나는 TCP/IP 서버야"}'
    return HTTPResponse(headers={'Content-Type': 'application/json'}, response_body=response_body)


def url_not_fount_view(http_request: HTTPRequest) -> HTTPResponse:
    response_body: str = '{"message": "서버가 알지 못하는 url입니다."}'

    return HTTPResponse(headers={'Content-Type': 'application/json'}, response_body=response_body)


# URL Dispatcher
url_patterns = {
    '/hello': hello_function_view,
    '/bye': bye_function_view,
}


print('서버가 실행되었습니다....\n')
# 서버가 계속 Client요청을 받기위해 무한루프
while True:
    # 클라이언트에서 요청이 들어오면 받을수 있게 서버 소캣을 열어두고 대기합니다.
    client_socket, addr = server_socket.accept()

    # 브라우저에서 접속했습니다.
    print(f'{addr} 클라이언트에서 HTTP 패킷을 보냈습니다.')
    # 클라이언트가 보낸 패킷을 전부 받습니다(receive).
    data: bytes = client_socket.recv(1024)

    http_request = HTTPRequest(http_request_packet=data)

    # http response 의 body 정보를 웹브라우저가 보내준 http_path 에 따라서 다르게 작성해줍니다
    try:
        view_function = url_patterns[http_request.http_path]
        print(f'서버에서 이러한 {http_request.http_path}을 알고있습니다 이에 맞는 응답을 전송하겠습니다.')
    except KeyError as e:
        print(f'서버에서 url_patterns에 이러한 {http_request.http_path}를 따로 정의해준적이 없기때문에 KeyError가 발생했습니다,')
        view_function = url_not_fount_view

    http_response = view_function(http_request=http_request)

    # 직접 만든 HTTP 패킷을 Client에게 응답값으로 전달해줍니다.
    client_socket.sendall(http_response.serialize())
    client_socket.close()
