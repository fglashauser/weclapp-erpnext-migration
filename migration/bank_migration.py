from .base_migration import BaseMigration
from erpnext import ERPNextAPI, ERPNextHelper, ERPNextDocType, ERPNextFilter, FilterOperator

class BankMigration(BaseMigration):
    """Migration wrapper for address objects from WeClapp to ERPNext.
    """

    def __init__(self, en_api: ERPNextAPI, wc_data: dict):
        """Initializes the contact migration.

        Args:
            en_api (ERPNextAPI): ERPNext-API-Object
            wc_data (dict): WeClapp-API-Object
            wc_customer_data (dict, optional): WeClapp-API-Object of the customer (parent). Defaults to None.
        """
        super().__init__(en_api, wc_data)
    
    def get_doctype(self) -> ERPNextDocType:
        return ERPNextDocType.BANK

    def validate(self) -> bool:
        """
        Validates the given data.

        Returns:
            bool: True if valid, False if not
        """
        return self.wc_data.get("creditInstitute", None) and \
            self.wc_data.get("bankCode", None)

    def migrate(self) -> dict:
        """Migrates a given WeClapp-Bank and creates it in ERPNext or gets the existing one.
        This function tries to find a existing bank in ERPNext first which matches the SWIFT-number.
        If it can't find a bank, it will create a new one. In case the wished name already exists,
        it will append a number to the name in such format: "Name (1)".

        Returns:
            dict: Created or found bank
        """
        new_bank = self._transform()
        bank_name = new_bank.get("bank_name", None)
        swift_number = new_bank.get("swift_number", None)

        # Search for existing bank with same swift number
        banks = self._en_api.search(ERPNextDocType.BANK, filters=[ERPNextFilter("swift_number",
                                                                                 FilterOperator.EQUALS, swift_number)])
        if len(banks) > 0:
            existing_bank = banks[0]
            return existing_bank
        
        # Create new bank: is the name already taken?
        existing_bank = self._en_api.get(ERPNextDocType.BANK, bank_name)
        if not existing_bank:
            # Name is free -> create new bank
            return self._en_api.create(ERPNextDocType.BANK, new_bank)
        else:
            # Name is taken -> append next free number to name
            new_bank_name = None
            i = 1
            while not new_bank_name:
                query_bank_name = f"{bank_name} ({i})"
                existing_bank = self._en_api.get(ERPNextDocType.BANK, query_bank_name)

                # New name doesnt exist yet, assign as new bank name
                if not existing_bank:
                    new_bank_name = query_bank_name
                    break

                i += 1
            
            # New name found -> create new bank
            if new_bank_name:
                return self._en_api.create(ERPNextDocType.BANK, {"bank_name": new_bank_name, "swift_number": swift_number})
                
                
    def _transform(self) -> dict:
        """Transforms the data from WeClapp to ERPNext.

        Returns:
            dict: Transformed data
        """
        transformed_data = {
            "bank_name"             : self.wc_data.get("creditInstitute", str()),
            "swift_number"          : self.wc_data.get("bankCode", str())
        }
        return transformed_data