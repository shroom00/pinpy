class PinpyException(Exception):
    """Base exception for Pinterest Errors"""
    pass


class PinterestError(PinpyException):
    """Class to handle json formatted pinterest errors"""

    def __init__(self, response) -> None:
        self.status_code = response.status_code
        self.response_json = response.json()
        if "code" not in self.response_json and "body" in self.response_json:
            self.response_json = self.response_json["body"]["response"]["error"]
        self.api_code = self.response_json["code"]
        self.api_message = self.response_json["message"]
        self.message_detail = self.response_json["message_detail"] if "message_detail" in self.response_json else None
        super().__init__(f"({self.api_code}) {self.api_message}{' - ' + self.message_detail if self.message_detail else ''}")