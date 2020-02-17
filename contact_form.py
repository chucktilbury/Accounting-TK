from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase
from form_widgets import *
from notebk import NoteBk
from importer import Importer
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
        self.importer = Importer()

        row = 0
        col = 0
        width = 50

        header = Header(master, "Setup Customers")
        header.grid(row=row, column=col, columnspan=4)

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
        self.country_ID = ComboBox(master, self.table, 'country_ID')
        self.country_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.country_ID.get_line())

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
        self.email_status_ID = ComboBox(master, self.table, 'email_status_ID')
        self.email_status_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.email_status_ID.get_line())

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
        self.phone_status_ID = ComboBox(master, self.table, 'phone_status_ID')
        self.phone_status_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.phone_status_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Web Site:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        web_site = EntryBox(master, self.table, 'web_site')
        web_site.grid(row=row, column=col, sticky=(tk.W))
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
        tk.Label(master, text='Class:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.class_ID = ComboBox(master, self.table, 'class_ID')
        self.class_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.class_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Notes:').grid(row=row, column=0, sticky=(tk.E))
        col+=1
        notes = NotesBox(master, self.table, 'notes', height=15)
        notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(notes.get_line())

        row+=1
        col=0
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

        self.row = row
        self.notebook_callback()

    def notebook_callback(self):
        self.class_ID.populate('ContactClass', 'name')
        self.phone_status_ID.populate('PhoneStatus', 'name')
        self.email_status_ID.populate('EmailStatus', 'name')
        self.country_ID.populate('Country', 'name')
        self.set_form()

    @debugger
    def del_button_command(self):
        '''
        Delete the item given in the form from the database.
        This is an override to the parent class.
        '''
        row = self.data.get_row_list('SaleRecord', 'committed_ID = 1 and customer_ID = %d'%(self.id_list[self.crnt_index]))
        if not row is None:
            mb.showerror("ERROR", "Cannot delete the record because there are transactions committed for this customer.")
            return

        row = self.data.get_row_list('SaleRecord', 'committed_ID = 2 and customer_ID = %d'%(self.id_list[self.crnt_index]))
        #print('\n\n%s\n\n'%(str(row)))
        if not row is None:
            val = mb.askokcancel("Sure?", "There are %d uncommitted sales for this Customer. They will be deleted as well.\n\nContinue?"%(len(row)))
            if val:
                count = 0
                for item in row:
                    self.data.delete_row('SaleRecord', row[0]['ID'])
                    count += 1
                mb.showinfo('INFO', 'There were %d Sale Records deleted.'%(count))
            else:
                return

        val = mb.askokcancel("Sure?", "Are you sure you want to delete item from %s?"%(self.table))
        if val:
            self.logger.info("Deleting item %d from %s"%(self.id_list[self.crnt_index], self.table))
            self.data.delete_row(self.table, self.id_list[self.crnt_index])
            self.data.commit()
            self.id_list = self.get_id_list()
            if self.crnt_index >= len(self.id_list):
                self.crnt_index -= 1
            self.set_form()

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

        self.importer = Importer()
        row = 0
        col = 0
        width = 50

        header = Header(master, "Setup Vendors")
        header.grid(row=row, column=col, columnspan=4)

        row+=1
        col=0
        tk.Label(master, text='Name:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.name = EntryBox(master, self.table, 'name', width=width)
        self.name.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(self.name.get_line())

        row+=1
        col=0
        tk.Label(master, text='Contact:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.contact_name = EntryBox(master, self.table, 'contact_name', width=width)
        self.contact_name.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
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
        self.email_status_ID = ComboBox(master, self.table, 'email_status_ID')
        self.email_status_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.email_status_ID.get_line())

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
        self.phone_status_ID = ComboBox(master, self.table, 'phone_status_ID')
        self.phone_status_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.phone_status_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Web Site:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        web_site = EntryBox(master, self.table, 'web_site', width=width)
        web_site.grid(row=row, column=col, sticky=(tk.W), columnspan=4)
        self.form_contents.append(web_site.get_line())

        #row+=1
        #col=0
        col+=1
        tk.Label(master, text='Vendor Type:').grid(row=row, column=col, sticky=(tk.E))
        col+=1
        self.type_ID = ComboBox(master, self.table, 'type_ID')
        self.type_ID.grid(row=row, column=col, sticky=(tk.W))
        self.form_contents.append(self.type_ID.get_line())

        row+=1
        col=0
        tk.Label(master, text='Notes:').grid(row=row, column=0, sticky=(tk.E))
        col+=1
        notes = NotesBox(master, self.table, 'notes')
        notes.grid(row=row, column=col, columnspan=3, sticky=(tk.W))
        self.form_contents.append(notes.get_line())

        row+=1
        col=0
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

        self.row = row
        self.notebook_callback()

    @debugger
    def notebook_callback(self):
        self.email_status_ID.populate('EmailStatus', 'name')
        self.type_ID.populate('VendorType', 'name')
        self.phone_status_ID.populate('PhoneStatus', 'name')
        self.set_form()

    @debugger
    def del_button_command(self):
        '''
        Delete the item given in the form from the database.
        This is an override to the parent class.
        '''
        row = self.data.get_row_list('PurchaseRecord', 'committed_ID = 1 and vendor_ID = %d'%(self.id_list[self.crnt_index]))
        if not row is None:
            mb.showerror("ERROR", "Cannot delete the record because there are transactions committed for this vendor.")
            return

        row = self.data.get_row_list('PurchaseRecord', 'committed_ID = 2 and vendor_ID = %d'%(self.id_list[self.crnt_index]))
        print('\n\n%s\n\n'%(str(row)))
        if not row is None:
            val = mb.askokcancel("Sure?", "There are %d uncommitted sales for this vendor. They will be deleted as well.\n\nContinue?"%(len(row)))
            if val:
                count = 0
                for item in row:
                    self.data.delete_row('PurchaseRecord', row[0]['ID'])
                    count += 1
                mb.showinfo('INFO', 'There were %d Purchase Records deleted.'%(count))
            else:
                return

        val = mb.askokcancel("Sure?", "Are you sure you want to delete item from %s?"%(self.table))
        if val:
            self.logger.info("Deleting item %d from %s"%(self.id_list[self.crnt_index], self.table))
            self.data.delete_row(self.table, self.id_list[self.crnt_index])
            self.data.commit()
            self.id_list = self.get_id_list()
            if self.crnt_index >= len(self.id_list):
                self.crnt_index -= 1
            self.set_form()
