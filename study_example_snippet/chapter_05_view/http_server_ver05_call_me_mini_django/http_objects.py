from typing import Any
from typing import Dict
from typing import List


class HTTPRequest:
    http_method: str
    http_path: str
    http_version: str
    headers: Dict[str, str] = {}
    request_body: str = ""

    def __init__(self, http_request_packet: bytes):
        packet_list: List[str] = http_request_packet.decode("utf-8").split("\r\n")

        self.http_method, self.http_path, self.http_version = packet_list.pop(0).split(" ")
        request_body_start_idx = -1
        for i, packet in enumerate(packet_list):
            if not packet:
                request_body_start_idx = i
                break
            split_idx = packet.find(":")
            header_key, header_value = packet[0:split_idx], packet[split_idx + 1 :]
            self.headers[header_key] = header_value

        if request_body_start_idx != -1:
            self.request_body = packet_list[request_body_start_idx + 1]


class HTTPResponse:
    http_status: int
    http_message: str
    http_version: str
    headers: Dict[str, Any]
    response_body: str

    def __init__(self, response_body: str, headers={}, http_status=200, http_message="OK", http_version="HTTP/1.1"):
        self.http_version = http_version
        self.http_status = http_status
        self.http_message = http_message
        self.headers = headers
        self.response_body = response_body

        # Content-Length 헤더값은 정확하지 않으면 패킷이 누락될수있다. 그렇기 때문에 정확히 body크기를 계산해서 저장한다.
        self.headers["Content-Length"] = len(self.response_body.encode("utf-8"))
        # 서버의 출처 정보를 넣어주고 싶으면 User-Agent라는 헤더값에 원하는 정보를 명시해주면된다.
        self.headers["User-Agent"] = "Python no longer tcp Server"

    def serialize(self) -> bytes:
        response_line: bytes = f"{self.http_version} {self.http_status} {self.http_message}\r\n".encode("utf-8")
        response_header: bytes = "\r\n".join(f"{key}:{value}" for key, value in self.headers.items()).encode("utf-8")
        response_body: bytes = ("\r\n\r\n" + self.response_body).encode("utf-8")
        return response_line + response_header + response_body
