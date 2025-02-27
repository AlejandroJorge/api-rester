from lib.core import make_api_call, read_request_file
from lib.core import write_cookies_file, write_response_file

from lib.core import read_cookies_file


class BaseAPIRunner:
    def __init__(self, request_filename: str,
                 response_filename: str,
                 cookies_filename: str
                 ):
        self.request_filename = request_filename
        self.response_filename = response_filename
        self.cookies_filename = cookies_filename

    def onBeforeReadingRequest(self):
        """Hook: Runs before reading the request"""
        pass

    def onAfterReadingRequest(self):
        """Hook: Runs after reading the request"""
        pass

    def onBeforeReadingCookies(self):
        """Hook: Runs before reading the cookies"""
        pass

    def onAfterReadingCookies(self):
        """Hook: Runs after reading the cookies"""
        pass

    def onBeforeApiCall(self):
        """Hook: Runs before making the API call"""
        pass

    def onAfterApiCall(self):
        """Hook: Runs after making the API call"""
        pass

    def onBeforeWritingCookies(self):
        """Hook: Runs before writing the cookies"""
        pass

    def onAfterWritingCookies(self):
        """Hook: Runs after writing the cookies"""
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

        self.onBeforeReadingCookies()
        self.cookies_data = read_cookies_file(self.cookies_filename)
        self.onAfterReadingCookies()

        self.onBeforeApiCall()
        self.res_data, self.cookies_data = make_api_call(
            self.req_data, self.cookies_data)
        self.onAfterApiCall()

        self.onBeforeWritingCookies()
        write_cookies_file(self.cookies_filename, self.cookies_data)
        self.onAfterWritingCookies()

        self.onBeforeWritingResponse()
        write_response_file(self.response_filename, self.res_data)
        self.onAfterWritingResponse()
