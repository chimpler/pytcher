Pytcher is a REST micro-framework for Python 3 that relies on a routing tree
similar to [RODA](http://roda.jeremyevans.net/) in Ruby, [Akka HTTP](https://doc.akka.io/docs/akka-http/current/index.html) in Scala or [Javalin](https://javalin.io/) in Java.

## Features
* Routing tree definition using `with` or `for` construction
* Marshalling of Python objects (data classes, namedtuples, date, datetime, uuid, ...) that supports custom encoders
* Unmarshalling of JSON to Python objects (data classes, namedtuples, date, datetime, uuid, ...) supporting `typing` (e.g., `Dict[str, MyDataClass]`) syntax and custom decoders. 
* Additional Routing decorators similar to Flask
* Well scoped objects (no global variables)
* Support for WSGI


## Example of routing tree

```python
{!examples/simple_app.py!}
```