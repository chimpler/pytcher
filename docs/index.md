Pytcher is a REST micro-framework for Python 3 that relies on a routing tree
similar to [RODA](http://roda.jeremyevans.net/) in Ruby, [Akka HTTP](https://doc.akka.io/docs/akka-http/current/index.html) in Scala or [Javalin](https://javalin.io/) in Java.

!!! danger
    Under development

## Example of routing tree

```python
{!examples/simple_app.py!}
```

## Features

- Routing tree definition
- Marshalling / Unmarshalling of `data classes` (using types), `namedtuples`, `date`, `datetime`, `uuid`, ...   
- Additional Routing decorators similar to Flask
- Well scoped objects (no global variables)
- Support for WSGI
