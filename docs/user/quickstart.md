# Quickstart

First, make sure that you have Pytcher installed and up to date:

    $ pip install pytcher --upgrade
    
## Create a simple web service
```python
class MyRoute(object):
   @route
   def route(self, r): 
       blabla
     
route = MyRoute()
App(route).start()
```

## Create a simple web service using for construct

