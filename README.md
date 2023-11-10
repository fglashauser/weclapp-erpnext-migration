# WeClapp -> ERPNext Migration

A python project for migrating data from WeClapp ERP-System (https://www.weclapp.com/) to ERPNext Open-Source ERP-System (https://erpnext.com) via the REST-API of both products.

### Important note
The project isn't complete yet and still under development. The chances are high you have to customize it for successful usage.
Feel free to contribute.

## Features
### Cache-Database
Our WeClapp account expired while developing the migration, so I implemented a cache-layer for saving all WeClapp-objects with PysonDB in JSON-Format.

### Migrations to ERPNext
Till now following objects are implemented to migrate to ERPNext:

- Addresses
- Bank Accounts
- Banks
- Contacts
- Customers
- Sales Invoices

Next migrations on roadmap are:
- Quoatations
- Sales Orders
- Contracts
- Sepa Mandates
- Tickets

## Installation
### Configuration
Clone the repository to your local machine:

```bash
git clone https://github.com/fglashauser/weclapp-erpnext-migration
```

Copy the example configuration:
```bash
cd weclapp-erpnext-migration
cp config_example.py config.py
```

Open _**config.py**_ and set the needed REST-API URL's and keys for both WeClapp and ERPNext REST-API.  
For generating a API token in WeClapp, go to ``My settings > API`` and generate one.  
  
In ERPNext get a API-token by generating a API-key and API-secret:
```
1. User list -> Open a user
2. Settings -> API Access section
3. Click on Generate Keys
4. Copy API secret (it won't show again!)
5. Copy API key
```

### Option 1: Open with VS-Code Dev Container (recommended)
Make sure you have docker installed and got VScode Dev-Container extension.  
Open the folder _**weclapp-erpnext-migration**_ in VScode or run from shell:
```
code .
```
Then open command palette and run ``Dev Containers: Reopen in container``

### Option 2: Open locally (Debian-based systems)
Make sure you got the current **Python** and **pip** packages and install the packages in requirements.txt:
```
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
```

## Usage
### 1. Caching WeClapp-Database
First create a local backup of your WeClapp instance by using the built in caching function:
```bash
python3 cache_weclapp.py
```
After that you will have .json-Files of all WeClapp-objects in _**weclapp/cache**_ and PDF documents in _**weclapp/cache/documents**_ for following object-types:
- article
- contact
- contract
- customer
- incomingGoods
- party
- purchaseInvoice
- purchaseOrder
- quotation
- salesInvoice
- salesOrder
- shipment
- ticket

### 2. Migrating to ERPNext
...in development / coming soon, you can look into ``main.py`` to look how to use the migration I realized so far and how to use it.

# Stay tuned!
Since I got a truckload of work to do besides this project it will take some time till this project will be finished.  
Feel free to contribute your ideas and code!

If you want to support my work, I'm really happy about a small donation to get some coffee & beer:
https://paypal.me/pcgiga