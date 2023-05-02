import config
import requests

class WCCustomerAPI:
    BASE_URL                = f"{config.WC_API_BASE}"
    BASE_URL_CUSTOMER       = f"{BASE_URL}customer"
    BASE_URL_SEPA_MANDATES  = f"{BASE_URL}sepaDirectDebitMandate"

    def __init__(self):
        self.headers = {
            "AuthenticationToken": config.WC_API_TOKEN,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Language": "de",
        }

    def get_customers(self):
        response = requests.get(self.BASE_URL_CUSTOMER, headers=self.headers)
        return response.json()

    def create_customer(self, data):
        response = requests.post(self.BASE_URL_CUSTOMER, json=data, headers=self.headers)
        return response.json()

    def update_customer(self, customer_id, data):
        url = f"{self.BASE_URL_CUSTOMER}/id/{customer_id}"
        response = requests.put(url, json=data, headers=self.headers)
        return response.json()

    def delete_customer(self, customer_id):
        url = f"{self.BASE_URL_CUSTOMER}/id/{customer_id}"
        response = requests.delete(url, headers=self.headers)
        return response.status_code

    def get_customer(self, customer_id):
        url = f"{self.BASE_URL_CUSTOMER}/id/{customer_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_customer_count(self):
        url = f"{self.BASE_URL_CUSTOMER}/count"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_customer_sepa_mandates(self, bank_account_id):
        response = requests.get(self.BASE_URL_SEPA_MANDATES, \
                                headers=self.headers, \
                                params={
                                    "partyBankAccountId-eq": bank_account_id
                                })
        return response.json()