from .contact_type import ContactType
from .gender import Gender
from .doctype_base import DocTypeBase

class Contact(DocTypeBase):
    def __init__(self, type : ContactType, gender : Gender, first_name : str, \
                last_name : str, phone : str, mobile : str, email : str, \
                position : str):
        super.__init__()
        self.type       = type
        self.gender     = gender
        self.first_name = first_name
        self.last_name  = last_name
        self.phone      = phone
        self.mobile     = mobile
        self.email      = email
        self.position   = position