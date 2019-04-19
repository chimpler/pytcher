Pytcher can be run as a WSGI application. 
In this page, we will describe how to use various WSGI implementations to run with pytcher.

## Running pytcher using uWSGI

Install [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/):
    
    $ pip install uwsgi
    
If you use a virtualenv `venv3`, you can run the example `simple_app.py` as follows:

    $ uwsgi --http :8000 --wsgi-file examples/simple_app.py --pp examples  -H venv3/ --wsgi simple_app:app
    
## Running pytcher using Gunicorn

Install [Gunicorn](https://gunicorn.org/):
    
    $ pip install uwsgi

To run it:

    $ gunicorn --pythonpath examples simple_app:app


## Running pytcher using Gevent

Install [gevent](http://www.gevent.org/):

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

Install [Twisted](https://twistedmatrix.com/trac/):

    $ pip install twisted
    
To run it:
    
    $ twistd -n web --port tcp:8000 --wsgi examples.simple_app.app

