###############################################################################
# This file is intended to be imported by the accounting program
# in the event that no database is found.

###############################################################################
### Information Database Structure
CREATE TABLE Business
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        name TEXT NOT NULL,
        address1 TEXT,
        address2 TEXT,
        state TEXT,
        city TEXT,
        zip TEXT,
        email_address TEXT,
        phone_number TEXT,
        web_site TEXT,
        description TEXT,
        terms TEXT,
        returns TEXT,
        warranty TEXT,
        country TEXT,
        logo BLOB,
        slogan TEXT);

###############################################################################
### Vendor Database Structure
CREATE TABLE Vendor
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        date_created TEXT,
        name TEXT NOT NULL,
        description TEXT,
        notes TEXT,
        email_address TEXT,
        email_status_ID INTEGER,
        phone_number TEXT,
        phone_status_ID INTEGER,
        web_site TEXT);

###############################################################################
### Customer Database Structure
CREATE TABLE Customer
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        date_created TEXT,
        name TEXT NOT NULL,
        address1 TEXT,
        address2 TEXT,
        state TEXT,
        city TEXT,
        zip TEXT,
        email_address TEXT,
        email_status_ID INTEGER,
        phone_number TEXT,
        phone_status_ID INTEGER,
        web_site TEXT,
        description TEXT,
        notes TEXT,
        country_ID INTEGER,
        class_ID INTEGER NOT NULL);

CREATE TABLE Country
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        abbreviation TEXT NOT NULL);
# Static data: ('United States', 'USA')

CREATE TABLE PhoneStatus
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);
# Static data: primary, secondary, inactive, other

CREATE TABLE EmailStatus
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);
# Static data: primary, secondary, inactive, other

CREATE TABLE ContactClass
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);
# Static data: retail, wholesale, gratis, other


###############################################################################
### Inventory Database Structure

CREATE TABLE InventoryItem
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_num INTEGER NOT NULL,
        # date_added REAL NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        notes TEXT,
        num_stock INTEGER NOT NULL,
        retail REAL NOT NULL,
        wholesale REAL NOT NULL);

###############################################################################
### Accounting Module Database Structure

CREATE TABLE Account
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        type_ID INTEGER NOT NULL,
        notes TEXT,
        total REAL NOT NULL);

CREATE TABLE AccountTypes
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);
# Static data: credit, debit, other

###############################################################################
### Account Transactions

CREATE TABLE TransactionType
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        notes TEXT);
# Initial data: transactions listed above

# These rows are semi-static and are used to automate the movement of funds
# from one account to another. These records tell the transaction instance
# what to do.
CREATE TABLE TransactionSequence
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        notes TEXT,
        transaction_type_ID INTEGER NOT NULL,
        sequence_number INTEGER NOT NULL,
        raw_import_column TEXT,
        to_account_ID INTEGER NOT NULL,
        from_account_ID INTEGER NOT NULL);
# Initial data: steps for transaction types listed above.

# A line in this table is created for every movement of funds from one account to another.
CREATE TABLE TransactionInstance
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        description TEXT,
        notes TEXT,
        raw_import_ID INTEGER,
        gross REAL NOT NULL,
        contact_ID INTEGER NOT NULL,
        transaction_type_ID INTEGER NOT NULL,
        transaction_seq_ID INTEGER NOT NULL);

# This table is used when expenses or contacts are imported from PayPal. A
# transaction instance is created when the expense is categorized.
CREATE TABLE ImportRecord
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        contact_ID INTEGER,
        transaction_id TEXT NOT NULL, # UUID from PayPal
        gross REAL NOT NULL,
        shipping REAL,
        fee REAL,
        tax REAL,
        import_type_ID INTEGER NOT NULL);

CREATE TABLE ImportRecordType
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);
# Static data 'credit', 'debit'

#  This table is used to record the fact of a sale. When a sale is made, this
# is created and then when the order is shipped, this is marked as such. This
# is used to allow us to track orders that have not shipped yet.
CREATE TABLE SaleRecord
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        customer_ID INTEGER NOT NULL,
        raw_import_ID INTEGER,
        status_ID INTEGER NOT NULL);

# This table connects what was sold to the sale record, many to one.
CREATE TABLE ProductList
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_record_ID INTEGER NOT NULL,
        inventory_ID INTEGER NOT NULL);

CREATE TABLE SaleStatus
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);
# Static data: active, paid, ready, shipped, complete, trouble, canceled

# This table is used to record the fact of a purchase. When a purchse is made,
# a row is created and made ready to select whether it is a COGS expense or not.;
CREATE TABLE PurchaseRecord
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        raw_import_ID INTEGER,
        vendor_ID INTEGER NOT NULL,
        status_ID INTEGER NOT NULL,
        type_ID INTEGER,
        gross REAL NOT NULL);

CREATE TABLE PurchaseType
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);
# Static data: cogs, other, unknown

CREATE TABLE PurchaseStatus
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);
# Static data: paid, shipped, backorder, arrived, other

###############################################################################
### Raw import table
CREATE TABLE RawImport
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Time TEXT,
        TimeZone TEXT,
        Name TEXT,
        Type TEXT,
        Status TEXT,
        Currency TEXT,
        Gross TEXT,
        Fee TEXT,
        Net TEXT,
        FromEmail TEXT,
        ToEmail TEXT,
        TransactionID TEXT,
        ShippingAddress TEXT,
        AddressStatus TEXT,
        ItemTitle TEXT,
        ItemID TEXT,
        Shipping TEXT,
        InsuranceAmount TEXT,
        SalesTax TEXT,
        Option1Name TEXT,
        Option1Value TEXT,
        Option2Name TEXT,
        Option2Value TEXT,
        ReferenceTxnID TEXT,
        InvoiceNumber TEXT,
        CustomNumber TEXT,
        Quantity TEXT,
        ReceiptID TEXT,
        Balance TEXT,
        AddressLine1 TEXT,
        AddressLine2 TEXT,
        City TEXT,
        State TEXT,
        PostalCode TEXT,
        Country TEXT,
        Phone TEXT,
        Subject TEXT,
        Note TEXT,
        CountryCode TEXT,
        BalanceImpact TEXT,
        Completed INTEGER);

CREATE TABLE RawImportNames
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);

###############################################################################
### Table for any random thing that doesn't fit somewhere else.
CREATE TABLE Config
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        last_contact_ID INTEGER);

###############################################################################
### This table links paypal transaction IDs to customers or vendors
CREATE TABLE TransactionID
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id TEXT NOT NULL,
        customer_ID INTEGER, # One of these will be NULL
        vendor_ID INTEGER);

