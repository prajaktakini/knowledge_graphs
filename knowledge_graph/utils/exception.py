
class ExternalAPIExceptionError(Exception):
    def __init__(self, status_code, message = None):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return "Encountered an error: status code: {}, message: {}".format(self.status_code, self.message)