class InvalidUsage(Exception):

    def __init__(self, message, statusCode = 400, payload = None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
        self.statusCode = statusCode

    def toDict(self):
        ret = dict(self.payload or ())
        ret['message'] = self.message
        return ret