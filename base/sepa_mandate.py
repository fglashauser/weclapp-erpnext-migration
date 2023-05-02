from base.bank_account import BankAccount
from base.sepa_mandate_frequency import SepaMandateFrequency
from base.sepa_mandate_type import SepaMandateType
from datetime import date

class SepaMandate:
    def __init__(self, reference : str, name : str, frequency : SepaMandateFrequency, \
                 type : SepaMandateType, signature_date : date, bank_account : BankAccount):
        self.reference      = reference
        self.name           = name
        self.frequency      = frequency
        self.type           = type
        self.signature_date = signature_date
        self.bank_account   = bank_account