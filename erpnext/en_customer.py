from base import CustomerBase

class ERPNextCustomer(CustomerBase):
    def __init__(self, erpnext_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.erpnext_id = erpnext_id