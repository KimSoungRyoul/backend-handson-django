import micro_webframework

# HTTP Response 패킷을 직접 만들어줍니다.
default_http_response_packet = bytearray(
    b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nUser-Agent: Python tcp Server \r\nAccept: text/html,application/xhtml+xml,application/json;\r\nAccept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7\r\n',
)

app = micro_webframework


@app.router('/hello', http_method='GET')
def hello_function_view(http_request_packet):
    response_body: bytes = '{"message" : "안녕 나도 반가워 난 TCP/IP 서버야"}'.encode('utf-8')
    response_body_length = len(response_body)
    http_response = (
        default_http_response_packet + f'Content-Length: {response_body_length}\r\n\r\n'.encode('utf-8') + response_body
    )
    return http_response


@app.router('/bye', http_method='GET')
def bye_function_view(http_request_packet):
    response_body: bytes = '{"message" : "그래 잘가 나는 TCP/IP 서버야"}'.encode('utf-8')
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
