import config
import requests
from requests.auth import HTTPBasicAuth

class ERPNextAddressAPI:
    BASE_URL = f"{config.EN_API_BASE}Address"

    def __init__(self):
        self.auth = HTTPBasicAuth(config.EN_API_KEY, config.EN_API_SECRET)
        self.headers = {"Content-Type": "application/json"}

    def get_addresses(self) -> dict:
        response = requests.get(self.BASE_URL, auth=self.auth, headers=self.headers)
        return response.json()

    def create_address(self, data) -> dict:
        response = requests.post(self.BASE_URL, json=data, auth=self.auth, headers=self.headers)
        return response.json()

    def update_address(self, address_name, data) -> dict:
        url = f"{self.BASE_URL}/{address_name}"
        response = requests.put(url, json=data, auth=self.auth, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Address {address_name} not updated\n{response.text}")

    def delete_address(self, address_name) -> dict:
        url = f"{self.BASE_URL}/{address_name}"
        response = requests.delete(url, auth=self.auth, headers=self.headers)
        return response.json()
    
    def get_address(self, address_name) -> dict:
        url = f"{self.BASE_URL}/{address_name}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Address {address_name} not found\n{response.text}")