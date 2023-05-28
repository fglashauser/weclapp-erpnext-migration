from .doctype_base import DocTypeBase

class BankAccount(DocTypeBase):
    def __init__(self, account_holder, bank_name, iban, bic, weclapp_id):
        super.__init__()
        self.account_holder     = account_holder
        self.bank_name          = bank_name
        self.iban               = iban
        self.bic                = bic
        self.weclapp_id         = weclapp_id