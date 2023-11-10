import requests
import json
from enum import Enum
from requests.auth import HTTPBasicAuth
from requests import RequestException
from .en_api_data import ERPNextAPIChild
from .en_doctypes import ERPNextDocType
from base import ApiBase, ApiException
from pathlib import Path

class FilterOperator(Enum):
    EQUALS                  = "="
    NOT_EQUALS              = "!="
    LESS_THAN               = "<"
    GREATER_THAN            = ">"
    LESS_THAN_OR_EQUALS     = "<="
    GREATER_THAN_OR_EQUALS  = ">="

class ERPNextFilter:
    def __init__(self, field: str, operator: FilterOperator, value: str):
        self.field = field
        self.operator = operator
        self.value = value

    def get_erpnext_filter(self) -> list:
        return [self.field, self.operator.value, self.value]

class ERPNextAPI(ApiBase):
    def __init__(self, api_key : str, api_secret : str, base_url : str):
        """Class for accessing ERPNext API.

        Args:
            api_key (str): ERPNext API key
            api_secret (str): ERPNext API secret
            base_url (str): ERPNext API base URL with trailing slash
            doctype (str): ERPNext DocType (e.g. Customer, Address, ...)
        """
        super().__init__(base_url)
        self.api_key = api_key
        self.api_secret = api_secret

    def open(self):
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.api_key, self.api_secret)
        self.session.headers = {"Content-Type": "application/json"}

    def close(self):
        self.session.close()
    
    def _request(self, url: str, method: str, data: dict = None, params: dict = None) -> dict:
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
        try:
            response = self.session.request(method=method, url=url, json=data, params=params)
            response.raise_for_status()
        except RequestException as e:
            if response.status_code == 404:
                raise ApiException(
                    message=f"Not found: {response.text}",
                    method=method,
                    url=url,
                    response_text=response.text,
                    status_code=response.status_code
                ) from e
            else:
                raise ApiException(
                    f"Error in {method} request to {url}: {response.text}",
                    method=method,
                    url=url,
                    response_text=response.text,
                    status_code=response.status_code
                ) from e

        return response.json()

    def _get_resource_url(self, doctype: ERPNextDocType) -> str:
        """Returns base URL for current API-connection and given DocType.

        Args:
            doctype (WeClappDocTypes): Desired DocType

        Returns:
            str: Url built of Base-URL & DocType
        """
        return f"{self.base_url}resource/{doctype.value}"

    def _get_method_url(self, method: str) -> str:
        """Returns base URL for current API-connection and given DocType.

        Args:
            method (str): Desired method

        Returns:
            str: Url built of Base-URL & API-method
        """
        return f"{self.base_url}method/{method}"

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
        url = f"{self.base_url}resource/{child_doctype}/{child_name}"
        data = {
            "links": [{
                "link_doctype": parent_doctype,
                "link_name": parent_name
            }]
        }
        return self._request(url, "PUT", data)
        
    def get_all(self, doctype: ERPNextDocType) -> dict:
        """Get all entities of the DocType

        Returns:
            dict: JSON-response from ERPNext API
        """
        return self._request(self._get_resource_url(doctype), "GET")
    
    def get(self, doctype: ERPNextDocType, id : str) -> dict:
        """Get an entity of the DocType

        Args:
            name (str): Name of the entity to get

        Returns:
            dict: JSON-response from ERPNext API
        """
        try:
            return self._request(f"{self._get_resource_url(doctype)}/{id}", "GET")["data"]
        except ApiException as e:
            if e.status_code == 404:
                return None

    def create(self, doctype: ERPNextDocType, data : dict) -> dict:
        """Creates a new entity of the DocType

        Args:
            data (dict): Data to fill the entity with

        Returns:
            dict: JSON-response from ERPNext API
        """
        return self._request(self._get_resource_url(doctype), "POST", data)["data"]

    def update(self, doctype: ERPNextDocType, id : str, data : dict) -> dict:
        """Updates an entity of the DocType

        Args:
            name (str): Name of the entity to update
            data (dict): Data to update the entity with

        Returns:
            dict: JSON-response from ERPNext API
        """
        return self._request(f"{self._get_resource_url(doctype)}/{id}", "PUT", data)

    def delete(self, doctype: ERPNextDocType, id : str) -> dict:
        """Deletes an entity of the DocType

        Args:
            name (str): Name of the entity to delete

        Returns:
            dict: JSON-response from ERPNext API
        """
        return self._request(f"{self._get_resource_url(doctype)}/{id}", "DELETE")

    def search(self, doctype: ERPNextDocType, filters: list) -> dict:
        """Search for entities of the DocType

        Args:
            filters (list): Filters to search for (must contain ERPNextFilter-objects)

        Returns:
            dict: JSON-response from ERPNext API
        """
        filters_converted = []
        for filter in filters:
            filters_converted.append(filter.get_erpnext_filter())

        return self._request(self._get_resource_url(doctype), "GET",
                             params={"filters": json.dumps(filters_converted)})["data"]
    
    def get_count(self, doctype: ERPNextDocType) -> int:
        raise NotImplementedError("Not implemented yet")
    
    def upload_file(self, doctype: ERPNextDocType, id: str, file_path: str) -> dict:
        """Uploads a file to the given DocType

        Args:
            doctype (ERPNextDocType): DocType to upload file to
            id (str): ID of the entity to upload file to
            file_path (str): Path to file to upload
            file_name (str, optional): Name of the file to upload. Defaults to original file name.

        Returns:
            dict: JSON-response from ERPNext API
        """
        # Upload file
        headers = {
            'Authorization': f"token {self.api_key}:{self.api_secret}",
        }
        with open(file_path, "rb") as file:
            response = requests.post(
                url     = self._get_method_url("upload_file"),
                headers = headers,
                files   = {"file": file},
                data    = {"doctype": doctype.value, "docname": id}
            )
            response.raise_for_status()