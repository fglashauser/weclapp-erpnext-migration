from abc import ABC, abstractmethod
from erpnext import ERPNextAPI, ERPNextDocType
from pathlib import Path
import config
from weclapp import WeClappDocType

class BaseMigration(ABC):
    """Base class for all migration classes.
    Used to migrate a single dataset from WeClapp to ERPNext.
    Using a existing dict-Object from WeClapp-API.
    """

    def __init__(self, en_api: ERPNextAPI, wc_data: dict):
        """Initializes the migration wrapper.

        Args:
            en_api (ERPNextAPI): ERPNext-API-Object
            wc_data (dict): WeClapp-API-Object
        """
        self._en_api = en_api
        self.wc_data = wc_data
        self._is_primary = False

    def migrate(self) -> dict:
        """Migrates a given WeClapp-Object and creates it in ERPNext.

        Returns:
            dict: Data of the created entity
        """
        return self._en_api.create(self.get_doctype(), self._transform())

    def is_primary(self) -> bool:
        """Returns if the contact is the primary contact of the customer.
        """
        return self._is_primary
    
    def upload_weclapp_documents(self, name: str):
        """Uploads and assigns the original WeClapp documents.

        Args:
            name (str): Name of the entity to upload the documents to
        """
        id = self.wc_data.get("id", None)
        if not id:
            return
        
        # Get WeClapp document-root by invoice ID
        wc_doc_base = Path(f"{config.WC_CACHE_DOCUMENTS_BASE}{self.get_wc_doctype().value}/{id}/")

        # Check if base path exists
        if not wc_doc_base.exists():
            return
        
        # Get all files in directory
        files = [f for f in wc_doc_base.iterdir() if f.is_file()]

        # Upload all files
        for file in files:
            self._en_api.upload_file(self.get_doctype(), name, str(file))
            print(f"Uploaded file {file.name}")

    @abstractmethod
    def _transform(self) -> dict:
        """Transforms the data from WeClapp to ERPNext.

        Returns:
            dict: Transformed data
        """
        pass

    @abstractmethod
    def get_doctype(self) -> ERPNextDocType:
        """Returns the ERPNext DocType of the object.

        Returns:
            ERPNextDocTypes: ERPNext DocType
        """
        pass

    @abstractmethod
    def get_wc_doctype(self) -> WeClappDocType:
        """Returns the WeClapp DocType of the object.

        Returns:
            WeClappDocTypes: WeClapp DocType
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """
        Validates the given data.

        Returns:
            bool: True if valid, False if not
        """
        pass