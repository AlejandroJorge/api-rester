from lib.core import make_api_call, read_request_file, write_response_file
from lib.util import dbg_print
from lib.config import app_config


class BaseAPIRunner:
    def __init__(self, request_filename: str, response_filename: str):
        self.request_filename = request_filename
        self.response_filename = response_filename

    def onBeforeReadingRequest(self):
        """Hook: Runs before reading the request"""
        pass

    def onAfterReadingRequest(self):
        """Hook: Runs after reading the request"""
        pass

    def onBeforeApiCall(self):
        """Hook: Runs before making the API call"""
        pass

    def onAfterApiCall(self):
        """Hook: Runs after making the API call"""
        pass

    def onBeforeWritingResponse(self):
        """Hook: Runs before writing the response"""
        pass

    def onAfterWritingResponse(self):
        """Hook: Runs after writing the response"""
        pass

    def execute(self):
        """Main execution step"""
        self.onBeforeReadingRequest()
        self.req_data = read_request_file(self.request_filename)
        self.onAfterReadingRequest()

        self.onBeforeApiCall()
        self.res_data = make_api_call(self.req_data)
        self.onAfterApiCall()

        self.onBeforeWritingResponse()
        write_response_file(self.response_filename, self.res_data)
        self.onAfterWritingResponse()
