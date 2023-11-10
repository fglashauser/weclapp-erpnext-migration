import requests
import config
import erpnext as en
import weclapp as wc
import migration as mig

def migrate_wc_en_customers():
    """Migrate all customers from WeClapp to ERPNext"""
    with mig.MigrationWrapper(wc.WeClappDocType.CUSTOMER, en.ERPNextDocType.CUSTOMER) as migration:
        migration.migrate_all()

def migrate_wc_en_invoices():
    """Migrate all invoices from WeClapp to ERPNext"""
    with mig.MigrationWrapper(wc.WeClappDocType.SALES_INVOICE, en.ERPNextDocType.SALES_INVOICE) as migration:
        migration.migrate_all()

#migrate_wc_en_customers()
#migrate_wc_en_invoices()