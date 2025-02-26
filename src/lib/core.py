import json
import requests
from pydantic import ValidationError
from sys import stderr

from lib.data import APIRequest, APIResponse
from lib.util import replace_env, dbg_print
from lib.config import app_config


def read_request_file(request_filename: str) -> APIRequest:
    if app_config.verbose:
        dbg_print(f"Reading request from file: {request_filename}")
        dbg_print()

    try:
        req_file = open(request_filename, "r")
    except Exception as err:
        print(f"Couldn't open request file {
              request_filename}: {err}", file=stderr)
        exit(1)

    try:
        req_data = json.load(req_file)
        replace_env(req_data)
    except Exception as err:
        print(f"Couldn't parse json in request file {
              request_filename}: {err}", file=stderr)
        exit(1)

    try:
        req_data = APIRequest(**req_data)
    except ValidationError as err:
        print(f"Request file doesn't comply with expected model: {err}")
        exit(1)

    if app_config.verbose:
        dbg_print(f"Successfully read request from file: {request_filename}")
        dbg_print()

    return req_data


def make_api_call(req_data: APIRequest) -> APIResponse:
    url = f"{req_data.protocol}://{req_data.host}{req_data.path}"
    if app_config.verbose:
        dbg_print("Making API call")
        dbg_print(f"Method: {req_data.method}")
        dbg_print(f"URL: {url}")
        if req_data.headers:
            dbg_print("Headers:")
            for header in req_data.headers:
                dbg_print(f"  {header}: {req_data.headers[header]}")
        dbg_print()

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

    if app_config.verbose:
        dbg_print("Successful API call")
        dbg_print(f"Status Code: {res_data.status_code}")
        if res_data.headers:
            dbg_print("Headers:")
            for header in res_data.headers:
                dbg_print(f"  {header}: {res_data.headers[header]}")
        dbg_print()

    return res_data


def write_response_file(response_filename: str, res_data: APIResponse):
    if app_config.verbose:
        dbg_print(f"Writing response to file: {response_filename}")
        dbg_print()

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

    if app_config.verbose:
        dbg_print(f"Sucessfully written response to file: {response_filename}")
        dbg_print()
