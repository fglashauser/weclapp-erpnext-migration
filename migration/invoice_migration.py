from .base_migration import BaseMigration
from erpnext import ERPNextAPI, ERPNextDocType, ERPNextHelper, TaxInfo
from weclapp import WeClappAPI, WeClappDocType
from datetime import datetime
import config
from pathlib import Path

class InvoiceMigration(BaseMigration):
    
    WC_EN_TAX_MAPPPING = {
        "2691"  : TaxInfo("4400 - Erlöse 19 % USt - pcg", "3806 - Umsatzsteuer 19 % - pcg", "Umsatzsteuer 19 %", 19.0),
        "2699"  : TaxInfo("4400 - Erlöse 19 % USt - pcg", "3806 - Umsatzsteuer 19 % - pcg", "Umsatzsteuer 16 % (Q3/4 2020)", 16.0),
        "2680"  : TaxInfo("4125 - Steuerfreie Innergemeinschaftliche Lieferungen § 4 Nr. 1b UStG - pcg", None, None, 0.0),
        "179484": TaxInfo("4125 - Steuerfreie Innergemeinschaftliche Lieferungen § 4 Nr. 1b UStG - pcg", None, None, 0.0)
    }

    def __init__(self, en_api: ERPNextAPI, wc_data: dict):
        """Initializes the migration wrapper.

        Args:
            en_api (ERPNextAPI): ERPNext-API-Object
            wc_data (dict): WeClapp-API-Object
        """
        super().__init__(en_api, wc_data)
        self.taxes = {}

    def get_doctype(self) -> ERPNextDocType:
        return ERPNextDocType.SALES_INVOICE
    
    def get_wc_doctype(self) -> WeClappDocType:
        return WeClappDocType.SALES_INVOICE
    
    def validate(self) -> bool:
        """
        Validates the given data.

        Returns:
            bool: True if valid, False if not
        """
        if float(self.wc_data.get("netAmount", 0)) <= 0.0:
            return False
        
        return True

    def _transform(self) -> dict:
        """Transforms the data from WeClapp to ERPNext.

        Returns:
            dict: Transformed data
        """
        return {
            "name"              : f"RE-{self.wc_data.get('invoiceNumber', str())}",
            "docstatus"         : config.EN_DEFAULT_INVOICE_STATE,
            "set_posting_time"  : 1,
            "posting_date"      : self._map_invoice_date(),
            "due_date"          : self._map_due_date(),
            "customer"          : self.wc_data.get("customerNumber", str()),
            "title"             : self.wc_data.get("commission", str()),
            "payment_schedule"  : self._map_payment_schedule() if not self._is_credit_note() else None,
            "taxes_and_charges" : config.EN_DEFAULT_TAXES_AND_CHARGES,
            "items"             : self._map_items(),
            "taxes"             : self._map_taxes(),
            "is_return"         : self._is_credit_note()
        }
    
    def migrate(self) -> dict:
        """Migrates a given WeClapp-Object and creates it in ERPNext.

        Returns:
            dict: Created ERPNext-Object
        """
        # Base data
        en_data = self._transform()

        # Create customer in ERPNext (if not anonymous customer)
        if self.validate():
            en_invoice = self._en_api.create(ERPNextDocType.SALES_INVOICE, en_data)

            try:
                # After validation (is gross amount correct?)
                self._post_validation(en_invoice)
            except Exception as e:
                print(e)

            # Upload WeClapp documents
            self.upload_weclapp_documents(en_invoice.get("name", str()))

            # Create payment if invoice is paid
            self._create_payment(en_invoice)

            return en_invoice
        else:
            return None
        
    def _is_credit_note(self) -> bool:
        """Checks if the invoice is a credit note.

        Returns:
            bool: True if credit note, False if not
        """
        return self.wc_data.get("salesInvoiceType", str()) == "CREDIT_NOTE"

    def _map_payment_schedule(self) -> list[dict]:
        """Maps the payment schedule from WeClapp to ERPNext.

        Returns:
            list[dict]: Mapped payment schedule
        """
        return [{
                "docstatus"         : config.EN_DEFAULT_INVOICE_STATE,
                "due_date"          : self._map_due_date(),
                "invoice_portion"   : 100.0,
                "payment_term"      : self._map_payment_term()
        }]

    def _map_payment_term(self) -> str:
        """Maps the payment term from WeClapp to ERPNext.
        Uses default Payment term in config if not term is given.
        """
        term = self.wc_data.get("termOfPaymentName", None)
        return term if term else config.EN_DEFAULT_PAYMENT_TERM

    def _add_tax(self, wc_id: str, en_item: dict) -> None:
        """Adds the given ERPNext-Item to the tax with the given WeClapp-Tax-ID.
        
        Args:
            wc_id (str): WeClapp tax ID
            en_item (dict): ERPNext item
        """
        # Get tax info by WeClapp tax ID from mapping in config-file
        tax_info = self.WC_EN_TAX_MAPPPING.get(wc_id, None)
        if tax_info:
            tax = self.taxes.get(wc_id, None)

            # Add item to existing tax-type
            if tax:
                self.taxes[wc_id].append(en_item)

            # Create new tax-type with item
            else:
                self.taxes[wc_id] = [en_item]

    
    def _map_items(self) -> list[dict]:
        """Maps the items from WeClapp to ERPNext.

        Returns:
            list[dict]: Mapped items
        """
        en_items = list()
        for item in self.wc_data.get("salesInvoiceItems", list()):
            tax_info = self.WC_EN_TAX_MAPPPING.get(item.get("taxId", str()), None)
            en_item = {
                "docstatus"             : config.EN_DEFAULT_INVOICE_STATE,
                "item_name"             : self._map_item_title(item),
                "description"           : self._map_item_description(item),
                "price_list_rate"       : item.get("unitPrice", 0),                # Not discounted price (list price)
                "discount_percentage"   : item.get("discountPercentage", 0),
                "qty"                   : self._map_item_quantity(item),
                "uom"                   : self._map_item_uom(item),
                "cost_center"           : config.EN_DEFAULT_COST_CENTER,
                "income_account"        : tax_info.income_account if tax_info else None
            }
            en_items.append(en_item)
            self._add_tax(item.get("taxId", str()), en_item)
        return en_items

    def _map_item_quantity(self, item: dict) -> str:
        """Maps the item quantity.
        """
        quantity = item.get("quantity", 0)

        # Reverse Quantity if credit note
        if self._is_credit_note():
            quantity = quantity * -1

        return quantity

    def _map_item_uom(self, item: dict) -> str:
        """Maps the unit of measurement of the invoice item.
        """
        uom = item.get("unitName", None)

        # Convert "Stk." to "Stk"
        if uom and uom == "Stk.":
            uom = "Stk"

        return uom if uom else config.EN_DEFAULT_UOM

    def _map_item_title(self, item: dict) -> str:
        """Maps the title of the invoice.
        """
        title = item.get("title", None)
        # Limit title to 140 characters
        if title and len(title) > 140:
            title = title[:140]
        return title if title else "(Kein Titel)"
    
    def _map_item_description(self, item: dict) -> str:
        """Maps the invoice description.
        Returns the title if no description is given.
        """
        description = item.get("description", None)
        return description if description else self._map_item_title(item)

    def _map_invoice_date(self) -> str:
        """Maps the invoice date of the invoice.
        If invoice date is empty, return current date.
        """
        inv_date = self.wc_data.get("invoiceDate", None)
        if inv_date and isinstance(inv_date, int) and inv_date > 0:
            return ERPNextHelper.get_date_from_weclapp_ts(inv_date)
        else:
            return datetime.now().strftime("%Y-%m-%d")

    def _map_due_date(self) -> str:
        """Maps the due date of the invoice.
        If no due date is given, return the invoice date.
        """
        due_date = self.wc_data.get("dueDate", None)
        if due_date and isinstance(due_date, int) and due_date > 0:
            return ERPNextHelper.get_date_from_weclapp_ts(due_date)
        else:
            return self._map_invoice_date()

    def _map_taxes(self) -> list[dict]:
        """Maps the taxes from WeClapp to ERPNext.

        Returns:
            list[dict]: Mapped taxes
        """
        en_taxes = list()
        for tax_id, items in self.taxes.items():
            tax_info = self.WC_EN_TAX_MAPPPING.get(tax_id, None)
            if tax_info and tax_info.tax_account:
                en_tax = {
                    "docstatus"     : config.EN_DEFAULT_INVOICE_STATE,
                    "charge_type"   : "On Net Total",
                    "account_head"  : tax_info.tax_account,
                    "description"   : tax_info.description,
                    "rate"          : tax_info.tax_rate,
                    "cost_center"   : config.EN_DEFAULT_COST_CENTER
                }
                en_taxes.append(en_tax)
        return en_taxes
    
    def _post_validation(self, en_invoice: dict):
        """Validates the invoice after creation.

        Args:
            en_invoice (dict): Created ERPNext invoice
        """
        # Check if gross amount is correct
        en_total = en_invoice.get("grand_total", None)
        wc_total = self.wc_data.get("grossAmount", None)

        if en_total and wc_total:
            en_total = float(en_total)
            wc_total = float(wc_total)

            # If credit note, reverse gross amount
            if self._is_credit_note():
                wc_total = wc_total * -1
            
            if en_total != wc_total:
                raise Exception(f"Gross amount of invoice {en_invoice.get('name', str())} is not correct! (ERPNext: {en_total}, WeClapp: {wc_total})")

    def _create_payment(self, en_invoice: dict):
        """Creates a payment for the given invoice.
        Uses the cash account and the invoice date as pay-date.
        Checks the payment status of the invoice first and ignores credit notes.

        Args:
            en_invoice (dict): Created ERPNext invoice
        """
        # Check if no credit note
        if self._is_credit_note():
            return
        
        # Check if invoice is paid
        if self.wc_data.get("paymentStatus", str()) != "PAID":
            return

        if en_invoice.get("grand_total", 0.0) <= 0.0:
            return

        # Create payment
        data = {
            "docstatus"                 : config.EN_DEFAULT_INVOICE_STATE,                     
            "payment_type"              : "Receive",          
            "posting_date"              : en_invoice.get("posting_date", str()),       
            "mode_of_payment"           : config.EN_INVOICE_MODE_OF_PAYMENT,
            "party_type"                : ERPNextDocType.CUSTOMER.value,
            "party"                     : en_invoice.get("customer", str()),
            "party_name"                : en_invoice.get("customer_name", str()),
            "paid_from"                 : config.EN_INVOICE_PAID_FROM_ACCOUNT,
            "paid_from_account_type"    : "Receivable",
            "paid_from_account_currency": config.EN_DEFAULT_CURRENCY,
            "paid_to"                   : config.EN_INVOICE_PAID_TO_ACCOUNT,
            "paid_to_account_type"      : config.EN_INVOICE_PAID_TO_ACCOUNT_TYPE,
            "paid_to_account_currency"  : config.EN_DEFAULT_CURRENCY,
            "paid_amount"               : en_invoice.get("grand_total", 0),
            "received_amount"           : en_invoice.get("grand_total", 0),
            "references": [
                {
                    "docstatus"         : config.EN_DEFAULT_INVOICE_STATE,
                    "reference_doctype" : ERPNextDocType.SALES_INVOICE.value,
                    "reference_name"    : en_invoice.get("name", str()),
                    "total_amount"      : en_invoice.get("grand_total", 0),
                    "allocated_amount"  : en_invoice.get("grand_total", 0)
                }
            ]
        }
        self._en_api.create(ERPNextDocType.PAYMENT_ENTRY, data)