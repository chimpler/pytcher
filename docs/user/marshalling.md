Marshalling converts Python data (int, str, float, list, dict, data classes, named tuples) into a format that can be send across the wire.
The user can request a particular format to be returned using the `Accept` request HTTP header:
* `application/json`: accept JSON output
* `application/xml`: accept XML output
* `text/csv`: accept CSV output
* `*/*`: accept anything