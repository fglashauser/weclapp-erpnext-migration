from base import DocType

class WeClappDocType(DocType):
    ACCOUNTING_TRANSACTION = "accountingTransaction"
    ARTICLE = "article"
    ARTICLE_ACCOUNTING_CODE = "articleAccountingCode"
    ARTICLE_CATEGORY = "articleCategory"
    ARTICLE_ITEM_GROUP = "articleItemGroup"
    ARTICLE_PRICE = "articlePrice"
    ARTICLE_RATING = "articleRating"
    ARTICLE_STATUS = "articleStatus"
    ARTICLE_SUPPLY_SOURCE = "articleSupplySource"
    ATTENDANCE = "attendance"
    BANK_ACCOUNT = "bankAccount"
    BATCH_NUMBER = "batchNumber"
    BLANKET_PURCHASE_ORDER = "blanketPurchaseOrder"
    CALENDAR = "calendar"
    CALENDAR_EVENT = "calendarEvent"
    CAMPAIGN = "campaign"
    CAMPAIGN_PARTICIPANT = "campaignParticipant"
    CASH_ACCOUNT = "cashAccount"
    #COMMENT = "comment"                                         # TODO: get linked comments
    COMMERCIAL_LANGUAGE = "commercialLanguage"
    COMPANY_SIZE = "companySize"
    CONTACT = "contact"
    CONTRACT = "contract"
    CONTRACT_AUTHORIZATION_UNIT = "contractAuthorizationUnit"
    CONTRACT_BILLING_GROUP = "contractBillingGroup"
    CONTRACT_TERMINATION_REASON = "contractTerminationReason"
    COST_CENTER = "costCenter"
    COST_CENTER_GROUP = "costCenterGroup"
    COST_TYPE = "costType"
    CRM_CALL_CATEGORY = "crmCallCategory"
    CRM_EVENT = "crmEvent"
    CRM_EVENT_CATEGORY = "crmEventCategory"
    CURRENCY = "currency"
    CUSTOM_ATTRIBUTE_DEFINITION = "customAttributeDefinition"
    CUSTOMER = "customer"
    CUSTOMER_CATEGORY = "customerCategory"
    CUSTOMER_LEAD_LOSS_REASON = "customerLeadLossReason"
    CUSTOMER_TOPIC = "customerTopic"
    CUSTOMS_TARIFF_NUMBER = "customsTariffNumber"
    EXTERNAL_CONNECTION = "externalConnection"
    FINANCIAL_YEAR = "financialYear"
    FULFILLMENT_PROVIDER = "fulfillmentProvider"
    INCOMING_GOODS = "incomingGoods"
    INTERNAL_TRANSPORT_REFERENCE = "internalTransportReference"
    LEAD = "lead"
    LEAD_RATING = "leadRating"
    LEAD_SOURCE = "leadSource"
    LEDGER_ACCOUNT = "ledgerAccount"
    LEGAL_FORM = "legalForm"
    LOADING_EQUIPMENT_IDENTIFIER = "loadingEquipmentIdentifier"
    MANUFACTURER = "manufacturer"
    NOTIFICATION = "notification"
    OPPORTUNITY = "opportunity"
    OPPORTUNITY_TOPIC = "opportunityTopic"
    OPPORTUNITY_WIN_LOSS_REASON = "opportunityWinLossReason"
    PARTY = "party"
    PARTY_RATING = "partyRating"
    PAYMENT_METHOD = "paymentMethod"
    PAYMENT_RUN = "paymentRun"
    PAYMENT_RUN_ITEM = "paymentRunItem"
    PERSON_DEPARTMENT = "personDepartment"
    PERSON_ROLE = "personRole"
    PERSONAL_ACCOUNTING_CODE = "personalAccountingCode"
    PICK = "pick"
    PICK_CHECK_REASON = "pickCheckReason"
    PLACE_OF_SERVICE = "placeOfService"
    PRODUCTION_ORDER = "productionOrder"
    PRODUCTION_WORK_SCHEDULE = "productionWorkSchedule"
    PRODUCTION_WORK_SCHEDULE_ASSIGNMENT = "productionWorkScheduleAssignment"
    PURCHASE_INVOICE = "purchaseInvoice"
    PURCHASE_OPEN_ITEM = "purchaseOpenItem"
    PURCHASE_ORDER = "purchaseOrder"
    PURCHASE_ORDER_REQUEST = "purchaseOrderRequest"
    QUOTATION = "quotation"
    REMOTE_PRINT_JOB = "remotePrintJob"
    SALES_INVOICE = "salesInvoice"
    SALES_OPEN_ITEM = "salesOpenItem"
    SALES_ORDER = "salesOrder"
    SALES_STAGE = "salesStage"
    SECTOR = "sector"
    SEPA_DIRECT_DEBIT_MANDATE = "sepaDirectDebitMandate"
    SERIAL_NUMBER = "serialNumber"
    SHELF = "shelf"
    SHIPMENT = "shipment"
    SHIPMENT_METHOD = "shipmentMethod"
    SHIPMENT_RETURN_ASSESSMENT = "shipmentReturnAssessment"
    SHIPMENT_RETURN_ERROR = "shipmentReturnError"
    SHIPMENT_RETURN_REASON = "shipmentReturnReason"
    SHIPMENT_RETURN_RECTIFICATION = "shipmentReturnRectification"
    SHIPPING_CARRIER = "shippingCarrier"
    STORAGE_LOCATION = "storageLocation"
    STORAGE_PLACE = "storagePlace"
    STORAGE_PLACE_BLOCKING_REASON = "storagePlaceBlockingReason"
    STORAGE_PLACE_SIZE = "storagePlaceSize"
    SUPPLIER = "supplier"
    TAG = "tag"
    TAX = "tax"
    TAX_DETERMINATION_RULE = "taxDeterminationRule"
    TERM_OF_PAYMENT = "termOfPayment"
    TICKET = "ticket"
    TICKET_ASSIGNMENT_RULE = "ticketAssignmentRule"
    TICKET_CATEGORY = "ticketCategory"
    TICKET_CHANNEL = "ticketChannel"
    TICKET_FAQ = "ticketFaq"
    TICKET_SERVICE_LEVEL_AGREEMENT = "ticketServiceLevelAgreement"
    TICKET_STATUS = "ticketStatus"
    TICKET_TYPE = "ticketType"
    TITLE = "title"
    TRANSLATION = "translation"
    TRANSPORTATION_ORDER = "transportationOrder"
    UNIT = "unit"
    USER = "user"
    VARIANT_ARTICLE = "variantArticle"
    VARIANT_ARTICLE_ATTRIBUTE = "variantArticleAttribute"
    VARIANT_ARTICLE_VARIANT = "variantArticleVariant"
    WAREHOUSE = "warehouse"
    WAREHOUSE_STOCK = "warehouseStock"
    WAREHOUSE_STOCK_MOVEMENT = "warehouseStockMovement"
    WEBHOOK = "webhook"
    WECLAPP_OS = "weclappOs"