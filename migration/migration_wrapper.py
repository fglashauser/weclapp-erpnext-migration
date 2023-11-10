from pathlib import Path
import config
from .base_migration import BaseMigration
from .customer_migration import CustomerMigration
from .address_migration import AddressMigration
from .invoice_migration import InvoiceMigration
from weclapp import WeClappAPI, WeClappDocType, WcCacheApi
from erpnext import ERPNextAPI, ERPNextDocType

class MigrationWrapper:
    """Generic migration wrapper from WeClapp to ERPNext.
    """

    def __init__(self, wc_doctype: WeClappDocType, en_doctype: ERPNextDocType):
        """Initializes the migration wrapper.

        Args:
            wc_doctype (WeClappDocTypes): WeClapp document type
            en_doctype (ERPNextDocTypes): ERPNext document type
        """
        self.wc_doctype = wc_doctype
        self.en_doctype = en_doctype
        #self.wc_api = WeClappAPI(config.WC_API_TOKEN, config.WC_API_BASE)
        self.wc_api = WcCacheApi(config.WC_CACHE_BASE)
        self.en_api = ERPNextAPI(config.EN_API_KEY, config.EN_API_SECRET, config.EN_API_BASE)

    def __enter__(self):
        """Setup function for the migration wrapper.
        """
        self.wc_api.open()
        self.en_api.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Cleanup function for the migration wrapper.
        """
        self.wc_api.close()
        self.en_api.close()

    def migrate_all(self):
        """Migrates all documents from WeClapp to ERPNext of the given DocType.
        """
        wc_data = self.wc_api.get_all(self.wc_doctype)
        for wc_obj in wc_data:
            migration = self._get_migration(wc_obj)
            en_obj = migration.migrate()
            if en_obj:
                print(f"Created {self.en_doctype} {en_obj['name']}")

    def _get_migration(self, wc_obj: dict) -> BaseMigration:
        """Returns the migration object for the given WeClapp-Object.

        Returns:
            BaseMigration: Migration object
        """
        match self.en_doctype:
            case ERPNextDocType.CUSTOMER:
                return CustomerMigration(self.en_api, wc_obj)
            case ERPNextDocType.ADDRESS:
                return AddressMigration(self.en_api, wc_obj)
            case ERPNextDocType.SALES_INVOICE:
                return InvoiceMigration(self.en_api, wc_obj)
            case _:
                raise Exception("No migration found for given doctype!")