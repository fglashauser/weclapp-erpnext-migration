from pathlib import Path
import config
from .wc_api import WeClappAPI
from .wc_cache_api import WcCacheApi
from .wc_doctypes import WeClappDocType

class WcCacheWrapper:
    """Used for caching all doctypes from WeClapp to local database.
    """

    """list[str]: List of doctypes that have archived emails."""
    mail_doctypes = [
        WeClappDocType.SALES_INVOICE,
        WeClappDocType.SALES_ORDER,
        WeClappDocType.QUOTATION,
        WeClappDocType.TICKET
    ]
    
    def __init__(self, wc_api: WeClappAPI = None, wc_cache_api: WcCacheApi = None):
        """Initializes the cache wrapper.

        Args:
            wc_api (WeClappAPI, optional): API wrapper for accessing WeClapp data.
            Defaults to API configured in config.

            wc_cache_api (WcCacheApi, optional): API wrapper for accessing WeClapp data from cache.
            Defaults to cache configured in config.
        """
        # WeClapp API
        if wc_api:
            self.wc_api = wc_api
        else:
            self.wc_api = WeClappAPI(config.WC_API_TOKEN, config.WC_API_BASE)

        # WeClapp Cache API
        if wc_cache_api:
            self.wc_cache_api = wc_cache_api
        else:
            self.wc_cache_api = WcCacheApi(config.WC_CACHE_BASE)

    def __enter__(self):
        """Setup function for the cache wrapper.
        """
        self.wc_api.open()
        self.wc_cache_api.open()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Cleanup function for the cache wrapper.
        """
        self.wc_api.close()
        self.wc_cache_api.close()

    def _download_documents(self, doctype: WeClappDocType, ids: list[str]) -> None:
        """Downloads all documents for the given DocType and entity-IDs.
        Uses config.WC_CACHE_DOCUMENTS_BASE as base path and creates a folder for each DocType.
        Under each DocType-folder, a folder for each entity-ID is created.

        Args:
            doctype (WeClappDocType): DocType to get the documents from
            ids (list[str]): List of entity-IDs to get the documents from
        """
        for id in ids:
            # Get documents
            for document in self.wc_api.get_documents(doctype, id):
                # Create subfolders if not existing
                base_path = Path(config.WC_CACHE_DOCUMENTS_BASE).joinpath(doctype.value).joinpath(id)
                base_path.mkdir(parents=True, exist_ok=True)
                # Download document
                self.wc_api.download_document(document["id"], str(base_path.joinpath(document["name"])))

    def _cache_archived_emails(self, doctype: WeClappDocType, ids: list[str]) -> None:
        """Caches all archived E-Mails for the given DocType and entity-IDs.

        Args:
            doctype (WeClappDocType): DocType to get the archived E-Mails from
            ids (list[str]): List of entity-IDs to get the archived E-Mails from
        """
        for id in ids:
            # Get archived emails
            for email in self.wc_api.get_archived_emails(doctype, id):
                # Add meta data to email-object: doctype and id
                email["entityName"] = doctype.value
                email["entityId"] = id
                # Cache email
                self.wc_cache_api.create("archivedEmail", email)

    def cache_all(self):
        """Caches all WeClapp DocTypes to local database.
        """
        # Clear cache first
        for file in Path(config.WC_CACHE_BASE).glob("*.json"):
            file.unlink()

        # Cache all DocTypes
        for doctype in WeClappDocType:
            try:
                # Get all entities
                entities = self.wc_api.get_all(doctype, serialize_nulls=True)

                # Cache all entities
                self.wc_cache_api.create_many(doctype, entities)

                # Download all documents of the entities
                ids = [entity["id"] for entity in entities]
                self._download_documents(doctype, ids)

                # Cache all archived emails of the entities if doctype has archived emails
                if doctype in self.mail_doctypes:
                    self._cache_archived_emails(doctype, ids)

                print(f"Cached {doctype}")

            except Exception as e:
                # Doctype couldnt be cached
                print(f"Could not cache {doctype}.")
                print(e.response_text)