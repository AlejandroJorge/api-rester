# Api Rester 🚀

A lightweight, user-friendly command-line REST client that lets you test APIs without the overhead of GUI applications like Postman or Insomnia. Perfect for developers who prefer staying in their terminal!

## Installation 📥

Install Api Rester using pip:
```bash
pip install api-rester
```

## Why Api Rester? ✨

Api Rester provides a streamlined way to test APIs directly from your terminal:

Core Features:
- Make API calls using JSON files for requests and responses
- Support for common HTTP methods (GET, POST, PUT, DELETE, HEAD, PATCH)
- Handle query parameters and headers
- Environment variable substitution from .env files
- Configurable verbose logging for debugging

Request/Response Handling:
- Store and validate requests/responses as JSON
- Validate domains and paths
- Safe handling of HTTP headers
- Support for alternative request/response files

Cookie Management:
- Persistent cookie storage between requests
- Cookie validation and security checks

## Getting Started 🎯

### 1. Create Your First Request

Create a `request.json` file:

```json
{
    "protocol": "https",
    "host": "api.example.com",
    "path": "/api/v1/users",
    "method": "POST",
    "headers": {
        "Content-Type": "application/json"
    },
    "body": {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
}
```

### 2. Make the Call

```bash
api-rester call
```

### 3. Check the Response

Api Rester saves the response in `response.json`:

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

## Advanced Features

### Custom File Names

Need to use different file names? No problem:

```bash
api-rester call --request-file custom-request.json --response-file custom-response.json
```

### Environment Variables

Use environment variables in your requests with `${{VARIABLE_NAME}}` syntax:

```json
{
    "headers": {
        "Authorization": "Bearer ${{API_KEY}}"
    }
}
```

Run it with:
```bash
API_KEY=your_key_here api-rester call
```

### Query Parameters Made Easy

Add query parameters that are automatically encoded:

```json
{
    "protocol": "https",
    "host": "api.example.com",
    "path": "/search",
    "method": "GET",
    "queryParams": {
        "q": "search term",
        "filter": ["active", "verified"]
    }
}
```

### Smart Cookie Management

Cookies are automatically handled between requests and stored in `cookies.json`. They're automatically sent with matching domain requests - just like a browser would do!

### Debug Mode

Need to see what's happening? Use verbose mode:

```bash
api-rester call --v
```

### Quick Cleanup

Clean up generated files:

```bash
api-rester clear
```

Or specify custom files to clear:
```bash
api-rester clear --req custom-request.json --res custom-response.json --cookies custom-cookies.json
```

### Generate Request Templates

Start with a template to save time:

```bash
api-rester template --filename my-request.json
```

## Coming Soon 🔜

- Request timeouts
- Stdin/Stdout support for piping: `python seeder-script.py | api-rester call | bash analytics-script.sh`

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
