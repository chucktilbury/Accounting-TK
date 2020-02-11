from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk
import os, sys

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase
from form_widgets import *
from notebk import NoteBk
from tkinter.filedialog import askopenfile
from importer import Importer
from contact_form import CustomerForm, VendorForm
class ImportForm(SetupFormBase):
    '''
    This form is used to help import records from the PayPal CSV download.
    '''

    def __init__(self, master):

        super().__init__(master, 'RawImport')
        self.form_contents = []
        master.grid(padx=10, pady=10)

        row = 0
        col = 0

        header = Header(master, "Import Records")
        header.grid(row=row, column=col, columnspan=4)

        notebook = NoteBk(master, height=600, width=900)
        notebook.add_tab('Import Cust')
        notebook.add_tab('Import Vend')
        notebook.add_tab('Import Sale')
        notebook.add_tab('Import Purc')

        CustomerForm(notebook.get_frame('Import Cust'), importing=True)
        VendorForm(notebook.get_frame('Import Vend'), importing=True)
        ImportSales(notebook.get_frame('Import Sale'))
        ImportPurchases(notebook.get_frame('Import Purc'))

    def import_callback(self):
        self.import_frame.populate_picker()

class ImportSales(tk.Frame):
    '''
    Implement importing a CSV file from disk.
    '''
    def __init__(self, master, *args, **kargs):

        super().__init__(master, *args, **kargs)
        self.form_contents = []
        master.grid(padx=10, pady=10)

        row = 0
        col = 0

        header = Header(master, "Import Sales")
        header.grid(row=row, column=col, columnspan=4)


        row+=1
        col=0
        buttons = ButtonBox(master, 'sales_form_import')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(
            self.next_btn_command,
            self.prev_btn_command,
            self.select_button_command,
            self.new_button_command,
            self.save_button_command,
            self.del_button_command
        )

        row+=1
        col=0
        buttons = SingleButtonBox(master, 'vendor_form', 'Import')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(self.import_customers)

        self.row = row
        self.set_form(self.crnt_index)


    def populate_picker(self):
        Importer().import_all()
        print('\n\ncall me please\n\n')

class ImportPurchases(tk.Frame):
    '''
    Implement reviewing all of the imported sales.
    '''
    def __init__(self, master, *args, **kargs):

        super().__init__(master, *args, **kargs)
        self.form_contents = []
        master.grid(padx=10, pady=10)

        row = 0
        col = 0

        header = Header(master, "Import Purchases")
        header.grid(row=row, column=col, columnspan=4)

        row+=1
        col=0
        buttons = ButtonBox(master, 'purchases_form_import')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(
            self.next_btn_command,
            self.prev_btn_command,
            self.select_button_command,
            self.new_button_command,
            self.save_button_command,
            self.del_button_command
        )

        row+=1
        col=0
        buttons = SingleButtonBox(master, 'vendor_form', 'Import')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(self.import_customers)

        self.row = row
        self.set_form(self.crnt_index)
