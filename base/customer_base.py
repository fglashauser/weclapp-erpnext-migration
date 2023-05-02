from base.customer_type import CustomerType
from base.address import Address
from base.contact import Contact
from base.bank_account import BankAccount
from base.sepa_mandate import SepaMandate

class CustomerBase:
    # Kunden-Klasse für Migrationen und andere Aufgaben
    def __init__(self, cust_nr : str, type : CustomerType, name : str, \
                name_addition : str, phone : str, mobile : str, email : str, \
                website : str, vat_id : str, eori_id : str):
        self.cust_nr        = cust_nr
        self.type           = type
        self.name           = name
        self.name_addition  = name_addition
        self.phone          = phone
        self.mobile         = mobile
        self.email          = email
        self.website        = website
        self.vat_id         = vat_id
        self.eori_id        = eori_id
        self.addresses      = []
        self.contacts       = []
        self.bank_accounts  = []
        self.sepa_mandates  = []
    
    def add_address(self, address : Address):
        self.addresses.append(address)

    def add_contact(self, contact : Contact):
        self.contacts.append(contact)

    def add_bank_account(self, bank_account : BankAccount):
        self.bank_accounts.append(bank_account)

    def add_sepa_mandate(self, sepa_mandate : SepaMandate):
        self.sepa_mandates.append(sepa_mandate)