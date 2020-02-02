###############################################################################
#
# This file populates the database with default records.
#
INSERT INTO Contacts (
        date_created, # normally set by software
        name,
        address1,
        state,
        city,
        zip,
        email_address,
        email_status_ID,
        phone_number,
        phone_status_ID,
        web_site,
        description,
        country_ID,
        type_ID,
        status_ID,
        class_ID,
        locked)
    # Modify this to meet needs
    VALUES (
        '01/12/2020',
        'Chuck Tilbury',
        '10855 State Hwy 83',
        'Oklahoma',
        'Poteau',
        '74953',
        'chucktilbury@gmail.com',
        1,
        '512-84-8322',
        1,
        'http://whistlemaker.com',
        'Owner of company',
        1,
        3,
        3,
        4,
        True);

INSERT INTO Country
        (name, abbreviation)
    VALUES
        ('United States', 'US');

INSERT INTO PhoneStatus
        (name)
    VALUES
        ('primary'), ('secondary'), ('inactive'), ('other');

INSERT INTO EmailStatus
        (name)
    VALUES
        ('primary'), ('secondary'), ('inactive'), ('other');

INSERT INTO ContactType
        (name)
    VALUES
        ('customer'), ('vendor'), ('other');

INSERT INTO ContactStatus
        (name)
    VALUES
        ('active'), ('inactive'), ('other');

INSERT INTO ContactClass
        (name)
    VALUES
        ('wholesale'), ('retail'), ('gratis'), ('other');

###############################################################################
#
# Information about the business
#

INSERT INTO Business
    (contact_ID, title, slogan)
   VALUES
    (1, 'Tilbury Woodwinds Company', 'Maker of fine musical instruments');

###############################################################################
#
# Default account chart
#

# Revenue
# ID = 1
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (1001, 'Cash', 'Money on hand. Checking account.', 1, 0.0);

# ID = 2
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (1011, 'ShippingCollected', 'Money collected for shipping as part of a sale.', 1,  0.0);

# ID = 3
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (1021, 'TaxesCollected', 'Money collected for taxes as part of a sale.', 1, 0.0);

# Expenses
# ID = 4
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2001, 'Materials', 'Cost of items that stay in product past sale.', 2, 0.0);

# ID = 5
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2002, 'Consumables', 'Cost of items that do not stay in product past sale.', 2, 0.0);

# ID = 6
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2003, 'OtherExpense', 'Cost of items that are not materials or consumable.', 2, 0.0);

# ID = 7
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2011, 'ShippingCustomer', 'Cost of shipping payed for product out.', 2,  0.0);

# ID = 8
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2021, 'TaxPayed', 'Cost of taxes payed to vendor.', 2,  0.0);

# ID = 9
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2031, 'ShippingVendor', 'Cost of shipping payed to vendor.', 2,  0.0);

# ID = 10
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2041, 'BankFees', 'Cost of PayPal transaction.', 2,  0.0);

# ID = 11
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2051, 'RawExpense', 'Expenses that have not been categorized.', 2, 0.0);

# Asset
# ID = 12
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (3001, 'InventoryValue', 'Value of items in stock.', 3, 0.0);

# ID = 13
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (3002, 'InventoryInvestment', 'Value of items in stock.', 3, 0.0);

# Liability
# ID = 14
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (4001, 'CostOfGoodsSold', 'Cost of items in stock.', 4,  0.0);

# ID = 15
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (4002, 'InventoryCost', 'Cost of items that are ready to sell.', 2, 0.0);

# Equity
# ID = 16
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (5001, 'OwnerCapital', 'Owner investment in company.', 4,  0.0);

# ID = 17
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (6001, 'OwnerDraw', 'Owner draws from investment.', 4,  0.0);

INSERT INTO AccountTypes
        (name)
    VALUES
        ('Revenue'), ('Expense'), ('Asset'), ('Liability'), ('Other');

###############################################################################
#
# Default transaction map

# Funds come into the system from a sale.
# Increase: Cash
# Decrease: InventoryValue
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (100, 'Sale', 'Customer is buying a product', 'Gross', 1, 12);

# Move taxes collected from a sale into the tax collected account
# Increase: TaxCollected
# Decrease: Cash
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (101, 'SaleTax', 'Deduct taxes collected from sale', 'SalesTax', 3, 1);

# Funds come into the system from a sale.
# Increase: ShippingCollected
# Decrease: Cash
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (102, 'Shipping', 'Deduct shipping collected from sale', 'Shipping', 2, 1);

# Funds come into the system from a sale.
# Increase: BankFees
# Decrease: Cash
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (103, 'PayPalFee', 'Deduct paypal fee from sale', 'Shipping', 10, 1);

# Funds leave the system from an uncatagorized sale.
# Increase: RawExpense
# Decrease: Cash
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (201, 'RawPurchase', 'Not catagorized purchase', 'Gross', 11, 1);

# Move funds from an uncatagorized sale to materials.
# Increase: Materials
# Decrease: RawExpense
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (202, 'MoveMaterials', 'Move materials expense from gross purchase', '', 4, 11);

# Move funds from an uncatagorized sale to consumables.
# Increase: Consumables
# Decrease: RawExpense
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (203, 'MoveConsumables', 'Move consumables expense from gross purchase', '', 5, 11);

