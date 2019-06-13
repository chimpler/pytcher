# Build api
#pydocmd simple pytcher.App++ | bin/reformat_code.sh > docs/api/app.md
#pydocmd simple pytcher.Request+ pytcher.request.ParameterDict+ | bin/reformat_code.sh > docs/api/request.md
#pydocmd simple pytcher+ | bin/reformat_code.sh > docs/api/pytcher.md
#pydocmd simple pytcher.Integer++ pytcher.Float++ pytcher.Regex++ pytcher.Choice++ | bin/reformat_code.sh > docs/api/matchers.md

mkdocs serve
