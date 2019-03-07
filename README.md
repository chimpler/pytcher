### Pytcher

STILL A WORK IN PROGRESS

Pytcher is an HTTP routing DSL for Python. The main focus of Pytcher is to provide a human readable router syntax
while powerful enough to express complex query matching.

```python
def route_handler(r: Request):

    with r / 'books' / Regex('c.*r') as [book_id]:
        with r.get | r.put:
            return {'book': {'id': book_id}}

        with r.post:
            return {'books': [{'id': 2}]}

    with (r.get / 'novels' / int / 'authors' / int) & (r.p('g') == '3') as [novel_id, author_id]:
        print(r.p('g').list)
        return {'novel': novel_id, 'author': author_id}

```

# Compatiblity

Python      | Compatible
------------|:------:
cpython 3   | :white_check_mark:
pypy 3      | :white_check_mark:

## TODO

Items                                     | Status
------------------------------------------| :-----:
Support AND (&)                           | :white_check_mark:
Support OR (|)                            | :white_check_mark:
Support /                                 | :white_check_mark:
Support //                                | :x:
Support GET                               | :white_check_mark:
Support PUT                               | :white_check_mark:
Support POST                              | :white_check_mark:
Support PATCH                             | :white_check_mark:
Support parameter                         | :white_check_mark:
Support header                            | :white_check_mark:
Automatically generate route path for doc | :x:

