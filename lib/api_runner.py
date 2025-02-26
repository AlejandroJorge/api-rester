from lib.core import make_api_call, read_request_file, write_response_file
from lib.util import dbg_print


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


class DebugAPIRunner(BaseAPIRunner):
    def onBeforeReadingRequest(self):
        f = self.request_filename
        dbg_print(f"Reading request from file: {f}")
        dbg_print()

    def onAfterReadingRequest(self):
        f = self.request_filename
        dbg_print(f"Successfully read request from file: {f}")
        dbg_print()

    def onBeforeApiCall(self):
        rd = self.req_data
        url = f"{rd.protocol}://{rd.host}{rd.path}"

        dbg_print("Making API call")
        dbg_print(f"URL: {url}")
        if rd.headers:
            dbg_print("Headers:")
            for header in rd.headers:
                dbg_print(f"  {header}: {rd.headers[header]}")
        dbg_print()

    def onAfterApiCall(self):
        rd = self.res_data

        dbg_print("Successful API call")
        dbg_print(f"Status Code: {rd.status_code}")
        if rd.headers:
            dbg_print("Headers:")
            for header in rd.headers:
                dbg_print(f"  {header}: {rd.headers[header]}")
        dbg_print()

    def onBeforeWritingResponse(self):
        f = self.response_filename
        dbg_print(f"Writing response to file: {f}")
        dbg_print()

    def onAfterWritingResponse(self):
        f = self.response_filename
        dbg_print(f"Sucessfully written response to file: {f}")
        dbg_print()
