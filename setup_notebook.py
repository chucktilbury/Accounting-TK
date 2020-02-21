from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase
from form_widgets import *
from notebk import NoteBk
from importer import Importer
from contact_form import CustomerForm, VendorForm
from import_form import ImportPurchases, ImportSales

class SetupNotebook(object):

    def __init__(self, master):

        notebook = NoteBk(master, height=600, width=900)
        notebook.add_tab('Business', BusinessForm, scrolling=True)
        notebook.add_tab('Customers', CustomerForm)
        notebook.add_tab('Vendors', VendorForm)
        notebook.add_tab('Accounts', AccountsForm)
        notebook.add_tab('Inventory', InventoryForm)
        # notebook.add_tab('Trans Types', TransactionTypeForm)
        # notebook.add_tab('Transactions', TransactionsForm)
        notebook.add_tab(' Sales ', ImportSales, scrolling=True, height=700, width=600)
        notebook.add_tab(' Purchases ', ImportPurchases)
        notebook.add_tab('Import', ImportFiles)

        notebook.show_frame('Business')

class ImportFiles(SetupFormBase):
    '''
    Load one or more CSV files into the database from disk.
    '''
    def __init__(self, master, *args, **kargs):

        super().__init__(master, 'RawImport', *args, **kargs)
        self.form_contents = []
        master.grid(padx=10, pady=10)
        self.importer = Importer()

        row = 0
        col = 0

        header = Header(master, "Import Files")
        header.grid(row=row, column=col, columnspan=4)

        row+=1
        col=0
        tk.Label(master, text='Import a CSV file for disk. All of the records').grid(row=row, column=col)
        row+=1
        tk.Label(master, text='are placed in the database, the customers, vendors,').grid(row=row, column=col)
        row+=1
        tk.Label(master, text='sales, and purchases are updated into the system.').grid(row=row, column=col)

        row+=1
        col=0
        buttons = SingleButtonBox(master, 'import_file_form', 'Import')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(self.import_file)

        self.row = row
        #self.set_form()

    def import_file(self):
        '''
        Bring a file into the database.
        '''
        self.importer.import_all()
        # num = self.importer.read_all()
        # self.importer.import_country_codes()
        # #mb.showinfo('INFO', 'Imported %d lines from file.'%(num))
        # if num > 0:
        #     self.importer.import_customer_contacts()
        #     self.importer.import_vendor_contacts()
        #     self.importer.do_purchase_transactions()
        #     self.importer.do_sales_transactions()

