from lib.core import make_api_call, read_request_file, write_response_file


class APIRunner:
    def __init__(self, request_filename: str, response_filename: str):
        self.request_filename = request_filename
        self.response_filename = response_filename

    def onBeforeApiCall(self):
        """Runs before making the API call"""
        pass

    def onAfterApiCall(self):
        """Runs after making the API call"""
        pass

    def execute(self):
        """Main execution step"""
        self.req_data = read_request_file(self.request_filename)

        self.onBeforeApiCall()
        self.res_data = make_api_call(self.req_data)
        self.onAfterApiCall()

        write_response_file(self.response_filename, self.res_data)
