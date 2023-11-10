from abc import ABC, abstractmethod
from .doctype import DocType

class ApiBase(ABC):
    """Base class for API wrapper classes.
    """

    def __init__(self, base_url: str):
        """Initializes the api wrapper.

        Args:
            base_url (str): Base url of the api
        """
        self.base_url = base_url

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @abstractmethod
    def open(self):
        """Opens the api connection.
        """
        pass

    @abstractmethod
    def close(self):
        """Closes the api connection.
        """
        pass

    @abstractmethod
    def get_all(self, doctype: DocType|str) -> list:
        """Returns all objects of the given DocType.

        Args:
            doctype (str): DocType to get all objects from

        Returns:
            list: List of objects
        """
        pass

    @abstractmethod
    def get(self, doctype: DocType|str, id: str) -> dict:
        """Returns the object with the given name and DocType.

        Args:
            doctype (str): DocType of the object
            name (str): Name of the object

        Returns:
            dict: Object
        """
        pass

    @abstractmethod
    def create(self, doctype: DocType|str, data: dict) -> dict:
        """Creates a new object of the given DocType.

        Args:
            doctype (str): DocType of the object
            data (dict): Data of the object

        Returns:
            dict: Created object
        """
        pass

    @abstractmethod
    def update(self, doctype: DocType|str, id: str, data: dict) -> dict:
        """Updates the object with the given name and DocType.

        Args:
            doctype (str): DocType of the object
            name (str): Name of the object
            data (dict): Data of the object

        Returns:
            dict: Updated object
        """
        pass

    @abstractmethod
    def delete(self, doctype: DocType|str, id: str) -> dict:
        """Deletes the object with the given name and DocType.

        Args:
            doctype (str): DocType of the object
            name (str): Name of the object

        Returns:
            dict: Deleted object
        """
        pass

    @abstractmethod
    def get_count(self, doctype: DocType|str) -> int:
        """Returns the count of objects of the given DocType.

        Args:
            doctype (str): DocType to get the count from

        Returns:
            int: Count of objects
        """
        pass

    @abstractmethod
    def search(self, doctype: DocType|str, field: str, value: str) -> list:
        """Returns all objects of the given DocType with the given field-value.

        Args:
            doctype (str): DocType to search in
            field (str): Name of the field to check for
            value (str): The value to search for

        Returns:
            list: List of objects
        """
        pass