from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk
import os, sys

from utility import Logger, debugger
from setup_form import SetupFormBase
from form_widgets import *
from committer import CommitPurchase, CommitSale

# CREATE TABLE SaleRecord
#         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         date TEXT NOT NULL,
#         customer_ID INTEGER NOT NULL,
#         raw_import_ID INTEGER,
#         status_ID INTEGER NOT NULL,
#         transaction_uuid TEXT NOT NULL,
#         gross REAL NOT NULL,
#         fees REAL NOT NULL,
#         shipping REAL NOT NULL,
#         notes TEXT,
#         committed_ID INTEGER NOT NULL);
class ImportSales(SetupFormBase):
    '''
    Implement importing a CSV file from disk.
    '''
    def __init__(self, master, *args, **kargs):

        super().__init__(master, 'SaleRecord', empty_ok=True, *args, **kargs)
        self.form_contents = []
        master.grid(padx=10, pady=10)

        row = 0
        col = 0
        width=50

        header = Header(master, "Commit Imported Sales")
        header.grid(row=row, column=col, columnspan=4)

        row+=1
        col=0
        tk.Label(master, text='Date:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.name = LabelBox(master, self.table, 'date')
        self.name.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.name.get_line())

        row+=1
        col=0
        #col+=1
        tk.Label(master, text='Customer:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.customer_ID = LabelBox(master, self.table, 'customer_ID', width=width)#, readonly=True)
        self.customer_ID.grid(row=row, column=col, sticky=(tk.W))
        self.customer_ID.set_id('Customer', 'name')
        self.form_contents.append(self.customer_ID.get_line())

        row+=1
        col=0
        #col+=1
        tk.Label(master, text='Gross:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        gross = LabelBox(master, self.table, 'gross')
        gross.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(gross.get_line())

        row+=1
        col=0
        tk.Label(master, text='Fees:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        fees = LabelBox(master, self.table, 'fees')
        fees.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(fees.get_line())

        row+=1
        col=0
        #col+=1
        tk.Label(master, text='Shipping:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        shipping = LabelBox(master, self.table, 'shipping')
        shipping.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(shipping.get_line())

        row+=1
        col=0
        tk.Label(master, text='Status:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.status_ID = ComboBox(master, self.table, 'status_ID')
        self.status_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.status_ID.get_line())

        # row+=1
        # col=0
        # tk.Label(master, text='Committed:').grid(row=row, column=col, sticky=(tk.E))
        # col+=1
        # self.committed_ID = ComboBox(master, self.table, 'committed_ID')
        # self.committed_ID.grid(row=row, column=col, sticky=(tk.W))
        # self.form_contents.append(self.committed_ID.get_line())

        row+=1
        col=0
        #col+=1
        tk.Label(master, text='Notes:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        notes = NotesBox(master, self.table, 'notes')
        notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(notes.get_line())

        row+=1
        col=0
        buttons = ButtonBox(master, 'sales_form_import', disable_select=True, disable_new=True)
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
        buttons = SingleButtonBox(master, 'import_sales_form_commit', 'Commit')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(self.commit_sales)

        self.row = row
        self.notebook_callback()

    @debugger
    def get_id_list(self):
        '''
        Return the id list where only the records that have not been committed
        are in the list. This will change when a record is deleted or committed.
        '''
        return self.data.get_id_list(self.table, 'committed = false')

    @debugger
    def notebook_callback(self):
        self.id_list = self.get_id_list()
        #self.committed_ID.populate('CommittedState', 'name')
        if not self.id_list is None:
            self.status_ID.populate('SaleStatus', 'name')
            self.set_form()
        else:
            mb.showinfo('INFO', 'There are no uncommitted sales records to view.')

    @debugger
    def commit_sales(self):
        '''
        Import sale records
        '''
        if not self.id_list is None:
            CommitSale(self.form_contents, self.id_list[self.crnt_index])
        self.set_form()

# CREATE TABLE PurchaseRecord
#         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         date TEXT NOT NULL,
#         raw_import_ID INTEGER,
#         vendor_ID INTEGER NOT NULL,
#         status_ID INTEGER NOT NULL,
#         type_ID INTEGER,
#         transaction_uuid TEXT NOT NULL,
#         gross REAL NOT NULL,
#         tax REAL,
#         shipping REAL,
#         notes TEXT,
#         committed_ID INTEGER NOT NULL);
class ImportPurchases(SetupFormBase):
    '''
    Implement reviewing all of the imported sales.
    '''
    def __init__(self, master, *args, **kargs):

        super().__init__(master, 'PurchaseRecord', empty_ok=True, *args, **kargs)
        self.form_contents = []
        master.grid(padx=10, pady=10)

        row = 0
        col = 0
        width=50

        header = Header(master, "Commit Imported Purchases")
        header.grid(row=row, column=col, columnspan=4)

        row+=1
        col=0
        tk.Label(master, text='Date:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.name = LabelBox(master, self.table, 'date')
        self.name.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.name.get_line())

        row+=1
        col=0
        #col+=1
        tk.Label(master, text='Vendor:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.vendor_ID = LabelBox(master, self.table, 'vendor_ID', width=width)#, readonly=True)
        self.vendor_ID.grid(row=row, column=col, sticky=(tk.W))
        self.vendor_ID.set_id('Vendor', 'name')
        self.form_contents.append(self.vendor_ID.get_line())


        row+=1
        col=0
        #col+=1
        tk.Label(master, text='Gross:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        gross = LabelBox(master, self.table, 'gross')
        gross.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(gross.get_line())

        row+=1
        col=0
        #col+=1
        tk.Label(master, text='Tax:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        tax = LabelBox(master, self.table, 'tax')
        tax.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(tax.get_line())

        row+=1
        col=0
        #col+=1
        tk.Label(master, text='Shipping:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        shipping = LabelBox(master, self.table, 'shipping')
        shipping.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(shipping.get_line())

        row+=1
        col=0
        #col+=1
        tk.Label(master, text='Purchase Type:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.type_ID = ComboBox(master, self.table, 'type_ID')
        self.type_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.type_ID.get_line())

        #row+=1
        #col=0
        col+=1
        tk.Label(master, text='Purchase Status:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.status_ID = ComboBox(master, self.table, 'status_ID')
        self.status_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.status_ID.get_line())

        # row+=1
        # col=0
        # #col+=1
        # tk.Label(master, text='Committed:').grid(row=row, column=col, sticky=(tk.E))
        # col+=1
        # self.committed_ID = ComboBox(master, self.table, 'committed_ID')
        # self.committed_ID.grid(row=row, column=col, sticky=(tk.W))
        # self.form_contents.append(self.committed_ID.get_line())

        row+=1
        col=0
        #col+=1
        tk.Label(master, text='Notes:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        notes = NotesBox(master, self.table, 'notes')
        notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(notes.get_line())

        row+=1
        col=0
        #col+=1
        buttons = ButtonBox(master, 'purchases_form_import', disable_select=True, disable_new=True)
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
        buttons = SingleButtonBox(master, 'import_purchase_form_commit', 'Commit')
        buttons.grid(row=row, column=col, columnspan=4)
        buttons.register_events(self.commit_purchases)

        self.row = row
        self.notebook_callback()

    @debugger
    def get_id_list(self):
        '''
        Return the id list where only the records that have not been committed
        are in the list. This will change when a record is deleted or committed.
        '''
        return self.data.get_id_list(self.table, 'committed = false')

    @debugger
    def notebook_callback(self):
        self.id_list = self.get_id_list()
        #self.committed_ID.populate('CommittedState', 'name')
        if not self.id_list is None:
            self.status_ID.populate('PurchaseStatus', 'name')
            self.type_ID.populate('PurchaseType', 'name')
            self.set_form()
        else:
            mb.showinfo('INFO', 'There are no uncommitted sales records to view.')

    @debugger
    def commit_purchases(self):
        '''
        Import sales records
        '''
        # Validate that the commit has a valid type of cogs or other.
        if not self.id_list is None:
            CommitPurchase(self.form_contents, self.id_list[self.crnt_index])
        self.set_form()