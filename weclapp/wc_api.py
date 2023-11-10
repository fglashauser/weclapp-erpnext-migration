import config
import requests
from requests import RequestException
from .wc_doctypes import WeClappDocType
from base import ApiBase, ApiException

class WeClappAPI(ApiBase):
    def __init__(self, api_token: str, base_url : str):
        """Class for accessing WeClapp API.

        Args:
            api_token (str)     : WeClapp API key
            base_url (str)      : WeClapp API base URL with trailing slash
            doctype (str)       : WeClapp DocType (e.g. Customer, Address, ...)
        """
        super().__init__(base_url)
        self.api_token          = api_token

    def open(self):
        """Opens the api connection.
        """
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type"          : "application/json",
            "AuthenticationToken"   : self.api_token
        }

    def close(self):
        """Closes the api connection.
        """
        self.session.close()

    def _request(self, url : str, method: str, data: dict = None, params: dict = None) -> dict:
        """Makes a request to WeClapp API

        Args:
            url (str): URL to make request to
            method (str): HTTP method (e.g. GET, POST, PUT, DELETE)
            data (dict, optional): Data to send with request. Defaults to None.

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
                    message=f"Error in {method} request to {url}: {response.text}",
                    method=method,
                    url=url,
                    response_text=response.text,
                    status_code=response.status_code
                ) from e

        return response
    
    def _get_url(self, doctype: WeClappDocType|str) -> str:
        """Returns base URL for current API-connection and given DocType.

        Args:
            doctype (WeClappDocType): Desired DocType

        Returns:
            str: Url built of Base-URL & DocType
        """
        if isinstance(doctype, str):
            return f"{self.base_url}{doctype}"
        else:
            return f"{self.base_url}{doctype.value}"

    def _get_page(self, doctype: WeClappDocType|str, page: int, page_size: int = config.WC_PAGE_SIZE,
                  serialize_nulls: bool = False) -> dict:
        """Gets a page of entities of the DocType

        Args:
            doc_type (WeClappDocType): DocType to get all entities from
            page (int): Page number
            page_size (int, optional): Page size. Defaults to config.WC_PAGE_SIZE.
            serialize_nulls (bool, optional): If True, null values will be serialized. Defaults to False.

        Returns:
            dict: JSON-response from WeClapp API
        """
        url = self._get_url(doctype)
        if serialize_nulls:
            url += "?serializeNulls=true"
        return self._request(url, "GET", None, { "page": page, "pageSize": page_size }).json()["result"]
    
    def get_all(self, doctype: WeClappDocType|str, serialize_nulls: bool = False) -> list[dict]:
        """Get all entities of the DocType

        Args:
            doc_type (WeClappDocType): DocType to get all entities from
            serialize_nulls (bool, optional): If True, null values will be serialized. Defaults to False.

        Returns:
            dict: JSON-response from WeClapp API
        """
        count = self.get_count(doctype)                                     # Get count of entities
        pages = (count + config.WC_PAGE_SIZE - 1) // config.WC_PAGE_SIZE    # Calculate amount of pages

        # Get all pages and merge them
        result = []
        for page in range(1, pages + 1):
            result += self._get_page(doctype, page, serialize_nulls=serialize_nulls)
            
        return result
    
    def get(self, doctype: WeClappDocType|str, id : str, serialize_nulls: bool = False) -> dict:
        """Get an entity of the DocType

        Args:
            doc_type (WeClappDocType): DocType to get the entity from
            id (int): ID of the entity to get
            serialize_nulls (bool, optional): If True, null values will be serialized. Defaults to False.

        Returns:
            dict: JSON-response from WeClapp API
        """
        url = f"{self._get_url(doctype)}/id/{id}"
        if serialize_nulls:
            url += "?serializeNulls=true"
        return self._request(url, "GET").json()

    def search(self, doctype: WeClappDocType|str, field: str, value: str) -> list[dict]:
        """Starts a search in the WeClapp-API by passing a fieldname of the current DocType
        and a value to search for.
        Uses the -eq (equals) modifier.

        Args:
            field (str): Name of the field to check for
            value (str): The value to search for

        Returns:
            dict: JSON-response from WeClapp API
        """
        return self._request(f"{self._get_url(doctype)}", "GET", None, { f"{field}-eq": value }).json()["result"]
    
    def get_count(self, doctype: WeClappDocType|str) -> int:
        """Returns the count of readable objects of the DocType

        Returns:
            int: Amount of objects of DocType
        """
        result = self._request(f"{self._get_url(doctype)}/count", "GET").json()
        if result and result.get("result", None) != None:
            return result["result"]
        else:
            raise ApiException(
                message=f"Couldn't get amount of {doctype}-DocType",
                method="GET",
                url=f"{self._get_url(doctype)}/count"
            )

    def create(self, doctype: WeClappDocType|str, data : dict) -> dict:
        """Creates a new entity of the DocType

        Args:
            doctype (WeClappDocType): DocType to create the entity in
            data (dict): Data to fill the entity with

        Returns:
            dict: JSON-response from WeClapp API
        """
        return self._request(self._get_url(doctype), "POST", data).json()

    def update(self, doctype: WeClappDocType|str, id : int, data : dict) -> dict:
        """Updates an entity of the DocType

        Args:
            id (int)    : ID of the entity to update
            data (dict) : Data to update the entity with

        Returns:
            dict: JSON-response from WeClapp API
        """
        return self._request(f"{self._get_url(doctype)}/id/{id}", "PUT", data).json()

    def delete(self, doctype: WeClappDocType|str, id : int) -> dict:
        """Deletes an entity of the DocType

        Args:
            id (int): ID of the entity to delete

        Returns:
            dict: JSON-response from WeClapp API
        """
        return self._request(f"{self._get_url(doctype)}/id/{id}", "DELETE").json()
    
    def get_documents(self, doctype: WeClappDocType|str, id: str) -> list[dict]:
        """Gets all linked documents for a given DocType and ID.

        Args:
            doctype (WeClappDocType): DocType to get the documents from
            id (str): ID of the entity to get the documents from

        Returns:
            list[dict]: List of documents
        """
        return self._request(self._get_url("document"), "GET",
                             params={"entityName": doctype.value, "entityId": id}).json()["result"]
    
    def download_document(self, id: str, filename: str) -> None:
        """Downloads a document from WeClapp

        Args:
            id (str): ID of the document to download
            filename (str): Filename to save the document to
        """
        url = f"{self.base_url}document/id/{id}/download"
        response = self._request(url, "GET")
        # Save result to PDF-file
        with open(filename, "wb") as file:
            file.write(response.content)

    def get_archived_emails(self, doctype: WeClappDocType|str, id: str) -> list[dict]:
        """Gets all archived emails for a given DocType and ID.

        Args:
            doctype (WeClappDocType): DocType to get the archived emails from
            id (str): ID of the entity to get the archived emails from

        Returns:
            list[dict]: List of archived emails
        """
        return self._request(self._get_url('archivedEmail'), "GET",
                             params={"entityName": doctype.value,
                                     "entityId": id, "serializeNulls": True}).json()["result"]