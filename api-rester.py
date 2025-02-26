from lib.api_runner import APIRunner

api_runner = APIRunner(request_filename="request.json",
                       response_filename="response.json")

api_runner.execute()
