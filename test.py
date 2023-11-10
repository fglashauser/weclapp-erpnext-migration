import requests
import config
from weclapp import WeClappAPI, WeClappDocType
from erpnext import ERPNextBackup, ERPNextAPI, ERPNextDocType

def download_document():
    with WeClappAPI(config.WC_API_TOKEN, config.WC_API_BASE) as wc_api:
        for document in wc_api.get_documents(WeClappDocType.CONTRACT, "63972"):
            wc_api.download_document(document["id"], f"./weclapp/cache/documents/{document['name']}")

def create_payment_entry():
    with ERPNextAPI(config.EN_API_KEY, config.EN_API_SECRET, config.EN_API_BASE) as en_api:
        data = {
            "docstatus"                 : 0,                     
            "payment_type"              : "Receive",          
            "posting_date"              : "2020-09-30",       
            "mode_of_payment"           : "Bargeld",
            "party_type"                : "Customer",
            "party"                     : "ANONYMOUS_DEBITOR",
            "party_name"                : "Barverkauf",
            "paid_from"                 : "3250 - Erhaltene Anz. auf Bestellungen (Verb.) - pcg",
            "paid_from_account_type"    : "Receivable",
            "paid_from_account_currency": "EUR",
            "paid_to"                   : "1620 - Nebenkasse 2 - pcg",
            "paid_to_account_type"      : "Cash",
            "paid_to_account_currency"  : "EUR",
            "paid_amount"               : 214.60,
            "received_amount"           : 214.60,
            "reference_no"              : "RE-709",
            "reference_date"            : "2020-09-30",
            "references": [
                {
                    "docstatus"         : 0,
                    "reference_doctype" : "Sales Invoice",
                    "reference_name"    : "RE-709",
                    "total_amount"      : 214.60,
                    "allocated_amount"  : 214.60
                }
            ]
        }
        en_api.create(ERPNextDocType.PAYMENT_ENTRY, data)

#create_payment_entry()

#download_document()
#backup = ERPNextBackup()
#backup.backup()
#backup.restore()