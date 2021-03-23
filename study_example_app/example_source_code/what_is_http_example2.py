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

    # 브라우저에서 접속했습니다.
    print(f'{addr} 클라이언트에서 HTTP 패킷을 보냈습니다.')
    # 클라이언트가 보낸 패킷을 전부 받습니다(receive).
    data:bytes = client_socket.recv(1024)

    print('----')
    http_packets = data.decode('utf-8').split('\r\n')
    # 수신받은 문자열을 출력합니다.
    for packet in http_packets:
        print('패킷에 담겨진 데이터들입니다 : ', packet)


    # HTTP Response 패킷을 손으로 직접 만들어줍니다.
    response_byte_array = bytearray()

    # 1. Status Line : HTTP Response 패킷입니다. HTT Protocol(규칙)을 지키지 않으면 웹브라우저(Chrome, Safari, Internet Explorer) 는 내가 보낸 데이터 패킷을 이해하지 못합니다.
    response_byte_array += b'HTTP/1.1 200 OK\r\n'
    response_byte_array += b'Content-Type: application/json\r\n'
    response_byte_array += b'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) \r\n'
    response_byte_array += b'Accept: text/html,application/xhtml+xml,application/json;\r\n'
    response_byte_array += b'Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
    response_byte_array += b'Content-Length: 46\r\n\r\n'
    response_byte_array += '{\n"message":"안녕 나는 TCP/IP 서버야"\n}'.encode('utf-8')

    # 직접 만든 HTTP 패킷을 Client에게 응답값으로 전달해줍니다.
    client_socket.sendall(response_byte_array)
    client_socket.close()
