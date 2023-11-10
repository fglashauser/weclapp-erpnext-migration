class ApiException(Exception):
    def __init__(self, message: str, status_code: int = None,
                 method: str = None, url: str = None, response_text: str = None):
        """Exception raised for errors in the API.
        
        Args:
            message (str): Error message
            status_code (int, optional): HTTP status code. Defaults to None.
            method (str, optional): HTTP method. Defaults to None.
            url (str, optional): URL of the request. Defaults to None.
            response_text (str, optional): Response text. Defaults to None.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.method = method
        self.url = url
        self.response_text = response_text

    def to_dict(self):
        return dict(
            message=self.message,
            status_code=self.status_code,
            method = self.method,
            url = self.url,
            response_text = self.response_text)