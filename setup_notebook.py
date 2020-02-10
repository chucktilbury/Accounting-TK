from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase
from form_widgets import *
from notebk import NoteBk

class SetupNotebook(object):

    def __init__(self, master):

        notebook = NoteBk(master, height=600, width=900)
        notebook.add_tab('Contacts')
        notebook.add_tab('Accounts')
        notebook.add_tab('Inventory')
        notebook.add_tab('Trans Types')
        notebook.add_tab('Transactions')
        notebook.add_tab('Queries')

        ContactsForm(notebook.get_frame('Contacts'))
        AccountsForm(notebook.get_frame('Accounts'))
        InventoryForm(notebook.get_frame('Inventory'))
        TransactionTypeForm(notebook.get_frame('Trans Types'))
        TransactionsForm(notebook.get_frame('Transactions'))

        notebook.show_frame('Contacts')

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
        master.grid()

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
        account_type = ComboBox(master, self.table, 'type_ID')
        account_type.populate('AccountTypes', 'name')
        account_type.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(account_type.get_line())

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

        self.set_form(self.crnt_index)

# CREATE TABLE Contacts
#         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         date_created TEXT NOT NULL,
#         name TEXT NOT NULL,
#         address1 TEXT NOT NULL,
#         address2 TEXT,
#         state TEXT NOT NULL,
#         city TEXT NOT NULL,
#         zip TEXT NOT NULL,
#         email_address TEXT,
#         email_status_ID INTEGER,
#         phone_number TEXT,
#         phone_status_ID INTEGER,
#         web_site TEXT,
#         description TEXT,
#         notes TEXT,
#         country_ID INTEGER NOT NULL,
#         type_ID INTEGER NOT NULL,
#         status_ID INTEGER NOT NULL,
#         class_ID INTEGER NOT NULL,
#         locked_ID INTEGER NOT NULL);

