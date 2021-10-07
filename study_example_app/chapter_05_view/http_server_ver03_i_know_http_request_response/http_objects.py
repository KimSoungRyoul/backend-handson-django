from collections import deque
from typing import Any
from typing import Dict


class HTTPRequest:
    http_method: str
    http_path: str
    http_version: str
    headers: Dict[str, Any] = {}
    request_body: str = ""

    def __init__(self, http_request_packet: bytes):
        # http 패킷은 /r/n 을 구분자로 사용합니다. 각 패킷들을 분리해줍니다.
        packet_deq: deque[str] = deque(http_request_packet.decode("utf-8").split("\r\n"))

        # http 패킷의 첫줄은 항상 Method, path, version 정보를 담고있습니다.
        self.http_method, self.http_path, self.http_version = packet_deq.popleft().split(" ")

        # 두번째줄부터 빈값이 들어간 패킷이전까지는 header에 해당하는 정보들입니다.
        while packet := packet_deq.popleft():
            if not packet:
                break
            header_key, header_value = packet.split(": ")
            self.headers[header_key] = header_value

        # 헤더 정보를 전부 담고도 패킷이 더 존재한다면 그건 HTTP BODY에 해당하는 정보들입니다.
        if packet_deq:
            self.request_body = packet_deq.popleft()


class HTTPResponse:
    http_status: int
    http_message: str
    http_version: str
    headers: Dict[str, Any]
    response_body: str

    def __init__(
            self, response_body: str, headers={}, http_status=200, http_message="OK", http_version="HTTP/1.1",
    ):
        self.http_version = http_version
        self.http_status = http_status
        self.http_message = http_message
        self.headers = headers
        self.response_body = response_body

        # Content-Length 헤더값이 정확하지 않으면 패킷이 누락될수있다. 그렇기 때문에 정확히 body크기를 계산해서 저장한다.
        self.headers["Content-Length"] = len(self.response_body.encode("utf-8"))
        # 서버의 출처 정보를 넣어주고 싶으면 User-Agent라는 헤더값에 원하는 정보를 명시해주면된다.
        # 실제로 사용되고있는 User-Agent 헤더값 예시
        # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        # "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko)"
        self.headers["User-Agent"] = "Python no longer tcp Server"

    def serialize(self) -> bytes:
        response_line: bytes = f"{self.http_version} {self.http_status} {self.http_message}\r\n".encode("utf-8")
        response_header: bytes = "\r\n".join(f"{key}:{value}" for key, value in self.headers.items()).encode("utf-8")
        response_body: bytes = ("\r\n\r\n" + self.response_body).encode("utf-8")
        return response_line + response_header + response_body
