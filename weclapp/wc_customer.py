from base.customer_base import CustomerBase

class WeclappCustomer(CustomerBase):
    def __init__(self, weclapp_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weclapp_id = weclapp_id