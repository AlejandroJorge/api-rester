import json
import requests
from pydantic import ValidationError
from sys import stderr

from lib.data import APIRequest, APIResponse
from lib.util import dbg_print_api_call_res, dbg_print_api_call_req
from lib.util import replace_env, dbg_print, prepare_query_params

from lib.data import Cookie

from lib.util import prepare_cookie_data


def read_request_file(request_filename: str) -> APIRequest:
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

    dbg_print(f"Successfully read request from file: {request_filename}")
    dbg_print()

    return req_data


def make_api_call(req_data: APIRequest,
                  cookie_data: list[Cookie]
                  ) -> tuple[APIResponse, list[Cookie]]:
    dbg_print_api_call_req(req_data, cookie_data)

    try:
        req_data.queryParams = prepare_query_params(req_data.queryParams)
        url = f"{req_data.protocol}://{req_data.host}{req_data.path}"
        response = requests.request(
            method=req_data.method,
            url=url,
            headers=req_data.headers,
            json=req_data.body,
            params=req_data.queryParams,
            cookies=prepare_cookie_data(cookie_data)
        )
        dbg_print(f"Final URL: {response.request.url}")
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

    dbg_print_api_call_res(response)

    cookies_returned = []
    for cookie in response.cookies:
        if cookie.value is None:
            continue
        cookies_returned.append(
            Cookie(
                name=cookie.name,
                value=cookie.value,
                domain=cookie.domain,
                path=cookie.path
            )
        )

    return res_data, cookies_returned


def write_response_file(response_filename: str, res_data: APIResponse):
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

    dbg_print(f"Sucessfully written response to file: {response_filename}")
    dbg_print()


def read_cookies_file(cookies_filename: str) -> list[Cookie]:
    dbg_print(f"Reading cookies from file: {cookies_filename}")
    dbg_print()

    try:
        cookies_file = open(cookies_filename, "r")
    except Exception as err:
        if isinstance(err, FileNotFoundError):
            dbg_print("Couldn't find file for cookies, omitting it")
            dbg_print()
            return []
        print(f"Couldn't open cookies file {
              cookies_filename}: {err}", file=stderr)
        exit(1)

    try:
        data = json.load(fp=cookies_file)
    except Exception as err:
        print(f"Couldn't parse cookies from {
              cookies_file}: {err}", file=stderr)
        exit(1)

    if isinstance(data, dict):
        cookies = [Cookie(**data)]
    elif isinstance(data, list):
        cookies = [Cookie(**elm) for elm in data]
    else:
        return []

    return cookies


def write_cookies_file(cookies_filename: str, cookies: list[Cookie]):
    if len(cookies) == 0:
        dbg_print("No cookies to write, omitting")
        dbg_print()
        return

    dbg_print(f"Writing cookies to file: {cookies_filename}")
    dbg_print()

    try:
        cookies_file = open(cookies_filename, "w+")
    except Exception as err:
        print(f"Couldn't open cookies file {
              cookies_filename}: {err}", file=stderr)
        exit(1)

    try:
        data = [cookie.model_dump() for cookie in cookies]
        json.dump(fp=cookies_file, obj=data, indent=2)
    except Exception as err:
        print(f"Couldn't serialize json in cookies file {
              cookies_file}: {err}", file=stderr)
        exit(1)

    dbg_print(f"Sucessfully written cookies to file: {cookies_file}")
    dbg_print()
