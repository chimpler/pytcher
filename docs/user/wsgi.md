## Running pytcher using uWSGI

Install uWSGI:
    
    $ pip install uwsgi
    
To run it:

    $ uwsgi --http :8000 --wsgi-file examples/simple_app.py --pp examples  -H venv3/ --wsgi simple_app:app