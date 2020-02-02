# Accounts and transactions

This is the design document for the business that the software is to
implement, including the data design of the business. The software
implementation is documented elsewhere.

These accounts and transactions are the basic design for the business
procedures. Manufacturing procedures are a different matter altogether
and not discussed here.

The transactions outlined are the only official way to change the values
in the accounts, though, methods are provided to create accounts and
enter values manually.

## Cash Flow

When a sale takes place, the cash account is added to for the gross amount,
then the expenses are tallied with the results added to their respective
accounts. This is handled automatically via the transaction mechanism.

When an expense is incurred, it is added to the Un-categorized account to be
categorized manually. When it is categorized, the correct transaction is
automatically called to distribute the amounts to the correct accounts.

Most transactions are to be imported from PayPal. When a transaction is
imported, the same procedures are implemented in software.

## Assets

* Cash (debit)
  * This is where a customer pays for product. It can be considered to be
    the same as a checking account. The gross amount is entered then the
    expenses are figured out from there.

* Shipping collected (credit)
  * This account has the shipping collected from the cash sale. When the
    shipping is actually payed, then this account is reduced and the expense
    account is incremented. This account will normally have a positive balance.
    When shipping is actually purchased, the amount is sent to the consumables
    account.

## Liabilities

* Taxes collected (credit)
  * This account is a holding account for the cash that is collected for the
    purpose of paying sales tax.

* Materials (debit)
  * These are expenses for things that stay in the product after a sale, such
    as tubing and screws. Things bought that will be sold are inventory.

* Other expense (debit)
  * This is an account that tracks expenses that are not to be applied to the
    COGS liability account.

* Customer shipping payed (debit)
  * This account contains the actual amount payed for shipping product to
    customers.

* Taxes Payed (debit)
  * This is the amount of sales tax that I have payed, including sales tax.

* Bank Fees (debit)
  * This is the PayPal fee for each sale.

## Equity

* OwnerCapital (credit)
  * This account is only used when the books are closed to make the balance
    work.

## Non-Balance Accounts

* Expense Import (none)
  * This is a special table in the database and not an account table like the
    others. Raw purchases are placed here. The purchase is then manually
    categorized to be one of materials, consumables, shipping from vendor,
    shipping to customer, or taxes payed. The transaction is tracked so that
    an individual transaction can be traced back to a specific purchase. This
    account is not a part of the trial balance. The total is not tracked.

* Shipping payed for materials (none)
  * This is shipping payed to receive goods. This is a dangling account used
    only to track the amount. It is not a part of the trial balance.

## Transactions

Some transactions are automated by importing a CSV file from PayPal, but they
can also be created manually. When a transaction is created by importing data,
the transaction records are created, but they are not run as a script as they
would be if the transaction was created manually.

* Sale -- This transaction happen whe the customer buys product from us.
  * Cash account is incremented by the gross amount of the sale.
  * Shipping collected is moved from the cas account to the shipping collected
    account.
  * PayPal fee is deducted and the fees expense is increased.

* Purchase -- This happens when we buy something that we need for the
  business.
  * The raw amount is placed in the Expense Import account. The shipping,
    tax and other components of the purchase are stored for later
    categorizing using transactions.

* Materials -- Categorize a purchase to the COGS expenses.
  * Cash is decreased by the gross amount.
  * Taxes payed in increased.
  * Shipping payed to vendor is increased.

* MiscExpense -- Categorize a purchase to the non-COGS expenses.
  * Cash is decreased by the gross amount.
  * Taxes payed in increased.
  * Shipping payed to vendor is increased.

* ShippingPayed -- When a purchase of shipping is made to ship product to
  customer.
  * Cash is decreased by the gross amount.
  * Shipping payed to customer is increased by the gross amount.

* Owner cash out -- When I buy something that is not business related or
  take cash out.
  * Owner equity is increased by the gross amount.
  * Cash account is decreased by the gross amount.

* Owner cash in -- This is a cash investment from the owner to the business.
  Any cash that is deposited with the company that is not a sale is owner
  cash in.
  * Owner equity is increased.
  * Cash account is increased.

* Manual transaction -- This is a transaction record of a manual transaction
  where the value of a particular account or accounts are changed without any
  sales or purchase transaction.

Sale and purchase transactions must be attributed to a contact.

All secondary transactions, such as attributing shipping collected is stored
in such a way as the transaction can be traced back to a specific sale or
purchase. Each transaction has a unique ID that is included in the record for
all secondary transactions.

## Database tables

The database tables are how the tracking for business actions are implemented.
This section describes the tables in relation to the procedures outlined
above.

### Contacts

The purpose of these tables is to allow one to contact a person in the future
based on previous information.

* Contacts
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * date_created REAL NOT NULL
  * first TEXT NOT NULL
  * last TEXT NOT NULL
  * middle TEXT
  * address1 TEXT NOT NULL
  * address2 TEXT
  * state TEXT NOT NULL
  * city TEXT NOT NULL
  * zip TEXT NOT NULL
  * email_address TEXT
  * email_status_ID INTEGER
  * phone_number TEXT
  * phone_status_ID INTEGER
  * web_site TEXT
  * description TEXT
  * notes TEXT
  * country_ID INTEGER NOT NULL
  * type_ID INTEGER NOT NULL
  * status_ID INTEGER NOT NULL
  * class_ID INTEGER NOT NULL
  * locked INTEGER NOT NULL