# Move funds from an uncatagorized sale to non-cogs account.
# Increase: OtherExpense
# Decrease: RawExpense
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (203, 'MoveNonCOGS', 'Move non-cogs expense from gross purchase', '', 6, 11);

# Funds come out of the system for a non-cogs purchase
# Increase: OtherExpense
# Decrease: Cash
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (204, 'NonCogsPurchase', 'Company is buying something not COGS from a vendor', '', 6, 1);

# Funds come out of the system for a materials purchase
# Increase: Materials
# Decrease: Cash
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (205, 'PurchaseMaterials', 'Company is buying materials from a vendor', '', 4, 1);

# Funds come out of the system for a consumable purchase
# Increase: Consumables
# Decrease: Cash
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (206, 'PurchaseConsumables', 'Company is buying consumables from a vendor', '', 5, 1);

# Move funds from materials into cogs account
# Increase: CostOfGoodsSold
# Decrease: Materials

# Move funds from consumables into cogs account
# Increase: CostOfGoodsSold
# Decrease: Consumables

# Inventory comes in from the shop by the cost.
# Increase: InventoryInvestment
# Decrease: InventoryCost
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (300, 'Inventory In', 'Bring in inventory from the shop', '', 1, 1);

# Account for the inventory cost of the sale
# Increase: InventoryCost
# Decrease: InventoryInvestment
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (301, 'Inventory Out', 'Shipping inventory to a customer', '', 1, 1);

# Account for owner taking money out of the system
# Increase: OwnerDraw
# Decrease: Cash
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (400, 'Owner Cash Out', 'Owner takes cash out of the company', '', 1, 1);

# Account for owner taking money out of the system
# Increase: Cash
# Decrease: OwnerEquity
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (500, 'Owner Cash In', 'Owner brings cash into the company', '', 1, 1);

# This is implemented as a procedure with no actual inc/dec accounts
#INSERT INTO TransactionType
#        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
#    VALUES
#        (600, 'Close Books', 'Year end book closing', '', 1, 1);

# This is created as a part of entering a manual transaction. The source column,
# increment and decrement accounts are specified at the time the transaction is
# entered.
INSERT INTO TransactionType
        (number, name, description, raw_source_col, inc_account_ID, dec_account_ID)
    VALUES
        (700, 'ManualTransaction', 'All steps for transaction are configured manually', '', 1, 1);


###############################################################################
#
# Default inventory map
#

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10001, 'Aluminum Soprano Eb', 'Aluminum soprano whistle in the key of E-flat.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10002, 'Aluminum Soprano D', 'Aluminum soprano whistle in the key of D.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10003, 'Aluminum Soprano C', 'Aluminum soprano whistle in the key of C.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10004, 'Aluminum Mezzo Bb', 'Aluminum Mezzo whistle in the key of B-flat.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10005, 'Aluminum Mezzo A', 'Aluminum Mezzo whistle in the key of A.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10006, 'Aluminum Mezzo G', 'Aluminum Mezzo whistle in the key of G.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10007, 'Aluminum Mezzo F', 'Aluminum Mezzo whistle in the key of F.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10101, 'Brass Soprano Eb', 'Brass soprano whistle in the key of E-flat.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10102, 'Brass Soprano D', 'Brass soprano whistle in the key of D.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10103, 'Brass Soprano C', 'Brass soprano whistle in the key of C.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10104, 'Brass Mezzo Bb', 'Brass Mezzo whistle in the key of B-flat.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10105, 'Brass Mezzo A', 'Brass Mezzo whistle in the key of A.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10106, 'Brass Mezzo G', 'Brass Mezzo whistle in the key of G.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10107, 'Brass Mezzo F', 'Brass Mezzo whistle in the key of F.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10201, 'Brass Soprano Eb Plastic Beak', 'Brass soprano whistle in the key of E-flat with a  Plastic Beak.', 0, 95.0, 65.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10202, 'Brass Soprano D Plastic Beak', 'Brass soprano whistle in the key of D with a  Plastic Beak.', 0, 95.0, 65.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10203, 'Brass Soprano C Plastic Beak', 'Brass soprano whistle in the key of C with a  Plastic Beak.', 0, 95.0, 65.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10204, 'Brass Mezzo Bb Plastic Beak', 'Brass Mezzo whistle in the key of B-flat with a  Plastic Beak.', 0, 110.0, 75.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10205, 'Brass Mezzo A Plastic Beak', 'Brass Mezzo whistle in the key of A with a  Plastic Beak.', 0, 110.0, 75.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10206, 'Brass Mezzo G Plastic Beak', 'Brass Mezzo whistle in the key of G with a  Plastic Beak.', 0, 110.0, 75.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10207, 'Brass Mezzo F Plastic Beak', 'Brass Mezzo whistle in the key of F with a  Plastic Beak.', 0, 110.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10310, 'CPVC Tunable D', 'CPVC plastic tunable soprano D whistle.', 0, 35.0, 15.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, price, cost)
    VALUES
        (10310, 'Delrin And Brass D', 'Delrin and brass soprano D whistle.', 0, 90.0, 85.0);





