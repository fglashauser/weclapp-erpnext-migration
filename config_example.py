# WeClapp REST-API
WC_API_BASE                 = "https://your-tenant.weclapp.com/webapp/api/v1/"
WC_API_TOKEN                = "your-api-token"
WC_PAGE_SIZE                = 100       # Amount of entities to fetch per request

# WeClapp Cache DB
WC_CACHE_BASE               = "./weclapp/cache/"
WC_CACHE_DOCUMENTS_BASE     = "./weclapp/cache/documents/"

# ERPNext REST-API
EN_API_BASE                 = "http://erp.localhost:8000/api/"
EN_API_KEY                  = "your-api-key"
EN_API_SECRET               = "your-api-secret"

# ERPNext Country Mapping
EN_COUNTRY_MAP = {
    'germany': 'Germany',
    'german': 'Germany',
    'ger': 'Germany',
    'deutschland': 'Germany',
    'de': 'Germany',
    'united states': 'United States',
    'usa': 'United States',
    'us': 'United States',
    'america': 'United States',
    'united kingdom': 'United Kingdom',
    'uk': 'United Kingdom',
    'gb': 'United Kingdom',
    'great britain': 'United Kingdom',
    'england': 'United Kingdom',
    'france': 'France',
    'french': 'France',
    'fr': 'France',
    'italy': 'Italy',
    'italian': 'Italy',
    'it': 'Italy',
    'spain': 'Spain',
    'spanish': 'Spain',
    'es': 'Spain',
    'netherlands': 'Netherlands',
    'dutch': 'Netherlands',
    'nl': 'Netherlands',
    'holland': 'Netherlands',
}

# ERPNext Settings
EN_DEFAULT_INVOICE_STATE        = 1                             # 0 = DRAFT, 1 = SUBMITTED, 2 = CANCELLED
EN_DEFAULT_CURRENCY             = "EUR"                         # Default currency for invoices (must exist in ERPNext)
EN_DEFAULT_PHONE_COUNTRY_CODE   = "49"                          # Default country code for phone numbers without leading +
EN_BANK_ACCOUNT_TYPE            = "Kunden-Bankkonto"            # Bank account type for customers (must exist in ERPNext)
EN_DEFAULT_PAYMENT_TERM         = "net sofort"                  # Default payment term for invoices (must exist in ERPNext)
EN_DEFAULT_UOM                  = "Stk"                         # Default UOM for items (must exist in ERPNext)
EN_DEFAULT_COST_CENTER          = "Haupt - pcg"                 # Default cost center for invoices (must exist in ERPNext)
EN_INVOICE_MODE_OF_PAYMENT      = "Bargeld"                     # Default mode of payment for invoices (must exist in ERPNext)
EN_INVOICE_PAID_TO_ACCOUNT_TYPE = "Cash"                        # Default account type for paid invoices (must exist in ERPNext)
EN_DEFAULT_TAXES_AND_CHARGES    = "Lieferung oder sonstige Leistung im Inland - pcg"        # Default taxes and charges for invoices (must exist in ERPNext)
EN_INVOICE_PAID_FROM_ACCOUNT    = "3250 - Erhaltene Anz. auf Bestellungen (Verb.) - pcg"    # Default account for paid invoices (must exist in ERPNext)
EN_INVOICE_PAID_TO_ACCOUNT      = "1620 - Nebenkasse 2 - pcg"                               # Default account for paid invoices (must exist in ERPNext)