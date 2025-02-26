import json
from sys import stderr

template = {
    "protocol": "http",
    "host": "localhost:3000",
    "path": "/",
    "method": "GET",
    "headers": {
        "Content-Type": "application/json"
    },
    "body": {
        "message": "Hello world"
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
