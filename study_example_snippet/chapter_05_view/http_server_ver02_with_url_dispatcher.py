"""
 http를 모르는 원시적인(tcp)서버

 1. 서버를 실행합니다.  python http_server_ver00.py
 2. 웹브라우저(Chrome, Safari, Internet Explorer)에 들어가서  http://127.0.0.1:9999 로 접속합니다.
 3. 실행된 서버에 출력되는 로그를 확인합니다.
"""
import socket
from typing import Callable
from typing import Dict
# HTTP Response 패킷을 직접 만들어줍니다.

default_http_response_packet = bytearray(
    b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nUser-Agent: Python tcp Server \r\nAccept: text/html,application/xhtml+xml,application/json;\r\nAccept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7\r\n',
)


# 서버 소캣을 열기위한 기본 작업입니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST, PORT = '127.0.0.1', 9999
server_socket.bind((HOST, PORT))
server_socket.listen()


def hello_function_view(http_request_packet):
    response_body: bytes = '{"message" : "안녕 나도 반가워 난 웹서버야"}'.encode('utf-8')
    response_body_length = len(response_body)
    http_response = (
        default_http_response_packet + f'Content-Length: {response_body_length}\r\n\r\n'.encode('utf-8') + response_body
    )
    return http_response


def bye_function_view(http_request_packet):
    response_body: bytes = '{"message" : "그래 잘가 나는 웹서버야"}'.encode('utf-8')
    response_body_length = len(response_body)
    http_response = (
        default_http_response_packet + f'Content-Length: {response_body_length}\r\n\r\n'.encode('utf-8') + response_body
    )
    return http_response


def url_not_fount_view(http_request_packet):
    response_body: bytes = '{"message" : "서버가 알지 못하는 url입니다."}'.encode('utf-8')
    response_body_length = len(response_body)
    http_response = (
        default_http_response_packet + f'Content-Length: {response_body_length}\r\n\r\n'.encode('utf-8') + response_body
    )
    return http_response


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
    http_request_packet: bytes = client_socket.recv(1024)
    print('----')
    http_method, http_path, http_version = http_request_packet.decode('utf-8').split('\r\n')[0].split(" ")

    # http response 의 body 정보를 웹브라우저가 보내준 http_path 에 따라서 다르게 작성해줍니다
    try:
        view_function = url_patterns[http_path]
        print(f'서버에서 이러한 {http_path}을 알고있습니다 이에 맞는 응답을 전송하겠습니다.')
    except KeyError as e:
        print(f'서버에서 url_patterns에 이러한 {http_path}를 따로 정의해준적이 없기때문에 KeyError가 발생했습니다,')
        view_function = url_not_fount_view

    http_response_packet = view_function(http_request_packet=http_request_packet)

    # 직접 만든 HTTP 패킷을 Client에게 응답값으로 전달해줍니다.
    client_socket.sendall(http_response_packet)
    client_socket.close()
