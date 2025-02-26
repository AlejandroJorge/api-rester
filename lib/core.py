import json
import requests
from pydantic import ValidationError
from sys import stderr

from lib.data import APIRequest, APIResponse


def read_request_file(request_filename: str) -> APIRequest:
    try:
        req_file = open(request_filename, "r")
    except Exception as err:
        print(f"Couldn't open request file {
              request_filename}: {err}", file=stderr)
        exit(1)

    try:
        req_data = json.load(req_file)
    except Exception as err:
        print(f"Couldn't parse json in request file {
              request_filename}: {err}", file=stderr)
        exit(1)

    try:
        req_data = APIRequest(**req_data)
    except ValidationError as err:
        print(f"Request file doesn't comply with expected model: {err}")
        exit(1)

    return req_data


def make_api_call(req_data: APIRequest) -> APIResponse:
    url = f"{req_data.protocol}://{req_data.host}{req_data.path}"

    try:
        response = requests.request(
            method=req_data.method,
            url=url,
            headers=req_data.headers,
            json=req_data.body
        )
    except Exception as err:
        print(f"HTTP Request failed: {err}")
        exit(1)

    body = None
    try:
        body = response.json()
    except Exception:
        print("Server didn't respond with a valid json body")

    res_data = APIResponse(
        status_code=response.status_code,
        headers=dict(response.headers),
        body=body)

    return res_data


def write_response_file(response_filename: str, res_data: APIResponse):
    try:
        res_file = open(response_filename, "w+")
    except Exception as err:
        print(f"Couldn't open response file {
              response_filename}: {err}", file=stderr)
        exit(1)

    try:
        data = res_data.model_dump()
        json.dump(fp=res_file, obj=data, indent=2)
    except Exception as err:
        print(f"Couldn't serialize json in response file {
              response_filename}: {err}", file=stderr)
        exit(1)
