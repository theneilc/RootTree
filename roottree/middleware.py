import traceback
import sys

class ProcessExceptionMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 200:
            traceback.print_exc()
        return response
