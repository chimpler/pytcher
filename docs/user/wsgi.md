## Running pytcher using uWSGI

Pytcher can be run as a WSGI application. In this page, we will describe how to use [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

Install uWSGI:
    
    $ pip install uwsgi
    
To run it:

    $ uwsgi --http :8000 --wsgi-file examples/simple_app.py --pp examples  -H venv3/ --wsgi simple_app:app