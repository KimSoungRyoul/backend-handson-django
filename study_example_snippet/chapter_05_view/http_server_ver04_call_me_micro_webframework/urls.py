from .apps import bye_function_view
from .apps import hello_function_view

# URL Dispatcher


url_patterns = {
    "/hello": hello_function_view,
    "/bye": bye_function_view,
}