class ContactsForm(SetupFormBase):
    '''
    This is the main frame that "contains" the other frames.
    '''

    def __init__(self, master):

        super().__init__(master, 'Contacts')
        self.form_contents = []
        master.grid()

        row = 0
        col = 0
        width = 50

        header = Header(master, "Setup Contacts")
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
        tk.Label(master, text='Contact Status:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        status_ID = ComboBox(master, self.table, 'status_ID')
        status_ID.populate('ContactStatus', 'name')
        status_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(status_ID.get_line())

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
        tk.Label(master, text='Email Status:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        email_status_ID = ComboBox(master, self.table, 'email_status_ID')
        email_status_ID.populate('EmailStatus', 'name')
        email_status_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(email_status_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Phone:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        phone_number = EntryBox(master, self.table, 'phone_number')
        phone_number.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(phone_number.get_line())

        #row+=1
        #col=0
        col+=1
        tk.Label(master, text='Phone Status:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        phone_status_ID = ComboBox(master, self.table, 'phone_status_ID')
        phone_status_ID.populate('PhoneStatus', 'name')
        phone_status_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(phone_status_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Web Site:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        web_site = EntryBox(master, self.table, 'web_site')
        web_site.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(web_site.get_line())

        #row+=1
        #col=0
        col+=1
        tk.Label(master, text='Country:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        country_ID = ComboBox(master, self.table, 'country_ID')
        country_ID.populate('Country', 'name')
        country_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(country_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Description:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        description = EntryBox(master, self.table, 'description', width=width)
        description.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(description.get_line())


        row+=1
        col=0
        tk.Label(master, text='Type:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        type_ID = ComboBox(master, self.table, 'type_ID')
        type_ID.populate('ContactType', 'name')
        type_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(type_ID.get_line())

        #row+=1
        #col=0
        col+=1
        tk.Label(master, text='Status:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        status_ID = ComboBox(master, self.table, 'status_ID')
        status_ID.populate('ContactStatus', 'name')
        status_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(status_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Class:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        class_ID = ComboBox(master, self.table, 'class_ID')
        class_ID.populate('ContactClass', 'name')
        class_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(class_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Locked:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        locked_ID = ComboBox(master, self.table, 'locked_ID')
        locked_ID.populate('LockedState', 'name')
        locked_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(locked_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Notes:').grid(row=row, column=0, sticky=(tk.E))
        col+=1
        notes = NotesBox(master, self.table, 'notes')
        notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(notes.get_line())

        row+=1
        col=0
        buttons = ButtonBox(master, 'contacts_form')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(
            self.next_btn_command,
            self.prev_btn_command,
            self.select_button_command,
            self.new_button_command,
            self.save_button_command,
            self.del_button_command
        )

        self.set_form(self.crnt_index)

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
        master.grid()

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

        self.set_form(self.crnt_index)

# Note that the name of the transaction type maps to a function in code.
# CREATE TABLE TransactionType
#         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEST NOT NULL,
#         number INTEGER NOT NULL,
#         description TEXT);

class TransactionTypeForm(SetupFormBase):
    '''
    This is the main frame that "contains" the other frames.
    '''

    def __init__(self, master):

        super().__init__(master, "TransactionType")
        self.form_contents = []
        master.grid()

        row = 0
        col = 0
        width = 50

        header = Header(master, "Setup Transaction Type")
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
        buttons = ButtonBox(master, 'transaction_type_form')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(
            self.next_btn_command,
            self.prev_btn_command,
            self.select_button_command,
            self.new_button_command,
            self.save_button_command,
            self.del_button_command,
        )

        self.set_form(self.crnt_index)

# CREATE TABLE TransactionSequence
#         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         description TEXT,
#         notes TEXT,
#         transaction_type_ID INTEGER NOT NULL,
#         sequence_number INTEGER NOT NULL,
#         raw_import_column TEXT,
#         to_account_ID INTEGER NOT NULL,
#         from_account_ID INTEGER NOT NULL);

class TransactionsForm(SetupFormBase):
    '''
    This is the main frame that "contains" the other frames.
    '''
    def __init__(self, master):

        super().__init__(master, "TransactionSequence")
        self.form_contents = []
        master.grid()

        row=0
        col=0
        width = 50

        header = Header(master, "Setup Transaction Sequence")
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
        tk.Label(master, text='Description:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        description = EntryBox(master, self.table, 'description', width=width)
        description.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(description.get_line())

        row+=1
        col=0
        tk.Label(master, text='Transaction Type:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        transaction = ComboBox(master, self.table, 'transaction_type_ID')
        transaction.populate('TransactionType', 'name')
        transaction.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(transaction.get_line())

        #row+=1
        #col=0
        col+=1
        tk.Label(master, text='Raw Import Column:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        raw_column = ComboBox(master, self.table, 'raw_import_column')
        raw_column.populate('RawImportNames', 'name')
        raw_column.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(raw_column.get_line())

        row+=1
        col=0
        tk.Label(master, text="From Account:").grid(row=row, column=col, sticky=(tk.E))
        col+=1
        from_account = ComboBox(master, self.table, 'from_account_ID')
        from_account.populate('Account', 'name')
        from_account.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(from_account.get_line())

        #row+=1
        #col=0
        col+=1
        tk.Label(master, text="To Account:").grid(row=row, column=col, sticky=(tk.E))
        col+=1
        to_account = ComboBox(master, self.table, 'to_account_ID')
        to_account.populate('Account', 'name')
        to_account.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(to_account.get_line())

        row+=1
        col=0
        tk.Label(master, text="Sequence:").grid(row=row, column=col, sticky=(tk.E))
        col+=1
        sequence = EntryBox(master, self.table, 'sequence_number')
        sequence.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(sequence.get_line())

        row+=1
        col=0
        tk.Label(master, text='Notes:').grid(row=6, column=0, sticky=(tk.E))
        col+=1
        notes = NotesBox(master, self.table, 'notes')
        notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(notes.get_line())

        row+=1
        col=0
        buttons = ButtonBox(master, 'transactions_form')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(
            self.next_btn_command,
            self.prev_btn_command,
            self.select_button_command,
            self.new_button_command,
            self.save_button_command,
            self.del_button_command,
        )

        self.set_form(self.crnt_index)

