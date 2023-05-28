import requests
from requests.auth import HTTPBasicAuth
from requests import RequestException
from .en_api_data import ERPNextAPIData

class ERPNextAPIError(Exception):
    """
    Exception raised for errors in the ERPNext API.
    """
    def __init__(self, message, method, url, response_text, status_code):
        super().__init__(message)
        self.message        = message
        self.method         = method
        self.url            = url
        self.response_text  = response_text
        self.status_code    = status_code

class ERPNextAPI:
    def __init__(self, api_key : str, api_secret : str, base_url : str, doctype : str):
        """Class for accessing ERPNext API.

        Args:
            api_key (str): ERPNext API key
            api_secret (str): ERPNext API secret
            base_url (str): ERPNext API base URL with trailing slash
            doctype (str): ERPNext DocType (e.g. Customer, Address, ...)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.doctype = doctype
        self.url = f"{base_url}{doctype}"
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(api_key, api_secret)
        self.session.headers = {"Content-Type": "application/json"}

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
    
    def _process_child_data(self, child_data: ERPNextAPIData) -> str:
        """Process child data

        Args:
            child_data (ERPNextAPIData): Child data

        Returns:
            str: Name of child data
        """
        doctype_url = f"{self.base_url}{child_data.doctype}"
        child_url = f"{doctype_url}/{child_data.name}"
        try:
            response = self._request(child_url, "GET")
        except ERPNextAPIError as e:
            if e.status_code == 404:  # Not found, create new
                response = self._request(doctype_url, "POST", child_data)
            else:
                raise e
        else:
            if child_data.update_existing:
                response = self._request(child_url, "PUT", child_data)

        return response["data"]["name"]

    def _process_data(self, data: dict) -> dict:
        """Process data

        Args:
            data (dict): Data to process

        Returns:
            dict: Processed data
        """
        for key, value in data.items():
            if isinstance(value, ERPNextAPIData):
                name = self._process_child_data(value)
                data[key] = name
            elif isinstance(value, dict):
                data[key] = self._process_data(value)
        return data

    def _request(self, url: str, method: str, data: ERPNextAPIData = None) -> dict:
        """Makes a request to ERPNext API

        Args:
            url (str): URL to make request to
            method (str): HTTP method (e.g. GET, POST, PUT, DELETE)
            data (ERPNextAPIData, optional): Data to send with request. Defaults to None.

        Returns:
            dict: Response JSON
        Raises:
            Exception: If request fails
        """
        if data is not None:
            data = self._process_data(data)

        try:
            #response = self.session.request(
            #    method=method, url=url, json=data
            #)
            response = requests.request(
                method=method, url=url, json=data, auth=self.session.auth, headers=self.session.headers
            )
            response.raise_for_status()
        except RequestException as e:
            if response.status_code == 404:
                raise ERPNextAPIError(
                    f"{self.doctype} not found: {response.text}",
                    method,
                    url,
                    response.text,
                    response.status_code,
                ) from e
            else:
                raise ERPNextAPIError(
                    f"Error in {method} request to {url}: {response.text}",
                    method,
                    url,
                    response.text,
                    response.status_code,
                ) from e

        return response.json()

    def create_link(self, parent_doctype : str, parent_name : str, child_doctype : str, child_name : str) -> dict:
        """Create a link between two entities

        Args:
            parent_doctype (str): Parent DocType
            parent_name (str): Parent name
            child_doctype (str): Child DocType
            child_name (str): Child name

        Returns:
            dict: Response JSON
        """
        url = f"{self.base_url}{child_doctype}/{child_name}"
        data = {
            "links": [{
                "link_doctype": parent_doctype,
                "link_name": parent_name
            }]
        }
        return self._request(url, "PUT", data)
        
    def get_all(self) -> dict:
        """Get all entities of the DocType

        Returns:
            dict: JSON-response from ERPNext API
        """
        return self._request(self.url, "GET")

    def create(self, data : dict) -> dict:
        """Creates a new entity of the DocType

        Args:
            data (dict): Data to fill the entity with

        Returns:
            dict: JSON-response from ERPNext API
        """
        return self._request(self.url, "POST", data)

    def update(self, name : str, data : dict) -> dict:
        """Updates an entity of the DocType

        Args:
            name (str): Name of the entity to update
            data (dict): Data to update the entity with

        Returns:
            dict: JSON-response from ERPNext API
        """
        return self._request(f"{self.url}/{name}", "PUT", data)

    def delete(self, name : str) -> dict:
        """Deletes an entity of the DocType

        Args:
            name (str): Name of the entity to delete

        Returns:
            dict: JSON-response from ERPNext API
        """
        return self._request(f"{self.url}/{name}", "DELETE")
    
    def get(self, name : str) -> dict:
        """Get an entity of the DocType

        Args:
            name (str): Name of the entity to get

        Returns:
            dict: JSON-response from ERPNext API
        """
        return self._request(f"{self.url}/{name}", "GET")