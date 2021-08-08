"""
 http를 모르는 원시적인(tcp)서버

 1. 서버를 실행합니다.  python chapter_00_tcp_server.py
 2. 웹브라우저(Chrome, Safari, Internet Explorer)에 들어가서  http://127.0.0.1:9999 로 접속합니다.
 3. 실행된 서버에 출력되는 로그를 확인합니다.
"""
import socket


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
    http_packets = data.decode('utf-8').split('\r\n')
    # 수신받은 문자열을 출력합니다.
    for packet in http_packets:
        print('웹브라우저가 보내준 패킷에 담겨진 데이터들입니다 : ', packet)

    # 1. Status Line : HTTP Response 패킷입니다. HTT Protocol(규칙)을 지키지 않으면 웹브라우저(Chrome, Safari, Internet Explorer)는 내가 보낸 데이터 패킷을 이해하지 못합니다.
    response_body: bytes = '{"message" : "안녕 나는 TCP/IP 서버야"}'.encode('utf-8')  # 여기있는 값은 마음데로 수정해도됩니다.
    response_body_length = len(response_body)

    # HTTP Response 패킷을 직접 만들어줍니다.
    response_byte_array = bytearray()
    response_byte_array += b'HTTP/1.1 200 OK\r\n'
    response_byte_array += b'Content-Type: application/json\r\n'
    response_byte_array += b'User-Agent: Python tcp Server \r\n'
    response_byte_array += b'Accept: text/html,application/xhtml+xml,application/json;\r\n'
    response_byte_array += b'Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
    response_byte_array += f'Content-Length: {response_body_length}\r\n\r\n'.encode('utf-8')
    response_byte_array += response_body

    # 직접 만든 HTTP 패킷을 Client에게 응답값으로 전달해줍니다.
    client_socket.sendall(response_byte_array)
    client_socket.close()
