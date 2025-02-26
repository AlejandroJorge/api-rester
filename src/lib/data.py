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
    # TODO maybe properly validate
    body: dict[str, Any] | list[Any] | None = None

    @field_validator("host")
    def validate_host(cls, value: str) -> str:
        host_pattern = r"""
        ^(((?:([a-z0-9-]+|\*)\.)?([a-z0-9-]{1,61})\.([a-z0-9]{2,7}))|(localhost))(:[0-9]{1,4})?$
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
