from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase
from form_widgets import *
from notebk import NoteBk
#from import_form import ImportForm

# CREATE TABLE Customer
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
class CustomerForm(SetupFormBase):
    '''
    Implement the customer form.
    '''

    def __init__(self, master, importing=False):

        super().__init__(master, 'Customer')
        self.form_contents = []
        master.grid(padx=10, pady=10)

        row = 0
        col = 0
        width = 50

        header = Header(master, "Setup Customers")
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
        tk.Label(master, text='Class:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        class_ID = ComboBox(master, self.table, 'class_ID')
        class_ID.populate('ContactClass', 'name')
        class_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(class_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Notes:').grid(row=row, column=0, sticky=(tk.E))
        col+=1
        notes = NotesBox(master, self.table, 'notes')
        notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(notes.get_line())

        row+=1
        col=0
        if importing:
            buttons = ButtonBox(master, 'customer_form_import')
        else:
            buttons = ButtonBox(master, 'customer_form')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(
            self.next_btn_command,
            self.prev_btn_command,
            self.select_button_command,
            self.new_button_command,
            self.save_button_command,
            self.del_button_command
        )

        if importing:
            row+=1
            col=0
            buttons = SingleButtonBox(master, 'customer_form', 'Import')
            buttons.grid(row=row, column=col, columnspan=4)
            buttons.register_events(self.import_customers)

        self.row = row
        self.set_form(self.crnt_index)

    def import_customers(self):
        print('\n\nImport Customers\n\n')


# CREATE TABLE Vendor
#         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         date_created TEXT,
#         name TEXT NOT NULL,
#         description TEXT,
#         notes TEXT,
#         email_address TEXT,
#         email_status_ID INTEGER,
#         phone_number TEXT,
#         phone_status_ID INTEGER,
#         web_site TEXT);
class VendorForm(SetupFormBase):
    '''
    Implement the vendor form.
    '''

    def __init__(self, master, importing=False):

        super().__init__(master, 'Vendor')
        self.form_contents = []
        master.grid(padx=10, pady=10)

        row = 0
        col = 0
        width = 50

        header = Header(master, "Setup Vendors")
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

        row+=1
        col=0
        tk.Label(master, text='Notes:').grid(row=row, column=0, sticky=(tk.E))
        col+=1
        notes = NotesBox(master, self.table, 'notes')
        notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(notes.get_line())

        row+=1
        col=0
        if importing:
            buttons = ButtonBox(master, 'vendor_form_import')
        else:
            buttons = ButtonBox(master, 'vendor_form')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(
            self.next_btn_command,
            self.prev_btn_command,
            self.select_button_command,
            self.new_button_command,
            self.save_button_command,
            self.del_button_command
        )

        if importing:
            row+=1
            col=0
            buttons = SingleButtonBox(master, 'vendor_form', 'Import')
            buttons.grid(row=row, column=col, columnspan=4)
            buttons.register_events(self.import_customers)

        self.row = row
        self.set_form(self.crnt_index)

    def import_vendors(self):
        print('\n\nImport Vendors\n\n')