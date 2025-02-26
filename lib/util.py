from os import getenv
from typing import Any

from lib.config import app_config


def dbg_print(str: str = ''):
    if str != '':
        print(f"[DEBUG] {str}")
    else:
        print()


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
