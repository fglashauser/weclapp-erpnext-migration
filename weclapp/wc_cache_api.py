from pathlib import Path
from pysondb import PysonDB
from base import ApiBase, ApiException
from .wc_doctypes import WeClappDocType

class WcCacheApi(ApiBase):
    """Class for accessing WeClapp data from cache (psysondb)
    """

    def __init__(self, base_url: str):
        """Initializes the api wrapper for local WeClapp-db cache.

        Args:
            base_url (str): Base filepath to database-files (.json)
        """
        super().__init__(base_url)
        self._open_conns = {}   # Used for storing open connections to databases

    def open(self):
        """Opens the api connection.
        """
        # Checks the base file path
        path = Path(self.base_url)
        if not path.exists() or not path.is_dir():
            raise ApiException(
                message=f"Base file path '{self.base_url}' does not exist or is not a directory.",
                method="open",
                url=self.base_url
            )

    def close(self):
        """Closes the api connection.
        """
        pass

    def _get_db(self, doctype: WeClappDocType|str) -> PysonDB:
        """Returns the database for the given DocType.

        Args:
            doctype (WeClappDocType|str): DocType to get the database from

        Returns:
            PysonDB: Database
        """
        doctype_str = doctype.value if isinstance(doctype, WeClappDocType) else doctype

        # Checks if database is already open
        if self._open_conns.get(doctype_str, None):
            return self._open_conns[doctype_str]

        # Opens the database
        db_path = Path(self.base_url).joinpath(f"{doctype_str}.json")
        try:
            self._open_conns[doctype_str] = PysonDB(str(db_path))
            return self._open_conns[doctype_str]
        except Exception as e:
            raise ApiException(
                message=f"Could not get database for DocType '{doctype_str}'.",
                method="_get_db",
                url=self.base_url
            ) from e
        
    def _get_by_db_id(self, doctype: WeClappDocType|str, id: str) -> dict:
        """Returns the object with the given id from the given DocType.

        Args:
            doctype (str): DocType to get the object from
            id (str): ID of the object

        Returns:
            dict: Object
        """
        return self._get_db(doctype).get_by_id(id)

    def get_all(self, doctype: WeClappDocType|str) -> list:
        """Returns all objects of the given DocType.

        Args:
            doctype (str): DocType to get all objects from

        Returns:
            list: List of objects
        """
        return list(self._get_db(doctype).get_all().values())

    def get(self, doctype: WeClappDocType|str, id: str) -> dict:
        """Returns the object with the given name and DocType.

        Args:
            doctype (str): DocType of the object
            name (str): Name of the object

        Returns:
            dict: Object
        """
        return self._get_db(doctype).get_by_query(lambda x: x["id"] == id)

    def create(self, doctype: WeClappDocType|str, data: dict) -> dict:
        """Creates a new object of the given DocType.

        Args:
            doctype (str): DocType of the object
            data (dict): Data of the object

        Returns:
            dict: Created object
        """
        return self._get_by_db_id(doctype, self._get_db(doctype).add(data))
    
    def create_many(self, doctype: WeClappDocType|str, data : list) -> None:
        """Creates multiple new entities of the DocType
        
        Args:
            doc_type (WeClappDocType): DocType to create the entities for
            data (list): Data to fill the entities with
        """
        self._get_db(doctype).add_many(data)

    def update(self, doctype: WeClappDocType|str, id: str, data: dict) -> dict:
        """Updates the object with the given name and DocType.

        Args:
            doctype (str): DocType of the object
            name (str): Name of the object
            data (dict): Data of the object

        Returns:
            dict: Updated object
        """
        updated_ids = self._get_db(doctype).update_by_query(lambda x: x["id"] == id, data)
        if len(updated_ids) > 0:
            return self._get_by_db_id(updated_ids[0])

    def delete(self, doctype: WeClappDocType|str, id: str) -> None:
        """Deletes the object with the given name and DocType.

        Args:
            doctype (str): DocType of the object
            name (str): Name of the object
        """
        self._get_db(doctype).delete_by_query(lambda x: x["id"] == id)

    def get_count(self, doctype: WeClappDocType|str) -> int:
        """Returns the count of objects of the given DocType.

        Args:
            doctype (str): DocType to get the count from

        Returns:
            int: Count of objects
        """
        raise NotImplementedError("get_count is not implemented for WcCacheApi")

    def search(self, doctype: WeClappDocType|str, field: str, value: str) -> list:
        """Returns all objects of the given DocType with the given field-value.

        Args:
            doctype (str): DocType to search in
            field (str): Name of the field to check for
            value (str): The value to search for

        Returns:
            list: List of objects
        """
        return self._get_db(doctype).get_by_query(lambda x: x[field] == value)