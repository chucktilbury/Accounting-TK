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

# Account types
INSERT INTO AccountTypes
        (name)
    VALUES ('credit'), ('debit'), ('other');

# ID = 1
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (1001, 'Cash', 'Money on hand. Checking account.', 2, 0.0);

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

# ID = 4
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2001, 'Materials', 'wholesale of items that stay in product past sale.', 2, 0.0);

# ID = 5
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2002, 'OtherExpense', 'wholesale of items that do not stay in product past sale.', 2, 0.0);

# ID = 6
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2003, 'CustomerShippingPayed', 'wholesale of shipping product to customers.', 2, 0.0);

# ID = 7
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2011, 'TaxesPayed', 'Taxes that have been payed for an expense.', 2,  0.0);

# ID = 8
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2021, 'BankFees', 'Transaction fees payed to bank.', 2,  0.0);

# ID = 9
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2031, 'OwnerCapital', 'Funds payed out to the owner.', 1,  0.0);

# ID = 10
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2041, 'ExpenseImport', 'Raw expense before categorization.', 3,  0.0);

# ID = 11
INSERT INTO Account
        (number, name, description, type_ID,  total)
    VALUES
        (2051, 'MaterialsShippingPayed', 'Shipping that has been payed to a vendor.', 2, 0.0);

###############################################################################
#
# Default inventory map
#

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10001, 'Aluminum Soprano Eb', 'Aluminum soprano whistle in the key of E-flat.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10002, 'Aluminum Soprano D', 'Aluminum soprano whistle in the key of D.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10003, 'Aluminum Soprano C', 'Aluminum soprano whistle in the key of C.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10004, 'Aluminum Mezzo Bb', 'Aluminum Mezzo whistle in the key of B-flat.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10005, 'Aluminum Mezzo A', 'Aluminum Mezzo whistle in the key of A.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10006, 'Aluminum Mezzo G', 'Aluminum Mezzo whistle in the key of G.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10007, 'Aluminum Mezzo F', 'Aluminum Mezzo whistle in the key of F.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10101, 'Brass Soprano Eb', 'Brass soprano whistle in the key of E-flat.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10102, 'Brass Soprano D', 'Brass soprano whistle in the key of D.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10103, 'Brass Soprano C', 'Brass soprano whistle in the key of C.', 0, 80.0, 50.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10104, 'Brass Mezzo Bb', 'Brass Mezzo whistle in the key of B-flat.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10105, 'Brass Mezzo A', 'Brass Mezzo whistle in the key of A.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10106, 'Brass Mezzo G', 'Brass Mezzo whistle in the key of G.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10107, 'Brass Mezzo F', 'Brass Mezzo whistle in the key of F.', 0, 85.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10201, 'Brass Soprano Eb Plastic Beak', 'Brass soprano whistle in the key of E-flat with a  Plastic Beak.', 0, 95.0, 65.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10202, 'Brass Soprano D Plastic Beak', 'Brass soprano whistle in the key of D with a  Plastic Beak.', 0, 95.0, 65.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10203, 'Brass Soprano C Plastic Beak', 'Brass soprano whistle in the key of C with a  Plastic Beak.', 0, 95.0, 65.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10204, 'Brass Mezzo Bb Plastic Beak', 'Brass Mezzo whistle in the key of B-flat with a  Plastic Beak.', 0, 110.0, 75.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10205, 'Brass Mezzo A Plastic Beak', 'Brass Mezzo whistle in the key of A with a  Plastic Beak.', 0, 110.0, 75.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10206, 'Brass Mezzo G Plastic Beak', 'Brass Mezzo whistle in the key of G with a  Plastic Beak.', 0, 110.0, 75.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10207, 'Brass Mezzo F Plastic Beak', 'Brass Mezzo whistle in the key of F with a  Plastic Beak.', 0, 110.0, 55.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10310, 'CPVC Tunable D', 'CPVC plastic tunable soprano D whistle.', 0, 35.0, 15.0);

INSERT INTO InventoryItem
        (stock_num, name, description, num_stock, retail, wholesale)
    VALUES
        (10310, 'Delrin And Brass D', 'Delrin and brass soprano D whistle.', 0, 90.0, 85.0);





