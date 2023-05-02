import config
import base
import weclapp as wc
import erpnext as en
from datetime import date

class WcEnCustomerMigration:
    def __init__(self):
        self.wc_api = wc.WCCustomerAPI()
        self.en_cust_api = en.ERPNextAPI(config.EN_API_KEY, config.EN_API_SECRET, config.EN_API_BASE, en.ERPNextDocTypes.CUSTOMER)
        self.en_addr_api = en.ERPNextAPI(config.EN_API_KEY, config.EN_API_SECRET, config.EN_API_BASE, en.ERPNextDocTypes.ADDRESS)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.en_cust_api.session.close()
        self.en_addr_api.session.close()

    def migrate_customer_from_weclapp_to_erpnext(self, weclapp_id):
        '''Migrate a customer from WeClapp to ERPNext'''

        wc_customer = self.get_customer_from_weclapp(weclapp_id)
        self.create_erpnext_customer(wc_customer)

    def get_customer_from_weclapp(self, weclapp_id):
        '''Get a customer object from WeClapp API'''

        wc_customer_data = self.wc_api.get_customer(weclapp_id)

        # Ein WeClapp-Kundenobjekt erzeugen
        type = (
            base.CustomerType.PERSON if wc_customer_data["partyType"] == "PERSON"
            else base.CustomerType.COMPANY
        )
        name = (
            wc_customer_data["company"] if type == base.CustomerType.COMPANY
            else f'{wc_customer_data["firstName"]} {wc_customer_data["lastName"]}'
        )
        wc_customer = wc.WeclappCustomer(
            weclapp_id      = wc_customer_data["id"],
            name            = name,
            cust_nr         = wc_customer_data["customerNumber"],
            type            = type,
            name_addition   = wc_customer_data.get("company2", None),
            phone           = wc_customer_data.get("phone", None),
            mobile          = wc_customer_data.get("mobilePhone1", None),
            email           = wc_customer_data.get("email", None),
            website         = wc_customer_data.get("website", None),
            vat_id          = wc_customer_data.get("vatRegistrationNumber", None),
            eori_id         = None # TODO: EORI nicht in wc_customer_data vorhanden
        )

        # Bankverbindungen hinzufügen
        for bank_account in wc_customer_data["bankAccounts"]:
            wc_customer.add_bank_account(base.BankAccount(
                account_holder  = bank_account.get("accountHolder", None),
                bank_name       = bank_account.get("creditInstitute", None),
                iban            = bank_account.get("accountNumber", None),
                bic             = bank_account.get("bankCode", None),
                weclapp_id      = bank_account["id"]
            ))

        # Adressen hinzufügen
        for address in wc_customer_data["addresses"]:
            address_type = (
                base.AddressType.BILLING if address["invoiceAddress"]
                else base.AddressType.DELIVERY if address["deliveryAddress"]
                else None
            )
            wc_customer.add_address(base.Address(
                type        = address_type,
                street      = address.get("street1", None),
                zip         = address.get("zipcode", None),
                city        = address.get("city", None),
                country     = address.get("countryCode", None)
            ))

        # Kontakte hinzufügen
        primary_contact_id = wc_customer_data.get("primaryContactId", None)
        for contact in wc_customer_data["contacts"]:
            type = (
                base.ContactType.PRIMARY if contact["id"] == primary_contact_id
                else None
            )
            gender = (
                base.Gender.MALE if contact.get("salutation", None) == "MR"
                else base.Gender.FEMALE if contact.get("salutation", None) == "MRS"
                else None
            )
            wc_customer.add_contact(base.Contact(
                type        = type,
                gender      = gender,
                first_name  = contact.get("firstName", None),
                last_name   = contact.get("lastName", None),
                phone       = contact.get("phone", None),
                mobile      = contact.get("mobilePhone1", None),
                email       = contact.get("email", None),
                position    = None # TODO: nicht in contact enthalten
            ))

        # SEPA-Mandate hinzufügen
        for bank_account in wc_customer.bank_accounts:
            mandates = self.wc_api.get_customer_sepa_mandates(bank_account.weclapp_id)["result"]
            for mandate in mandates:
                type = (
                    base.SepaMandateType.CORE if mandate['type'] == "CORE"
                    else base.SepaMandateType.B2B if mandate['type'] == "B2B"
                    else None
                )
                frequency = (
                    base.SepaMandateFrequency.ONE_TIME if mandate['runtime'] == "ONE_OFF_MANDATE"
                    else base.SepaMandateFrequency.RECURRING if mandate['runtime'] == "RECURRING_MANDATE"
                    else None
                )
                signature_date = (
                    date.fromtimestamp(mandate["signatureDate"] / 1000)
                    if mandate["signatureDate"] is not None
                    and isinstance(mandate["signatureDate"], int)
                    else None
                )
                wc_customer.add_sepa_mandate(base.SepaMandate(
                    type            = type,
                    frequency       = frequency,
                    signature_date  = signature_date,
                    reference       = mandate.get("mandateReference", None),
                    name            = mandate.get("description", None),
                    bank_account    = bank_account
                ))

        return wc_customer
    
    def create_erpnext_customer(self, customer : base.CustomerBase):
        '''Creates a customer in ERPNext'''

        customer_group = (
            "B2B Small Business" if customer.type == base.CustomerType.COMPANY
            else "Einzelperson" if customer.type == base.CustomerType.PERSON
            else None
        )
        customer_type = (
            "Company" if customer.type == base.CustomerType.COMPANY
            else "Individual" if customer.type == base.CustomerType.PERSON
            else None
        )

        customer_primary_address_name = f"{customer.cust_nr}-Hauptadresse"
        customer_primary_address = en.ERPNextAPIData(en.ERPNextDocTypes.ADDRESS, customer_primary_address_name, True, {
            "address_title": customer_primary_address_name,
            "address_type": "Billing",
            "address_line1": customer.addresses[0].street if customer.addresses else "",
            "city": customer.addresses[0].city if customer.addresses else "",
            "country": en.ERPNextHelper.get_country_string(customer.addresses[0].country) if customer.addresses else "",
            "pincode": customer.addresses[0].zip if customer.addresses else "",
            "email_id": customer.email,
            "phone": customer.phone,
            "is_primary_address": True,
            "is_shipping_address": True
        })

        customer_data = {
            "customer_name": customer.name,
            "customer_group": customer_group,
            "territory": en.ERPNextHelper.get_country_string(customer.addresses[0].country) if customer.addresses else "",
            "customer_type": customer_type,
            "customer_primary_address": customer_primary_address,
            "customer_primary_contact": customer.name,
            "customer_primary_mobile": customer.mobile,
            "customer_primary_website": customer.website,
            "customer_primary_gst_number": customer.vat_id,
            "customer_primary_pan_number": customer.eori_id,
            "customer_primary_bank_name": customer.bank_accounts[0].bank_name if customer.bank_accounts else "",
            "customer_primary_bank_account_number": customer.bank_accounts[0].iban if customer.bank_accounts else "",
            "customer_primary_bank_iban": customer.bank_accounts[0].iban if customer.bank_accounts else "",
            "customer_primary_bank_bic": customer.bank_accounts[0].bic if customer.bank_accounts else "",
            "customer_primary_bank_account_type": "Savings",
            "customer_primary_bank_currency": "EUR"
        }
        
         # Create customer
        try:
            customer_response = self.en_cust_api.create(customer_data)
        except en.ERPNextAPIError as e:
            print(e.message)
            return
        
        # Create link
        try:
            link_response = self.en_cust_api.create_link(en.ERPNextDocTypes.CUSTOMER, customer_response["data"]["name"], \
                                                         en.ERPNextDocTypes.ADDRESS, customer_primary_address_name)
        except Exception as e:
            print(e)
            return