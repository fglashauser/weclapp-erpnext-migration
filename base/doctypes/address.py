from .address_type import AddressType
from .doctype_base import DocTypeBase

class Address(DocTypeBase):
    def __init__(self, type : AddressType, street : str, zip : str, \
                 city : str, country : str):
        super.__init__()
        self.type       = type
        self.street     = street
        self.zip        = zip
        self.city       = city
        self.country    = country