# CREATE TABLE Business
#         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         title TEXT NOT NULL,
#         name TEXT NOT NULL,
#         address1 TEXT,
#         address2 TEXT,
#         state TEXT,
#         city TEXT,
#         zip TEXT,
#         email_address TEXT,
#         phone_number TEXT,
#         web_site TEXT,
#         description TEXT,
#         terms TEXT,
#         returns TEXT,
#         warranty TEXT,
#         country TEXT,
#         logo BLOB,
#         slogan TEXT);
class BusinessForm(SetupFormBase):
    '''
    This is the form used to set up accounts.
    '''

    def __init__(self, master):

        super().__init__(master, 'Business')
        self.form_contents = []
        #master.grid(padx=10, pady=10)

        row = 0
        col = 0
        width = 50

        header = Header(master, "Setup Business Info")
        header.grid(row=row, column=col, columnspan=4)

        row+=1
        col=0
        tk.Label(master, text='Title:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        title = EntryBox(master, self.table, 'title', width=width)
        title.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(title.get_line())

        row+=1
        col=0
        tk.Label(master, text='Name:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.name = EntryBox(master, self.table, 'name', width=width)
        self.name.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(self.name.get_line())

        row+=1
        col=0
        tk.Label(master, text='Address1:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        address1 = EntryBox(master, self.table, 'address1', width=width)
        address1.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(address1.get_line())

        row+=1
        col=0
        tk.Label(master, text='Address2:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        address2 = EntryBox(master, self.table, 'address2', width=width)
        address2.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(address2.get_line())

        row+=1
        col=0
        tk.Label(master, text='City:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        city = EntryBox(master, self.table, 'city')
        city.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(city.get_line())

        #row+=1
        #col=0
        col+=1
        tk.Label(master, text='State:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        state = EntryBox(master, self.table, 'state')
        state.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(state.get_line())

        row+=1
        col=0
        tk.Label(master, text='Zip Code:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        zip = EntryBox(master, self.table, 'zip')
        zip.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(zip.get_line())

        #row+=1
        #col=0
        col+=1
        tk.Label(master, text='Country:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        country = EntryBox(master, self.table, 'country')
        country.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(country.get_line())

        row+=1
        col=0
        tk.Label(master, text='Email:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        email_address = EntryBox(master, self.table, 'email_address')
        email_address.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(email_address.get_line())

        #row+=1
        #col=0
        col+=1
        tk.Label(master, text='Phone:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        phone_number = EntryBox(master, self.table, 'phone_number')
        phone_number.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(phone_number.get_line())

        row+=1
        col=0
        tk.Label(master, text='Web Site:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        web_site = EntryBox(master, self.table, 'web_site', width=width)
        web_site.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(web_site.get_line())

        row+=1
        col=0
        tk.Label(master, text='Description:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        description = EntryBox(master, self.table, 'description', width=width)
        description.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(description.get_line())

        row+=1
        col=0
        tk.Label(master, text='Terms:').grid(row=row, column=0, sticky=(tk.E))
        col+=1
        terms = NotesBox(master, self.table, 'terms')
        terms.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(terms.get_line())

        row+=1
        col=0
        tk.Label(master, text='Returns:').grid(row=row, column=0, sticky=(tk.E))
        col+=1
        returns = NotesBox(master, self.table, 'returns')
        returns.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(returns.get_line())

        row+=1
        col=0
        tk.Label(master, text='Warranty:').grid(row=row, column=0, sticky=(tk.E))
        col+=1
        warranty = NotesBox(master, self.table, 'warranty')
        warranty.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(warranty.get_line())

        row+=1
        col=0
        buttons = SingleButtonBox(master, 'business_form', 'Save')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(self.save_button_command)

        self.notebook_callback()

    def notebook_callback(self):
        self.set_form()

# CREATE TABLE Account
#         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         number INTEGER NOT NULL,
#         name TEXT NOT NULL,
#         description TEXT NOT NULL,
#         type TEXT,
#         notes TEXT,
#         total REAL NOT NULL);
class AccountsForm(SetupFormBase):
    '''
    This is the form used to set up accounts.
    '''

    def __init__(self, master):

        super().__init__(master, 'Account')
        self.form_contents = []
        master.grid(padx=10, pady=10)

        row = 0
        col = 0

        header = Header(master, "Setup Accounts")
        header.grid(row=row, column=col, columnspan=4)

        row+=1
        tk.Label(master, text='Name:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.name = EntryBox(master, self.table, 'name')
        self.name.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.name.get_line())

        row+=1
        col=0
        tk.Label(master, text='Number:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        number = EntryBox(master, self.table, 'number')
        number.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(number.get_line())

        row+=1
        col=0
        tk.Label(master, text='Type:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.account_type = ComboBox(master, self.table, 'type_ID')
        self.account_type.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.account_type.get_line())

        row+=1
        col=0
        tk.Label(master, text='Total:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        total = EntryBox(master, self.table, 'total')
        total.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(total.get_line())

        row+=1
        col=0
        tk.Label(master, text='Description:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        description = EntryBox(master, self.table, 'description', width=50)
        description.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(description.get_line())

        row+=1
        col=0
        tk.Label(master, text='Notes:').grid(row=row, sticky=(tk.E))
        col+=1
        notes = NotesBox(master, self.table, 'notes')
        notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(notes.get_line())

        row+=1
        col=0
        buttons = ButtonBox(master, 'accounts_form')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(
            self.next_btn_command,
            self.prev_btn_command,
            self.select_button_command,
            self.new_button_command,
            self.save_button_command,
            self.del_button_command,
        )

        self.notebook_callback()

    def notebook_callback(self):
        self.account_type.populate('AccountTypes', 'name')
        self.set_form()


# CREATE TABLE InventoryItem
#         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         stock_num INTEGER NOT NULL,
#         # date_added REAL NOT NULL,
#         name TEXT NOT NULL,
#         description TEXT,
#         note TEXT,
#         num_stock INTEGER NOT NULL,
#         retail REAL NOT NULL,
#         wholesale REAL NOT NULL);
class InventoryForm(SetupFormBase):
    '''
    This is the main frame that "contains" the other frames.
    '''

    def __init__(self, master):

        super().__init__(master, "InventoryItem")
        self.form_contents = []
        master.grid(padx=10, pady=10)

        row = 0
        col = 0
        width = 50

        header = Header(master, "Setup Inventory")
        header.grid(row=row, column=col, columnspan=4)

        row+=1
        col=0
        tk.Label(master, text='Name:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.name = EntryBox(master, self.table, 'name')
        self.name.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.name.get_line())

        row+=1
        col=0
        tk.Label(master, text='Stock Num:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        stock_num = EntryBox(master, self.table, 'stock_num')
        stock_num.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(stock_num.get_line())

        row+=1
        col=0
        tk.Label(master, text='Stock:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        num_stock = EntryBox(master, self.table, 'num_stock')
        num_stock.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(num_stock.get_line())

        row+=1
        col=0
        tk.Label(master, text='Retail:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        retail = EntryBox(master, self.table, 'retail')
        retail.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(retail.get_line())

        row+=1
        col=0
        tk.Label(master, text='Wholesale:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        wholesale = EntryBox(master, self.table, 'wholesale')
        wholesale.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(wholesale.get_line())

        row+=1
        col=0
        tk.Label(master, text='Description:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        description = EntryBox(master, self.table, 'description', width=width)
        description.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(description.get_line())

        row+=1
        col=0
        tk.Label(master, text='Notes:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        notes = NotesBox(master, self.table, 'notes')
        notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(notes.get_line())

        row+=1
        col=0
        buttons = ButtonBox(master, 'inventory_form')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(
            self.next_btn_command,
            self.prev_btn_command,
            self.select_button_command,
            self.new_button_command,
            self.save_button_command,
            self.del_button_command,
        )

        self.notebook_callback()
        #self.set_form(self.crnt_index)

    def notebook_callback(self):
        self.set_form()

# # Note that the name of the transaction type maps to a function in code.
# # CREATE TABLE TransactionType
# #         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
# #         name TEST NOT NULL,
# #         number INTEGER NOT NULL,
# #         description TEXT);

# class TransactionTypeForm(SetupFormBase):
#     '''
#     This is the main frame that "contains" the other frames.
#     '''

#     def __init__(self, master):

#         super().__init__(master, "TransactionType")
#         self.form_contents = []
#         master.grid(padx=10, pady=10)

#         row = 0
#         col = 0
#         width = 50

#         header = Header(master, "Setup Transaction Type")
#         header.grid(row=row, column=col, columnspan=4)

#         row+=1
#         col=0
#         tk.Label(master, text='Name:').grid(row=row, column=col, sticky=(tk.E))
#         col+=1
#         self.name = EntryBox(master, self.table, 'name')
#         self.name.grid(row=row, column=col, sticky=(tk.W))
#         self.form_contents.append(self.name.get_line())

#         row+=1
#         col=0
#         tk.Label(master, text='Description:').grid(row=row, column=col, sticky=(tk.E))
#         col+=1
#         description = EntryBox(master, self.table, 'description', width=width)
#         description.grid(row=row, column=col, sticky=(tk.W))
#         self.form_contents.append(description.get_line())

#         row+=1
#         col=0
#         tk.Label(master, text='Notes:').grid(row=row, column=col, sticky=(tk.E))
#         col+=1
#         notes = NotesBox(master, self.table, 'notes')
#         notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
#         self.form_contents.append(notes.get_line())

#         row+=1
#         col=0
#         buttons = ButtonBox(master, 'transaction_type_form')
#         buttons.grid(row=row, column=col, columnspan=4)
#         buttons.register_events(
#             self.next_btn_command,
#             self.prev_btn_command,
#             self.select_button_command,
#             self.new_button_command,
#             self.save_button_command,
#             self.del_button_command,
#         )

#         self.notebook_callback()
#         #self.set_form(self.crnt_index)

#     def notebook_callback(self):
#         self.set_form()

# # CREATE TABLE TransactionSequence
# #         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
# #         name TEXT NOT NULL,
# #         description TEXT,
# #         notes TEXT,
# #         transaction_type_ID INTEGER NOT NULL,
# #         sequence_number INTEGER NOT NULL,
# #         raw_import_column TEXT,
# #         to_account_ID INTEGER NOT NULL,
# #         from_account_ID INTEGER NOT NULL);

# class TransactionsForm(SetupFormBase):
#     '''
#     This is the main frame that "contains" the other frames.
#     '''
#     def __init__(self, master):

#         super().__init__(master, "TransactionSequence")
#         self.form_contents = []
#         master.grid(padx=10, pady=10)

#         row=0
#         col=0
#         width = 50

#         header = Header(master, "Setup Transaction Sequence")
#         header.grid(row=row, column=col, columnspan=4)

#         row+=1
#         col=0
#         tk.Label(master, text='Name:').grid(row=row, column=col, sticky=(tk.E))
#         col+=1
#         self.name = EntryBox(master, self.table, 'name')
#         self.name.grid(row=row, column=col, sticky=(tk.W))
#         self.form_contents.append(self.name.get_line())

#         row+=1
#         col=0
#         tk.Label(master, text='Description:').grid(row=row, column=col, sticky=(tk.E))
#         col+=1
#         description = EntryBox(master, self.table, 'description', width=width)
#         description.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
#         self.form_contents.append(description.get_line())

#         row+=1
#         col=0
#         tk.Label(master, text='Transaction Type:').grid(row=row, column=col, sticky=(tk.E))
#         col+=1
#         self.transaction = ComboBox(master, self.table, 'transaction_type_ID')
#         self.transaction.grid(row=row, column=col, sticky=(tk.W))
#         self.form_contents.append(self.transaction.get_line())

#         #row+=1
#         #col=0
#         col+=1
#         tk.Label(master, text='Raw Import Column:').grid(row=row, column=col, sticky=(tk.E))
#         col+=1
#         self.raw_column = ComboBox(master, self.table, 'raw_import_column')
#         self.raw_column.grid(row=row, column=col, sticky=(tk.W))
#         self.form_contents.append(self.raw_column.get_line())

#         row+=1
#         col=0
#         tk.Label(master, text="From Account:").grid(row=row, column=col, sticky=(tk.E))
#         col+=1
#         self.from_account = ComboBox(master, self.table, 'from_account_ID')
#         self.from_account.grid(row=row, column=col, sticky=(tk.W))
#         self.form_contents.append(self.from_account.get_line())

#         #row+=1
#         #col=0
#         col+=1
#         tk.Label(master, text="To Account:").grid(row=row, column=col, sticky=(tk.E))
#         col+=1
#         self.to_account = ComboBox(master, self.table, 'to_account_ID')
#         self.to_account.grid(row=row, column=col, sticky=(tk.W))
#         self.form_contents.append(self.to_account.get_line())

#         row+=1
#         col=0
#         tk.Label(master, text="Sequence:").grid(row=row, column=col, sticky=(tk.E))
#         col+=1
#         sequence = EntryBox(master, self.table, 'sequence_number')
#         sequence.grid(row=row, column=col, sticky=(tk.W))
#         self.form_contents.append(sequence.get_line())

#         row+=1
#         col=0
#         tk.Label(master, text='Notes:').grid(row=6, column=0, sticky=(tk.E))
#         col+=1
#         notes = NotesBox(master, self.table, 'notes')
#         notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
#         self.form_contents.append(notes.get_line())

#         row+=1
#         col=0
#         buttons = ButtonBox(master, 'transactions_form')
#         buttons.grid(row=row, column=col, columnspan=4)
#         buttons.register_events(
#             self.next_btn_command,
#             self.prev_btn_command,
#             self.select_button_command,
#             self.new_button_command,
#             self.save_button_command,
#             self.del_button_command,
#         )

#         self.notebook_callback()

#     def notebook_callback(self):
#         self.transaction.populate('TransactionType', 'name')
#         self.raw_column.populate('RawImportNames', 'name')
#         self.from_account.populate('Account', 'name')
#         self.to_account.populate('Account', 'name')
#         self.set_form()

