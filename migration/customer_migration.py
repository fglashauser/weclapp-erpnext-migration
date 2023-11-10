from .base_migration import BaseMigration
from .address_migration import AddressMigration
from .contact_migration import ContactMigration
from .bank_account_migration import BankAccountMigration
from erpnext import ERPNextAPI, ERPNextDocType, ERPNextHelper

class CustomerMigration(BaseMigration):
    """Migration wrapper for a customer object from WeClapp to ERPNext.
    """

    def __init__(self, en_api: ERPNextAPI, wc_data: dict):
        """Initializes the migration wrapper.

        Args:
            en_api (ERPNextAPI): ERPNext-API-Object
            wc_data (dict): WeClapp-API-Object
        """
        super().__init__(en_api, wc_data)

    def get_doctype(self) -> ERPNextDocType:
        return ERPNextDocType.CUSTOMER

    def migrate(self) -> dict:
        """Migrates a given WeClapp-Object and creates it in ERPNext.

        Returns:
            dict: Created ERPNext-Object
        """
        # Base data
        en_data = self._transform()

        # Addresses
        en_addresses = list()
        for addr in self.wc_data["addresses"]:
            addr_migration = AddressMigration(self._en_api, addr, self.wc_data)
            if addr_migration.validate():               # Only migrate valid addresses
                en_addr = addr_migration.migrate()      # Migrate address
                en_addresses.append(en_addr)            # Add address to list
                if addr_migration.is_primary():         # Primary address
                    en_data["customer_primary_address"] = en_addr["name"]
                    en_data["territory"] = en_addr["country"]

        # Contacts
        en_contacts = list()
        for contact in self.wc_data["contacts"]:
            contact_migration = ContactMigration(self._en_api, contact, self.wc_data)
            if contact_migration.validate():            # Only migrate valid contacts
                en_contact = contact_migration.migrate()
                en_contacts.append(en_contact)          # Add contact to list
                if contact_migration.is_primary():      # Primary contact
                    en_data["customer_primary_contact"] = en_contact["name"]
        
        # Create customer in ERPNext
        en_customer = self._en_api.create(ERPNextDocType.CUSTOMER, en_data)

        # Link addresses to customer
        self._link_addresses(en_customer, en_addresses)

        # Link contacts to customer
        self._link_contacts(en_customer, en_contacts)

        # Bank Accounts
        for bank_account in self.wc_data["bankAccounts"]:
            bank_account_migration = BankAccountMigration(self._en_api, bank_account, en_customer)
            if bank_account_migration.validate():
                bank_account_migration.migrate()

        return en_customer


    def validate(self) -> bool:
        """
        Validates the given data.

        Returns:
            bool: True if valid, False if not
        """
        return self.wc_data.get("company", None) and \
            self.wc_data.get("partyType", None) and \
            self.wc_data.get("customerNumber", None)

    def _transform(self) -> dict:
        """Transforms the data from WeClapp to ERPNext.

        Returns:
            dict: Transformed data
        """
        transformed_data = {
            "name"                          : self.wc_data.get("customerNumber", None),
            "customer_name"                 : self._map_customer_name(),
            "customer_group"                : self._map_customer_group(),
            "customer_type"                 : self._map_customer_type(),
            "website"                       : self.wc_data.get("website", None),
            "customer_primary_gst_number"   : self.wc_data.get("vatRegistrationNumber", None),
            "phone"                         : ERPNextHelper.standardize_phone_number(self.wc_data.get("phone", str())),
            "email"                         : self.wc_data.get("email", None)
        }

        return transformed_data
    
    def _is_company(self) -> bool:
        """Returns if the given customer is a company (true) or a person (false)
        """
        return not(self.wc_data["partyType"] == "PERSON")
    
    def _map_customer_name(self) -> str:
        """Maps the customer name based on the party type
        """
        return self.wc_data["company"] if self._is_company() \
            else f"{self.wc_data.get('firstName', str())} {self.wc_data.get('lastName', str())}".strip()
        
    def _map_customer_group(self) -> str:
        """Maps the customer group based on the party type
        """
        return "B2B Small Business" if self._is_company() else "Einzelperson"
    
    def _map_customer_type(self) -> str:
        """Maps the customer type
        """
        return "Company" if self._is_company() else "Individual"
    
    def _link_addresses(self, en_customer: dict, en_addresses: list):
        """Links the addresses to the given customer
        """
        for en_addr in en_addresses:
            self._en_api.create_link(ERPNextDocType.CUSTOMER, en_customer["name"], \
                                     ERPNextDocType.ADDRESS, en_addr["name"])
            
    def _link_contacts(self, en_customer: dict, en_contacts: list):
        """Links the contacts to the given customer
        """
        for en_contact in en_contacts:
            self._en_api.create_link(ERPNextDocType.CUSTOMER, en_customer["name"], \
                                     ERPNextDocType.CONTACT, en_contact["name"])