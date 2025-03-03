from os import getenv
import os
from sys import stderr
from typing import Any

import requests

from lib.config import app_config
from lib.data import APIRequest, Cookie


def dbg_print(str: str = ''):
    if not app_config.verbose:
        return
    if str != '':
        print(f"[DEBUG] {str}")
    else:
        print()


def dbg_print_api_call_req(req_data: APIRequest, cookie_data: list[Cookie]):
    dbg_print("Making API call with the following parameters")
    dbg_print(f"Method: {req_data.method}")
    dbg_print(f"Protocol: {req_data.protocol}")
    dbg_print(f"Host: {req_data.host}")
    dbg_print(f"Path: {req_data.path}")
    if req_data.headers:
        dbg_print("Headers:")
        for header in req_data.headers:
            dbg_print(f"  {header}: {req_data.headers[header]}")
    if req_data.queryParams:
        dbg_print("Query Parameters:")
        for param in req_data.queryParams:
            dbg_print(f"  {param}: {req_data.queryParams[param]}")
    if cookie_data:
        dbg_print("Cookies:")
        for cookie in cookie_data:
            dbg_print(f"  {cookie.name}: {cookie.value}")
    dbg_print()


def dbg_print_api_call_res(res_data: requests.Response):
    dbg_print("Successful API call")
    dbg_print(f"Status Code: {res_data.status_code}")
    if res_data.headers:
        dbg_print("Headers:")
        for header in res_data.headers:
            dbg_print(f"  {header}: {res_data.headers[header]}")
    if res_data.cookies:
        dbg_print("Returned cookies")
        for cookie in res_data.cookies:
            dbg_print(f"  {cookie.name}: {cookie.value}")
    dbg_print()


def replace_env(req_data: dict[str, Any]):
    if app_config.verbose:
        dbg_print("Replacing env vars")

    for key in req_data:
        if isinstance(req_data[key], dict):
            req_data[key] = search_and_replace_dict(req_data[key])
        elif isinstance(req_data[key], list):
            req_data[key] = search_and_replace_list(req_data[key])
        elif isinstance(req_data[key], str):
            req_data[key] = search_and_replace_str(req_data[key])

    if app_config.verbose:
        dbg_print()


def search_and_replace_list(collection: list) -> list:
    for idx, elm in enumerate(collection):
        if isinstance(elm, dict):
            collection[idx] = search_and_replace_dict(collection[idx])
        elif isinstance(elm, list):
            collection[idx] = search_and_replace_list(collection[idx])
        elif isinstance(elm, str):
            collection[idx] = search_and_replace_str(collection[idx])

    return collection


def search_and_replace_dict(collection: dict) -> dict:
    for key in collection:
        if isinstance(collection[key], dict):
            collection[key] = search_and_replace_dict(collection[key])
        elif isinstance(collection[key], list):
            collection[key] = search_and_replace_list(collection[key])
        elif isinstance(collection[key], str):
            collection[key] = search_and_replace_str(collection[key])

    return collection


def search_and_replace_str(string: str) -> str:
    start_construct = "${{"
    end_construct = "}}"

    start_idx = string.find(start_construct)
    if start_idx == -1:
        return string

    end_idx = string.find(end_construct)
    if end_idx == -1:
        raise Exception(
            "Env replacement construct ${{}} was malformed or incomplete")

    env_var_name = string[start_idx +
                          len(start_construct):end_idx].lstrip().rstrip()
    env_var_value = getenv(env_var_name)
    if env_var_value is None:
        raise Exception(f"Environment variable {
                        env_var_name} hasn't been provided")

    if app_config:
        dbg_print(f"{env_var_name} was replaced with {env_var_value}")

    string = string.replace(
        string[start_idx:end_idx+len(end_construct)], env_var_value)

    return search_and_replace_str(string)


def prepare_query_params(
    queryParams: dict[str, str | list[str]] | None
) -> dict[str, str | list[str]] | None:
    if queryParams is None:
        return None

    for field in queryParams:
        value = queryParams[field]
        if isinstance(value, list):
            queryParams[field] = ",".join(value)

    return queryParams


def prepare_cookie_data(cookie_data: list[Cookie]) -> dict[str, str]:
    cookie_jar = dict()
    for cookie in cookie_data:
        cookie_jar[cookie.name] = cookie.value
    return cookie_jar


def clear_files(req_filename: str, res_filename: str, cookies_filename: str):
    try:
        if os.path.exists(req_filename):
            os.remove(req_filename)
    except Exception as err:
        print(f"Couldn't clear the request file: {err}", file=stderr)
        exit(1)

    try:
        if os.path.exists(res_filename):
            os.remove(res_filename)
    except Exception as err:
        print(f"Couldn't clear the response file: {err}", file=stderr)
        exit(1)

    try:
        if os.path.exists(cookies_filename):
            os.remove(cookies_filename)
    except Exception as err:
        print(f"Couldn't clear the cookies file: {err}", file=stderr)
        exit(1)
