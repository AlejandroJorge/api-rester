# CLI REST Client

Didn't like Postman / Insomnia / etc so I just made my own CLI tool for quickly testing my REST APIs

## Installation

Setup a virtual environment

```bash
python3 -m venv .venv
```

Get inside said virtual environment

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

## How to use

Make sure you're in the virtual environment (or your system has the necessary packages) and then run
```
python3 main.py
```

It will read the request data from `request_data.json`

```json
{
  "Host": "https://pokeapi.co",
  "Path": "/api/v2/pokemon/ditto",
  "Method": "GET"
}
```

And will also read request body from `request_body.json`

```json
{
    // your schema
}
```

Then the response metadata will be stored in `response_data.json`

```json
{
  "Status_Code": 200,
  "Is_Error": false,
  "Headers": {
    // response headers
  }
}
```

And the response body will be stored in `response_body.json`

```json
{
    // your schema
}
```