* Country
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * name TEXT NOT NULL
  * abbreviation TEXT NOT NULL
Static data: ('United States', 'USA')

* PhoneStatus
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * name TEXT NOT NULL
Static data: primary, secondary, inactive, other

* EmailStatus
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * name TEXT NOT NULL
Static data: primary, secondary, inactive, other

* ContactType
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * name TEXT NOT NULL
Static data: customer, vendor, other

* ContactClass
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * type TEXT NOT NULL
Static data: retail, wholesale, gratis, other

### Inventory

The purpose of this table is to track what products are in stock. These
records are only used to generate invoices and packing slips. There is no
implication for any account other than to reference what was sold.

* InventoryItem
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * date_added REAL NOT NULL
  * name TEXT NOT NULL
  * description TEXT
  * note TEXT NOT NULL
  * num_stock INTEGER NOT NULL
  * retail REAL NOT NULL
  * wholesale REAL NOT NULL

### Accounts

The purpose of these tables is to implement the double-entry accounting
principles for the business. Accounts are generic and have a particular type.
that governs what can be done with the account.

For the purposes of this system, all accounts are treated equally and not
categorized. In the database, an account is simply a placeholder for a dollar
amount. Some attempt is made to give an account an appropriate account number,
according to standard accounting practice.

* Account
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * number INTEGER NOT NULL
  * name TEXT NOT NULL
  * description TEXT NOT NULL
  * notes TEXT
  * total REAL NOT NULL
Initial data: accounts listed above

* AccountType
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * name
Static data: credit, debit

### Account Transactions

Transactions are of a specific type and contain the information that
pertains to that transaction. The transaction is used to record an event that
has an effect on an account. A transaction is the ONLY way to update an
account.

* TransactionType
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * name TEXT NOT NULL
  * description TEXT
  * notes TEXT
Initial data: transactions listed above

* TransactionSequence  -- These rows are semi-static and are used to automate
  the movement of funds from one account to another. These records tell the
  transaction instance what to do.
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * transaction_type_ID INTEGER NOT NULL
  * sequence_number INTEGER NOT NULL
  * raw_import_column TEXT
  * gross REAL NOT NULL
  * to_account_ID INTEGER NOT NULL
  * from_account_ID INTEGER NOT NULL
Initial data: steps for transaction types listed above.

* TransactionInstance -- A line in this table is created for every movement of
  funds from one account to another.
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * date TEXT NOT NULL
  * description TEXT
  * notes TEXT
  * raw_import_ID INTEGER
  * contact_ID INTEGER NOT NULL
  * transaction_type_ID INTEGER NOT NULL
  * transaction_seq_ID INTEGER NOT NULL

* ImportRecord -- This table is used when expenses or contacts are imported
  from PayPal. A transaction instance is created when the expense is
  categorized.
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * date TEXT NOT NULL
  * contact_ID INTEGER
  * gross REAL NOT NULL
  * shipping REAL
  * fee REAL
  * tax REAL

* SaleRecord -- This table is used to record the fact of a sale. When a sale
  is made, this is created and then when the order is shipped, this is marked
  as such. This is used to allow us to track orders that have not shipped yet.
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * date TEXT NOT NULL
  * contact_ID INTEGER NOT NULL
  * status_ID INTEGER NOT NULL

* ProductList -- This table connects what was sold to the sale record, many
  to one.
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * sale_record_ID INTEGER NOT NULL
  * inventory_ID INTEGER NOT NULL

* SaleStatus
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * name TEXT NOT NULL
Static data: active, paid, ready, shipped, complete, trouble, canceled

### Other information

This table holds information about the business, used to create invoices.

* Information
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * contact_ID INTEGER NOT NULL
  * title TEXT NOT NULL
  * logo BLOB
  * slogan TEXT NOT NULL

### Raw Import Table

* RawImport -- This holds the raw data that was imported from PayPal. It
  is specific to the CSV file that they send when transactions are downloaded
  from the internet.
  * ID INTEGER PRIMARY KEY AUTOINCREMENT
  * Date TEXT
  * Time TEXT
  * TimeZone TEXT
  * Name TEXT
  * Type TEXT
  * Status TEXT
  * Currency TEXT
  * Gross TEXT
  * Fee TEXT
  * Net TEXT
  * FromEmail TEXT
  * ToEmail TEXT
  * TransactionID TEXT
  * ShippingAddress TEXT
  * AddressStatus TEXT
  * ItemTitle TEXT
  * ItemID TEXT
  * Shipping TEXT
  * InsuranceAmount TEXT
  * SalesTax TEXT
  * Option1Name TEXT
  * Option1Value TEXT
  * Option2Name TEXT
  * Option2Value TEXT
  * ReferenceTxnID TEXT
  * InvoiceNumber TEXT
  * CustomNumber TEXT
  * Quantity TEXT
  * ReceiptID TEXT
  * Balance TEXT
  * AddressLine1 TEXT
  * AddressLine2 TEXT
  * City TEXT
  * State TEXT
  * PostalCode TEXT
  * Country TEXT
  * Phone TEXT
  * Subject TEXT
  * Note TEXT
  * CountryCode TEXT
  * BalanceImpact TEXT
  * Completed INTEGER
