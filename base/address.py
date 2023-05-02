from base.address_type import AddressType

class Address:
    def __init__(self, type : AddressType, street : str, zip : str, \
                 city : str, country : str):
        self.type       = type
        self.street     = street
        self.zip        = zip
        self.city       = city
        self.country    = country