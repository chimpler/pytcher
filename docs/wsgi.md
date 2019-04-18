Pytcher can be run as a WSGI application. In this page, we will describe how to use [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

## Running pytcher using uWSGI

Install uWSGI:
    
    $ pip install uwsgi
    
If you use a virtualenv `venv3`, you can run the example `simple_app.py` as follows:

    $ uwsgi --http :8000 --wsgi-file examples/simple_app.py --pp examples  -H venv3/ --wsgi simple_app:app
    
### uWSGI configuration

Minimal configuration

```ini
[uwsgi]
module = simple_app
callable = app
master = true
processes = 5
socket = uwsgi.sock
```

## Running pytcher using Gunicorn

Install uWSGI:
    
    $ pip install uwsgi

To run it:

    $ gunicorn --pythonpath examples simple_app:app


## Running pytcher using Gevent

Install gevent:

    $ pip install gevent
    
Then write a simple Python script:
```python
from gevent.pywsgi import WSGIServer
from examples.simple_app import app

http_server = WSGIServer(('', 8000), app)
http_server.serve_forever()
```    

And execute it.

## Running pytcher using Twisted

Install Twisted:

    $ pip install twisted
    
To run it:
    
    $ twistd -n web --port tcp:8000 --wsgi examples.simple_app.app

## Docker deployment
