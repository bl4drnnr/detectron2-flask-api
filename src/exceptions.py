class ApiResponse(Exception):
    def __init__(self, response, status_code=200):
        self.response = {"data": response, "status_code": status_code}
        self.status_code = status_code


class WrongPayload(Exception):
    def __init__(self, response='Wrong payload', status_code=500):
        self.response = {"data": response, "status_code": status_code}
        self.status_code = status_code
