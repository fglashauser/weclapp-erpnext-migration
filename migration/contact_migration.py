from .base_migration import BaseMigration
from erpnext import ERPNextAPI, ERPNextHelper, ERPNextDocType

class ContactMigration(BaseMigration):
    """Migration wrapper for address objects from WeClapp to ERPNext.
    """

    def __init__(self, en_api: ERPNextAPI, wc_data: dict, wc_customer_data: dict = None):
        """Initializes the contact migration.

        Args:
            en_api (ERPNextAPI): ERPNext-API-Object
            wc_data (dict): WeClapp-API-Object
            wc_customer_data (dict, optional): WeClapp-API-Object of the customer (parent). Defaults to None.
        """
        super().__init__(en_api, wc_data)
        self.wc_customer_data = wc_customer_data
        if self.wc_customer_data:
            self._is_primary = self.wc_customer_data.get("primaryContactId", False) == \
                self.wc_data.get("id", None)
    
    def get_doctype(self) -> ERPNextDocType:
        return ERPNextDocType.CONTACT

    def validate(self) -> bool:
        """
        Validates the given data.

        Returns:
            bool: True if valid, False if not
        """
        return self.wc_data.get("firstName", None) and \
            self.wc_data.get("lastName", None)

    def _transform(self) -> dict:
        """Transforms the data from WeClapp to ERPNext.

        Returns:
            dict: Transformed data
        """
        transformed_data = {
            "first_name"            : self.wc_data.get("firstName", str()),
            "last_name"             : self.wc_data.get("lastName", str()),
            "is_primary_contact"    : self.is_primary(),
            "status"                : "Passive",
            "email_ids"             : self._map_emails(),
            "phone_nos"             : self._map_phone_nos()
        }
        return transformed_data
    
    def _map_emails(self) -> list:
        """Maps the email addresses from WeClapp to ERPNext.

        Returns:
            list: List of email addresses
        """
        emails = list()
        if self.wc_data.get("email", None):
            emails.append({
                "email_id"  : self.wc_data.get("email", str()),
                "is_primary": True
            })
        return emails
    
    def _map_phone_nos(self) -> list:
        """Maps the phone numbers from WeClapp to ERPNext.

        Returns:
            list: List of phone numbers
        """
        phone_nos = list()

        # Office number
        phone_no = ERPNextHelper.standardize_phone_number(self.wc_data.get("phone", str()))
        if phone_no:
            phone_nos.append({
                "phone"             : phone_no,
                "is_primary_phone"  : True
            })

        # Mobile number
        mobile_no = ERPNextHelper.standardize_phone_number(self.wc_data.get("mobilePhone1", str()))
        if mobile_no:
            phone_nos.append({
                "phone"                 : mobile_no,
                "is_primary_mobile_no"  : True
            })

        return phone_nos