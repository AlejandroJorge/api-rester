import re
from typing import Any, Literal
from pydantic import BaseModel, field_validator


SupportedHTTPMethod = Literal['GET', 'HEAD', 'PUT', 'PATCH', 'POST', 'DELETE']


class APIRequest(BaseModel):
    protocol: Literal['http', 'https'] = 'http'
    host: str
    path: str
    method: SupportedHTTPMethod
    headers: dict[str, str] | None = None
    queryParams: dict[str, str | list[str]] | None = None
    # TODO maybe properly validate
    body: dict[str, Any] | list[Any] | None = None

    @field_validator("queryParams")
    def validate_queryParams(
            cls,
            value: dict[str, str | list[str]] | None) -> dict[str, str | list[str]] | None:
        if value is None:
            return None

        queryParams = value
        for field in queryParams:
            if not re.match(r'^[\w-]+$', field):
                raise ValueError(
                    "Query params names should be alphanumeric and only include _ or - as special char"
                )
            val = queryParams[field]
            if isinstance(val, str) and not re.match(r'^[\w-]+$', field):
                raise ValueError(
                    "Query params values should be alphanumeric and only include _ or - as special char"
                )
            if isinstance(val, list) and any([not re.match(r'^[\w-]+$', elm) for elm in val]):
                raise ValueError(
                    "Query params values inside a list should be alphanumeric and only include _ or - as special char"
                )

        return value

    @field_validator("host")
    def validate_host(cls, value: str) -> str:
        host_pattern = r"""
        ^(((?:([a-z0-9-]+|\*)\.)?([a-z0-9-]{1,61})\.([a-z0-9]{2,7}))|(localhost))(:[0-9]{1,4})?$
        """
        host_pattern = r"""
        (?i)^((?:([a-z0-9-]+|\*)\.)?([a-z0-9-]{1,61})(\.[a-z0-9-]{1,61})*\.([a-z0-9]{2,7})|localhost|([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}))(:[0-9]{1,4})?$
        """
        if not re.match(host_pattern, value, re.X):
            raise ValueError(
                "Invalid host, must be a valid domain name or IP address")
        if len(value) > 253:
            raise ValueError("Host exceeds maximum length of 253 characters")
        return value

    @field_validator("path")
    def validate_path(cls, value: str) -> str:
        path_pattern = r"^\/$|^\/(?!.*\/\/)[a-zA-Z0-9_\-/]+$"
        if not re.match(path_pattern, value, re.X):
            raise ValueError(
                "Invalid path"
            )
        return value

    @field_validator("headers")
    def validate_headers(
            cls, value: dict[str, str] | None
    ) -> dict[str, str] | None:
        if value is None:
            return None

        forbidden_headers = {"host", "content-length", "connection"}
        header_pattern = re.compile(r"^[A-Za-z0-9-]+$")

        for header in value:
            if not header_pattern.match(header):
                raise ValueError(f"Invalid header name: {header}")

            if header.lower() in forbidden_headers:
                raise ValueError(f"Cannot override header: {header}")

            if '\n' in value[header] or '\r' in value[header]:
                raise ValueError(
                    f"Invalid characters in header value: {header}")

        return value


class APIResponse(BaseModel):
    status_code: int
    headers: dict[str, str] | None = None
    body: dict[str, Any] | list[Any] | None = None


class Cookie(BaseModel):
    name: str
    value: str
    domain: str
    path: str = "/"

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        cookie_name_pattern = r'^[!#$%&\'*+\-.0-9A-Z^_`a-z|~]+$'
        if not re.match(cookie_name_pattern, value):
            raise ValueError(
                "Cookie name can only contain US-ASCII characters except control "
                "characters and separators (space, tab, and ()[]<>@,;:\\\"/=?{})"
            )
        return value

    @field_validator("value")
    def validate_value(cls, value: str) -> str:
        cookie_value_pattern = r'^[\x20-\x21\x23-\x2B\x2D-\x3A\x3C-\x5B\x5D-\x7E]+$'
        if not re.match(cookie_value_pattern, value):
            raise ValueError(
                "Cookie value can only contain US-ASCII characters excluding control "
                "characters, whitespace, double quotes, comma, semicolon and backslash"
            )
        return value

    @field_validator("domain")
    def validate_domain(cls, value: str) -> str:
        value = value.lstrip('.')
        domain_pattern = r'^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
        if not re.match(domain_pattern, value):
            raise ValueError(
                "Domain must be a valid hostname containing only alphanumeric "
                "characters, hyphens, and dots"
            )
        return value

    @field_validator("path")
    def validate_path(cls, value: str) -> str:
        path_pattern = r"^\/$|^\/(?!.*\/\/)[a-zA-Z0-9_\-/]+$"
        if not re.match(path_pattern, value, re.X):
            raise ValueError(
                "Invalid path"
            )
        return value
