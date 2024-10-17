# crm-be-service

General TODOS:

- acc - deactivation and reactivation path
- em - handle the changing of entity type use case
- acc- account orders api to see from the perspective of the account
- when uuid exists in path and in payload, need validation the two match
- handle the allowed duplication for entity children
- review the sign up flow vs the create sys user service
- validation on product list items
- invoice item may allows for duplicates
- dont let users disable themselves OR delete

The intent of this README is to desrcibe the requirements of this demo application.

## Apps

1. Entity Management (EM)
2. Customer Relationship Management (CRM)
3. Order Management (OM)
4. Portfolio Project Management (PPM)
5. Comptitive Intelligence Management (CIM)
6. Product Management (PM)

### Entity Management (EM)

This is a foundation app. The app includes the following:

1. entity relationships
2. contact and location information

### Oder Management (OM)

1. Accounts
2. Products
3. Price Lists
4. Product restriction per account
5. Orders
6. Invoices
7. Statements
8. Recurring billing

ORDERS

- need an order cancellation path

PRODUCTS

- support disabling, retiring, or archiving a product, thinking validation date range, start, end, allow for null
- support batch operations
- currently supporting get all, need to implement some query params, pagination
