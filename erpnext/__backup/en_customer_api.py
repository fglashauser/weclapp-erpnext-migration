import config
import requests
from requests.auth import HTTPBasicAuth

class ERPNextCustomerAPI:
    BASE_URL = f"{config.EN_API_BASE}Customer"

    def __init__(self):
        self.auth = HTTPBasicAuth(config.EN_API_KEY, config.EN_API_SECRET)
        self.headers = {"Content-Type": "application/json"}

    def get_customers(self) -> dict:
        response = requests.get(self.BASE_URL, auth=self.auth, headers=self.headers)
        return response.json()

    def create_customer(self, data) -> dict:
        response = requests.post(self.BASE_URL, json=data, auth=self.auth, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Customer {data['customer_name']} not created\n{response.text}")

    def update_customer(self, customer_name, data) -> dict:
        url = f"{self.BASE_URL}/{customer_name}"
        response = requests.put(url, json=data, auth=self.auth, headers=self.headers)
        return response.json()

    def delete_customer(self, customer_name) -> dict:
        url = f"{self.BASE_URL}/{customer_name}"
        response = requests.delete(url, auth=self.auth, headers=self.headers)
        return response.json()
    
    def get_customer(self, customer_name) -> dict:
        url = f"{self.BASE_URL}/{customer_name}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        return response.json()
    
    def get_territory(self, country : str) -> str:
        """Returns the ERPnext territory by a string"""
        return 'Germany' if str.lower(country) in ['germany', 'german', 'ger', 'deutschland', 'de'] \
            else country