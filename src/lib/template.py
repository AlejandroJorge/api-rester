import json
from sys import stderr

template = {
    "protocol": "http",
    "host": "localhost:3000",
    "path": "/api/v1/data",
    "method": "POST",
    "headers": {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer ${{API_KEY}}",
    },
    "body": {
        "message": "Hello world"
    },
    "query": {
        "page": "1",
        "limit": "10"
    }
}


def write_template(filename: str):
    try:
        file = open(filename, "w+")
    except Exception as err:
        print(f"Couldn't open request file {
              filename}: {err}", file=stderr)
        exit(1)

    try:
        json.dump(fp=file, obj=template, indent=2)
    except Exception as err:
        print(f"Couldn't serialize json in response file {
              filename}: {err}", file=stderr)
        exit(1)
