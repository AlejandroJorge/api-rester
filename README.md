# CLI REST Client

A lightweight command-line REST client for testing APIs without the overhead of GUI applications like Postman or Insomnia.

## Features

- Simple JSON-based request configuration
- Support for GET, POST, PUT, and DELETE methods
- Custom headers support
- Automatic response parsing and formatting
- Separate files for request/response data and bodies

## Installation

1. Clone the repository
```bash
git clone https://github.com/AlejandroJorge/cli-rest-client.git
cd cli-rest-client
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

## Usage

### Basic Usage

Run the client by providing a request name:

```bash
python rest_client.py <request_name>
```

### Request Files

The client expects two files:

1. `{request_name}_request_data.json`

```json
{
    "Host": "https://api.example.com",
    "Path": "/users",
    "Method": "GET",
    "Headers": {
        ...
    }
}
```

2. `{request_name}_request_body.json`

```json
{
    ...
}
```

### Response Files

The client will automatically save the response data and body to the following files:

1. `{request_name}_response_data.json`

```json
{
    "Status_Code": 200,
    "Is_Error": false,
    "Headers": {
      ...
    }
}
```

2. `{request_name}_response_body.json`

```json
{
    ...
}
```

### Example

Testing the PokéAPI:

1. Create `pokemon_api_request_data.json`

```json
{
    "Host": "https://pokeapi.co/api/v2",
    "Path": "/pokemon",
    "Method": "GET",
    "Headers": {}
}
```

`pokemon_api_request_body.json` is not needed for this example (since it's a GET request)

2. Run the client

```bash
python rest_client.py pokemon_api
```

3. Check the response files:

```bash
cat pokemon_api_response_data.json
cat pokemon_api_response_body.json
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.