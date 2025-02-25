from typing import Any, Literal
import requests
import json
from pydantic import BaseModel

class RequestData(BaseModel):
    Host: str
    Path: str = "/"
    Method: Literal['GET','POST','PUT','DELETE']
    Headers: dict[str, str] | None = None

def read_request_data(file) -> RequestData:
    raw_data = file.read()
    try:
        data = RequestData(**json.loads(raw_data))
        return data
    except Exception as err:
        print(f"Not valid request input data: {err}")
        exit(1)

def read_request_body(file) -> dict[str, Any] | None:
    data = json.loads(file.read())
    return data

def call_endpoint(base_url:str, path:str,
                  headers:dict[str,str],
                  method:Literal['GET','POST','PUT','DELETE'],
                  body:dict[str,Any]) -> requests.Response:
    return requests.request(
        method=method,
        url=f"{base_url}{path}",
        headers=headers,
        json=body
    )

def write_response_data(response: requests.Response, file):
    data = dict()
    data['Status_Code'] = response.status_code
    data['Is_Error'] = not response.ok
    data['Headers'] = dict(response.headers)
    file.write(json.dumps(data, indent=2))

def write_response_body(response: requests.Response, file):
    content_type = response.headers['Content-Type']
    if content_type is None or 'application/json' not in content_type:
        print("Not received a json body")
    else:
        file.write(json.dumps(response.json(), indent=2))

def show_process(request: RequestData, response: requests.Response):
    print(f"Host: {request.Host}")
    print(f"Path: {request.Path}")
    print(f"Method: {request.Method}")
    print(f"Status Code: {response.status_code}")
    print(f"Is Error: {not response.ok}")

def process_api_rest_request(request_name: str, response_name: str):
    request_data_file = open(f"{request_name}_request_data.json", "r")
    request_body_file = open(f"{request_name}_request_body.json","r")
    response_data_file = open(f"{response_name}_response_data.json", "w+")
    response_body_file = open(f"{response_name}_response_body.json", "w+")

    request_data = read_request_data(file=request_data_file)
    request_body = None
    if request_data.Method != 'GET':
        request_body = read_request_body(file=request_body_file)
    response = call_endpoint(
        base_url=request_data.Host,
        path=request_data.Path,
        method=request_data.Method,
        headers=request_data.Headers if request_data.Headers is not None else dict(),
        body=request_body if request_body is not None else dict()
    )
    show_process(request_data,response)
    write_response_data(response, file=response_data_file)
    write_response_body(response, file=response_body_file)
