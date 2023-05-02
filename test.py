import requests
import config
import erpnext as en
import weclapp as wc
import migration as mig

en_addr_api = en.ERPNextAPI(config.EN_API_KEY, config.EN_API_SECRET, config.EN_API_BASE, en.ERPNextDocTypes.ADDRESS)
en_cust_api = en.ERPNextAPI(config.EN_API_KEY, config.EN_API_SECRET, config.EN_API_BASE, en.ERPNextDocTypes.CUSTOMER)

def get_customers():
    #customers = api.get_customer('CUST-2023-00001') 
    customers = en_cust_api.get_all()
    
    # output api.get_customers() to file ./test/en_customers.json, format escape characters and newlines
    with open('./test/en_customers.json', 'w') as f:
        for customer in customers["data"]:
            cust_str = str(en_cust_api.get(customer["name"])).replace('\'', '"').replace('\\n', '\r\n')
            f.write(cust_str)
            print(cust_str)
        f.close()

def get_address(name : str, printout : bool) -> dict:
    """Returns a JSON object of an address by name"""
    address = en_addr_api.get(name)
    if printout:
        print(address)
    return address

def create_customer():
    data_address = {
        "address_title": "Standard",
        "address_type": "Billing"
    }

    data = {
        "customer_name": "Beispiel Peter GmbH",
        "customer_group": "B2B Small Business",
        "territory": "Germany",
        "customer_type": "Company",
        "customer_primary_contact": "Peter Beispiel",
        "customer_primary_email": "info@beispiel-gmbh.de",
        "customer_primary_phone": "0123456789",
        "customer_primary_mobile": "0123456789",
        "customer_primary_city": "Teststadt",
        "customer_primary_state": "Testbundesland",
        "customer_primary_country": "Deutschland",
        "customer_primary_pincode": "12345",
        "customer_primary_website": "https://www.beispiel-gmbh.de",
        "customer_primary_gst_number": "DE123456789",
        "customer_primary_pan_number": "DE123456789",
        "customer_primary_bank_name": "Testbank",
        "customer_primary_bank_account_number": "123456789",
        "customer_primary_bank_iban": "DE123456789",
        "customer_primary_bank_bic": "DE123456789",
        "customer_primary_bank_swift_code": "DE123456789",
        "customer_primary_bank_branch": "Testbankfiliale",
        "customer_primary_bank_address": "Testbankstraße 1",
        "customer_primary_bank_city": "Testbankstadt",
        "customer_primary_bank_state": "Testbankbundesland",
        "customer_primary_bank_country": "Deutschland",
        "customer_primary_bank_pincode": "12345",
        "customer_primary_bank_account_type": "Savings",
        "customer_primary_bank_currency": "EUR"
    }
    customer = en_cust_api.create(data)
    print(customer)

def migrate_customer(weclapp_id):
    with mig.WcEnCustomerMigration() as migration:
        migration.migrate_customer_from_weclapp_to_erpnext(weclapp_id)


#get_customers()
#create_customer()

# Kunde: Praxis Carina Seitz (Unternehmen)
migrate_customer("18397")
#result = en_customer_api._request(f"{config.EN_API_BASE}Customer", "GET")
#pass

# Kunde: Anneliese Altmann (Einzelperson)
#migrate_customer("7848")

# seitz bank-konto id: '37138' (partyBankAccountId)
# sepa mandate
#wc_api = WCCustomerAPI()
#fuckit = wc_api.get_customer_sepa_mandates('37138')

# bank-konten für seitz
#bank_accounts = wc_api.get_bank_accounts("18397")

#get_address("Test-Billing", True)
