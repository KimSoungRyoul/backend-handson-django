"""
 http url 정도는 분기문으로 분석할수 아는 원시적인 웹서버

 1. 서버를 실행합니다.  python chapter_01_tcp_server.py
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


print('서버가 실행되었습니다.... 웹브라우저에서(크롬, 사파리...) http://127.0.0.1:9999로 접속하면 이 서버와 통신할 수 있습니다.')
print('이 서버는 url을 약간은 분석할수 있습니다. http://127.0.0.1:9999/hello  http://127.0.0.1:9999/bye 로 접속하면 새로운 응답값을 전달합니다.\n')


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
    for idx, packet in enumerate(http_packets):
        print( packet)
        if idx == 0:
            http_method, http_path, http_version = packet.split(' ')
            print('--------------------------------------------')
            print(f'웹브라우저에서 보내준 HTTP 메서드는 {http_method}')
            print(f'웹브라우저에서 보내준 HTTP 경로는 {http_path}')
            print(f'웹브라우저에서 보내준 HTTP 버전는 {http_version}')
            print('--------------------------------------------')

    # http response 의 body 정보를 웹브라우저가 보내준 http_path 에 따라서 다르게 작성해줍니다
    response_body: bytes = b''
    if http_path == '/hello':
        response_body = '{"message" : "안녕 나도 반가워 난 웹서버야"}'.encode('utf-8')
        response_body_length = len(response_body)
    elif http_path == '/bye':
        response_body = '{"message" : "그래 잘가 나는 웹서버야"}'.encode('utf-8')
        response_body_length = len(response_body)
    else:
        response_body = '{"message" : "나는 웹서버야"}'.encode('utf-8')
        response_body_length = len(response_body)

    # 1. Status Line : HTTP Response 패킷입니다. HTT Protocol(규칙)을 지키지 않으면 웹브라우저(Chrome, Safari, Internet Explorer)는 내가 보낸 데이터 패킷을 이해하지 못합니다.
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

http_request_packet = b"""GET / HTTP/1.1
Host: 127.0.0.1:9999
Connection: keep-alive
sec-ch-ua: "Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36
sec-ch-ua-platform: "macOS"
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: image
Referer: http://127.0.0.1:9999/
Accept-Encoding: gzip, deflate, br
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: optimizelyEndUserId=oeu1606381745582r0.2736837453626988; _ga=GA1.1.1500297967.1606381746; wcs_bt=s_51119d387dfa:1615440263; _tq_id.TV-364536-1.dc78=4d11bca09268fe90.1606381746.0.1623387356..; _ga_6KMY7BWK8X=GS1.1.1623387355.2.0.1623387356.59; csrftoken=g6WCkDbZxmZYYojZ1qRtWljWSJ0oidX6; _ga_T33T3CSETQ=GS1.1.1628660512.4.0.1628660512.0
"""
