## Default exception handlers
Exceptions can be intercepted and converted to a response with a status code.
By default, if `debug` is enabled (by default), the exception will be captured
and the server will response with error `500` with a detailed error description
containing the error, the url, the headers and the stack trace:
```json
{
  "error": "list index out of range",
  "url": "/items/444",
  "headers": {
    "wsgi.input": "<_io.BufferedReader name=7>",
    "wsgi.errors": "<_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>",
    "wsgi.version": "(1, 0)",
    "wsgi.run_once": "False",
    "wsgi.multithread": "True",
    "wsgi.multiprocess": "False",
    "wsgi.file_wrapper": "<class 'wsgiref.util.FileWrapper'>"
  },
  "stack_trace": [
    "Traceback (most recent call last):",
    "  File \"/Users/fdang/chimpler/pytcher/pytcher/app.py\", line 124, in _handle_request",
    "    None",
    "  File \"/Users/fdang/chimpler/pytcher/pytcher/app.py\", line 117, in <genexpr>",
    "    output",
    "  File \"/Users/fdang/chimpler/pytcher/pytcher/app.py\", line 120, in <genexpr>",
    "    for router in self._routers",
    "  File \"/Users/fdang/chimpler/pytcher/pytcher/__init__.py\", line 151, in run_router",
    "    return router.func(request, *matched_vars)",
    "  File \"examples/simple_app.py\", line 22, in route",
    "    return self._items[item_id]",
    "IndexError: list index out of range",
    ""
  ]
}
```

If debug is disabled (for example in production), a simple Internal error message will be returned:
```json
{
  "error": "Internal Error"
}
```

## Customize exception handlers

If one wants to intercept other exceptions and not use the default ones, one can create a function
or a method inside a class and use the decorator `handle_exception` with the exception to capture.

The following example captures the `ValueError` exceptions and return a response with the exception message.

```python
from pytcher import Request, handle_exception

@handle_exception(ValueError)
def handle_value_error(request: Request, exception: ValueError):
    return {
        "error": str(exception)
    }
```
    
And then pass it to the application `App`:
```python
from pytcher import App

app = App([router, handle_value_error])
app.run()
```

Note that it can also be defined in the same class that defines the route:
```python
from pytcher import App, Request, route, handle_exception

class MyRoute(object):
    @route(path='/items')
    def route(self, r: Request):
        return "Hello"
        
    @handle_exception(ValueError)
    def handle_value_error(self, request: Request, exception: ValueError):
        return {
            "error": str(exception)
        }

app = App(MyRoute())
app.run()
```


