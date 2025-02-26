# Api Rester

A lightweight command-line REST client for testing APIs without the overhead of GUI applications like Postman or Insomnia.

## Installation

Api Rester can be installed through pip package manager with the following command
```bash
pip install api-rester
```

## Features

- API Calls execution with request and response stored on JSON files
- Support for all major HTTP methods (GET, POST, PUT, DELETE, HEAD, PATCH)
- Environment variables replacement on request and response files
- Alternative request and response files
- Verbose logging mode for debugging

### Coming Soon

- Query parameters support
- Network error handling
- Environment variables from file
- Persistent cookies support

## Basic Usage

1. Create a request file, by default the application recognizes the file as `request.json`

```json
{
    "protocol": "https", // required (http or https)
    "host": "api.example.com", // required
    "path": "/api/v1/users", // required
    "method": "POST", // required (GET, POST, PUT, DELETE, HEAD, PATCH)
    "headers": {
        "Content-Type": "application/json"
    },
    "body": {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
}
```

2. Execute the request

```bash
api-rester call
```

3. The application will execute the request and save the response in the `response.json` file

```json
{
    "status": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": {
        "id": 59,
        "name": "John Doe",
        "email": "john.doe@example.com" 
    }
}
```

## Custom Files

The application supports alternative files to be used as a request and response.

For example, if you have a file called `example-file.json` and want to receive the response in a different file called `example-response.json`, you can use it as a request by running the following command:

```bash
api-rester call --request-file example-file.json --response-file example-response.json
```

The application will execute the request and save the response in the `example-response.json` file.

## Environment Variables

The application supports environment variables to be replaced in the `request.json` file.

For example, if you have an environment variable called `API_KEY`, you can replace it in the `request.json` file with `${{API_KEY}}`.

```json
{
    // ...
    "path": "/api/v1/users/${{API_KEY}}"
    // ...
}
```

When you execute the request, the application will replace the `${{API_KEY}}` with the value of the `API_KEY` environment variable.

```bash
API_KEY="1234567890" api-rester call
```

The application will replace the `${{API_KEY}}` with the value of the `API_KEY` environment variable and execute the request.

```json
{
    // ...
    "path": "/api/v1/users/1234567890"
    // ...
}
```

## Example

1. Create a request file called `example-file.json`

```json
{
    "protocol": "https",
    "host": "api.example.com",
    "path": "/api/v1/users",
    "method": "POST",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer ${{API_KEY}}"
    },
    "body": {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
}
```

2. Execute the request

```bash
API_KEY=1234567890 api-rester call --request-file example-file.json --response-file example-response.json
```

3. The application will execute the request and save the response in the `example-response.json` file

```json
{
    "status": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": {
        "id": 59,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
}
```

## Template generation

Api rester can also generate a template of what it expects as a request with this command:

```bash
api-rester template
```

Which you can specify the path with --filename or --f
```bash
api-rester template --filename custom_place.json
```

It will generate this file:
```json
{
  "protocol": "http",
  "host": "localhost:3000",
  "path": "/",
  "method": "GET",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "message": "Hello world"
  }
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
