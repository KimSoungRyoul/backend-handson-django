from .http_objects import HTTPRequest
from .http_objects import HTTPResponse


def hello_function_view(request: HTTPRequest) -> HTTPResponse:
    print("웹브라우저가 보내준 패킷의 httpMethod:", request.http_method)
    print("웹브라우저가 보내준 패킷의 httpPath:", request.http_path)
    print("웹브라우저가 보내준 패킷의 httpBody:", request.request_body)

    response_body: str = '{"message" : "안녕 난 더이상 TCP/IP 서버가 아니야 HTTP 서버로 다시 태어났지"}'

    return HTTPResponse(headers={"Content-Type": "application/json"}, response_body=response_body)


def bye_function_view(request: HTTPRequest) -> HTTPResponse:
    print("웹브라우저가 보내준 패킷의 httpMethod:", request.http_method)
    print("웹브라우저가 보내준 패킷의 httpPath:", request.http_path)
    print("웹브라우저가 보내준 패킷의 httpBody:", request.request_body)

    response_body: str = '{"message" : "그래 잘가 난 더이상 TCP/IP 서버가 아니야 HTTP 서버로 다시 태어났지"}'

    return HTTPResponse(headers={"Content-Type": "application/json"}, response_body=response_body)


def url_not_fount_view(request: HTTPRequest) -> HTTPResponse:
    print("웹브라우저가 보내준 패킷의 httpMethod:", request.http_method)
    print("웹브라우저가 보내준 패킷의 httpPath:", request.http_path)
    print("웹브라우저가 보내준 패킷의 httpBody:", request.request_body)

    response_body: str = '{"message": "서버가 알지 못하는 url입니다."}'

    return HTTPResponse(headers={"Content-Type": "application/json"}, response_body=response_body)
