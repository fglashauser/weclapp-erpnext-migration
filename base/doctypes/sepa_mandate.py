from .bank_account import BankAccount
from .sepa_mandate_frequency import SepaMandateFrequency
from .sepa_mandate_type import SepaMandateType
from datetime import date
from .doctype_base import DocTypeBase

class SepaMandate(DocTypeBase):
    def __init__(self, reference : str, name : str, frequency : SepaMandateFrequency, \
                 type : SepaMandateType, signature_date : date, bank_account : BankAccount):
        super.__init__()
        self.reference      = reference
        self.name           = name
        self.frequency      = frequency
        self.type           = type
        self.signature_date = signature_date
        self.bank_account   = bank_account