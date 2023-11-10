import config
from .base_migration import BaseMigration
from .bank_migration import BankMigration
from erpnext import ERPNextAPI, ERPNextHelper, ERPNextDocType

class BankAccountMigration(BaseMigration):
    """Migration wrapper for address objects from WeClapp to ERPNext.
    """

    def __init__(self, en_api: ERPNextAPI, wc_data: dict, en_customer_data: dict = None):
        """Initializes the contact migration.

        Args:
            en_api (ERPNextAPI): ERPNext-API-Object
            wc_data (dict): WeClapp-API-Object
            en_customer_data (dict, optional): ERPNext-API-Object of the customer (parent). Defaults to None.
        """
        super().__init__(en_api, wc_data)
        self.en_customer_data = en_customer_data
        self._is_primary = self.wc_data.get("primary", False)

    def get_doctype(self) -> ERPNextDocType:
        return ERPNextDocType.BANK_ACCOUNT
    
    def validate(self) -> bool:
        """
        Validates the given data.

        Returns:
            bool: True if valid, False if not
        """
        return self.wc_data.get("accountHolder", None) and \
            self.wc_data.get("accountNumber", None) and \
            self.wc_data.get("bankCode", None) and \
            self.wc_data.get("creditInstitute", None)

    def migrate(self) -> dict:
        """Migrates a given WeClapp-Object and creates it in ERPNext.

        Returns:
            str: Name of the created entity
        """
        # Base data
        en_data = self._transform()

        # Create bank in ERPNext
        bank_migration = BankMigration(self._en_api, self.wc_data)
        if bank_migration.validate():
            en_bank = bank_migration.migrate()
            en_data["bank"] = en_bank["name"]       # Assign bank to account

            # Create bank account in ERPNext
            return self._en_api.create(ERPNextDocType.BANK_ACCOUNT, en_data)


    def _transform(self) -> dict:
        """Transforms the data from WeClapp to ERPNext.

        Returns:
            dict: Transformed data
        """
        transformed_data = {
            "account_name"      : self._map_account_name(),
            "account_type"      : config.EN_BANK_ACCOUNT_TYPE,
            "is_default"        : self.is_primary(),
            "party_type"        : "Customer",
            "party"             : self.en_customer_data.get("name", None),
            "iban"              : self.wc_data.get("accountNumber", None)
        }
        return transformed_data
    
    def _map_account_name(self) -> str:
        """
        Maps the account name with the provided customer number (if given) or the address id from WeClapp.
        """
        if self.en_customer_data and self.en_customer_data.get("name", None):
            return self.en_customer_data["name"]
        else:
            return str(self.wc_data.get("id", None))