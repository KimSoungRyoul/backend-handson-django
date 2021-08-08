from typing import Callable
from typing import Dict

from .http_objects import HTTPRequest
from .http_objects import HTTPResponse
from .views import bye_function_view
from .views import hello_function_view

# URL Dispatcher
url_patterns: Dict[str, Callable[[HTTPRequest], HTTPResponse]] = {
    '/hello': hello_function_view,
    '/bye': bye_function_view,
}
