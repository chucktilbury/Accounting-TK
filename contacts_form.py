import os, time
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase
#from importer import Importer
from form_widgets import *

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

        try:
            self.set_form(self.crnt_index)
        except IndexError:
            self.logger.info('No records defined for table \'%s\''%(self.table))
