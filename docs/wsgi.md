## Running pytcher using uWSGI

Pytcher can be run as a WSGI application. In this page, we will describe how to use [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

Install uWSGI:
    
    $ pip install uwsgi
    
If you use a virtualenv `venv3`, you can run the example `simple_app.py` as follows:

    $ uwsgi --http :8000 --wsgi-file examples/simple_app.py --pp examples  -H venv3/ --wsgi simple_app:app
    
## uWSGI configuration

Minimal configuration

```ini
[uwsgi]
module = simple_app
callable = app
master = true
processes = 5
socket = uwsgi.sock
```

## Docker deployment
