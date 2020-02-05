import os, time
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database
#from tables import Tables
from setup_notebook import SetupBase
from importer import Importer

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
#         locked INTEGER NOT NULL);

class ContactsForm(SetupBase):# (SetupDialog):
    '''
    This is the main frame that "contains" the other frames.
    '''

    def __init__(self, master):

        row = 0
        col = 0
        padx = 6
        pady = 2
        width = 55

        frame = tk.Frame(master)#, bd=1, relief=tk.RIDGE)
        frame.grid(row=0, column=0, padx=4, pady=7)
        # tk.Label(frame, text="Setup Contacts", font=("Helvetica", 14)).grid(row=row, column=col)

        ######################
        # row = 0
        # col = 0
        tk.Label(frame, text='Name:').grid(row=row, column=col)
        self.name = tk.StringVar()
        col += 1
        tk.Entry(frame, textvariable=self.name, width=width).grid(columnspan=3, row=row, column=col, padx=padx, pady=pady, sticky=tk.W)

        ######################
        row += 1
        col = 0
        tk.Label(frame, text='Address1:').grid(row=row, column=col)
        self.address1 = tk.StringVar()
        col+= 1
        tk.Entry(frame, textvariable=self.address1, width=width).grid(row=row, column=col, padx=padx, pady=pady, columnspan=3, sticky=tk.W)

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=row, column=4, columnspan=2)
        tk.Button(btn_frame, text='Next', command=self.next_btn_command).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text='Prev', command=self.prev_btn_command).grid(row=0, column=0, padx=6)

        row += 1
        col = 0
        tk.Label(frame, text='Address2:').grid(row=row, column=col)
        self.address2 = tk.StringVar()
        col += 1
        tk.Entry(frame, textvariable=self.address2, width=width).grid(row=row, column=col, padx=padx, pady=pady, columnspan=3, sticky=tk.W)



        ######################
        row += 1
        col = 0
        tk.Label(frame, text='City:').grid(row=row, column=col)
        self.city = tk.StringVar()
        col+= 1
        tk.Entry(frame, textvariable=self.city).grid(row=row, column=col, padx=padx, pady=pady, sticky=tk.W)

        col+= 1
        tk.Label(frame, text='State:').grid(row=row, column=col)
        self.state = tk.StringVar()
        col+= 1
        tk.Entry(frame, textvariable=self.state).grid(row=row, column=col, padx=padx, pady=pady, sticky=tk.W)

        col+= 1
        tk.Label(frame, text='Zip Code:').grid(row=row, column=col)
        self.zip = tk.StringVar()
        col+= 1
        tk.Entry(frame, textvariable=self.zip).grid(row=row, column=col, padx=padx, pady=pady, sticky=tk.W)

        #######################
        row += 1
        col = 0
        tk.Label(frame, text='Email:').grid(row=row, column=col)
        self.email = tk.StringVar()
        col+= 1
        tk.Entry(frame, textvariable=self.email).grid(row=row, column=col, padx=padx, pady=pady, sticky=tk.W)

        col+= 1
        tk.Label(frame, text='Phone:').grid(row=row, column=col)
        self.phone = tk.StringVar()
        col+= 1
        tk.Entry(frame, textvariable=self.phone).grid(row=row, column=col, padx=padx, pady=pady, sticky=tk.W)

        col+= 1
        tk.Label(frame, text='Web Site:').grid(row=row, column=col)
        self.web = tk.StringVar()
        col+= 1
        tk.Entry(frame, textvariable=self.web).grid(row=row, column=col, padx=padx, pady=pady, sticky=tk.W)

        #######################
        row += 1
        col = 0
        tk.Label(frame, text='Description:').grid(row=row, column=col)
        self.description = tk.StringVar()
        col+= 1
        tk.Entry(frame, textvariable=self.description, width=width).grid(
                                        row=row, column=col, padx=padx, pady=pady, columnspan=3, sticky=tk.W)

        ##########################
        # Populate the combo boxes
        self.country_list = self.data.populate_list('Country', 'name')
        self.type_list = self.data.populate_list('ContactType', 'name')
        self.status_list = self.data.populate_list('ContactStatus', 'name')
        self.class_list = self.data.populate_list('ContactClass', 'name')


        oldrow = row
        #######################
        #row += 1
        col = 4
        tk.Label(frame, text='Country:').grid(row=row, column=col)
        self.country = ttk.Combobox(frame, values=self.country_list)
        self.country.grid(row=row, column=col+1, padx=padx, pady=pady)
        self.country.current(0)

        row += 1
        tk.Label(frame, text='Type:').grid(row=row, column=col)
        self.type = ttk.Combobox(frame, values=self.type_list)
        self.type.grid(row=row, column=col+1, padx=padx, pady=pady)
        self.type.current(0)

        row += 1
        tk.Label(frame, text='Status:').grid(row=row, column=col)
        self.status = ttk.Combobox(frame, values=self.status_list)
        self.status.grid(row=row, column=col+1, padx=padx, pady=pady)
        self.status.current(0)

        row += 1
        tk.Label(frame, text='Class:').grid(row=row, column=col)
        self.cont_class = ttk.Combobox(frame, values=self.class_list)
        self.cont_class.grid(row=row, column=col+1, padx=padx, pady=pady)
        self.cont_class.current(1)

        row += 1
        tk.Label(frame, text='Locked:').grid(row=row, column=col)
        self.locked = tk.BooleanVar()
        tk.Checkbutton(frame, var=self.locked).grid(row=row, column=col+1, sticky=tk.W)
        #ttk.Combobox(frame).grid(row=row, column=col+1, padx=padx, pady=pady)

        #######################
        row = oldrow + 1
        tk.Label(frame, text='Notes:').grid(row=row, column=0)
        frame2 = tk.Frame(frame, bd=1, relief=tk.RIDGE)
        frame2.grid(row=row, column=1, rowspan=4, columnspan=3, padx=padx, pady=pady)
        self.notes = tk.Text(frame2, height=6, width=60)
        self.sb = tk.Scrollbar(frame2)
        self.sb.pack(side=tk.RIGHT,fill=tk.Y)
        self.notes.pack(side=tk.LEFT)
        self.sb.config(command=self.notes.yview)
        self.notes.config(yscrollcommand=self.sb.set)
        self.notes.insert(tk.END, '')

        #######################

        row += 50
        frame1 = tk.Frame(frame, bd=1, relief=tk.RIDGE)
        frame1.grid(row=row, column=0, padx=5, pady=5, columnspan=7)
        col = 0
        row = 1
        tk.Button(frame1, text="Select", command=self.select_button_command).grid(padx=padx, row=row, column=col)
        col+= 1
        tk.Button(frame1, text="New", command=self.new_button_command).grid(padx=padx, row=row, column=col)
        col+= 1
        tk.Button(frame1, text="Save", command=self.save_button_command).grid(padx=padx, row=row, column=col)
        col+= 1
        tk.Button(frame1, text="Delete", command=self.del_button_command).grid(padx=padx, row=row, column=col)
        col+= 1
        tk.Button(frame1, text="Import", command=self.import_button_command).grid(padx=padx, row=row, column=col)

        #super().__init__(master)
        self.set_form(self.crnt_index)

        self.logger.debug("Setup Dialog end constructor")


    ############################
    # List of form variables
    #
    # self.name
    # self.address1
    # self.address2
    # self.city
    # self.state
    # self.zip
    # self.email
    # self.phone
    # self.web
    # self.description
    # self.notes
    # self.locked
    # self.country
    # self.type
    # self.status
    # self.cont_class
    #
    ##############################

    @debugger
    def import_button_command(self):
        # Show the file select dialog and import only the contacts from it.
        # If the first and last names exist, then ignore the record.
        imp = Importer()
        imp.import_all()

    @debugger
    def clear_form(self):
        # simply clear the form
        self.country.current(0)
        self.type.current(0)
        self.status.current(0)
        self.cont_class.current(1)

        self.name.set('')
        self.address1.set('')
        self.address2.set('')
        self.city.set('')
        self.state.set('')
        self.zip.set('')
        self.email.set('')
        self.phone.set('')
        self.web.set('')
        self.description.set('')
        self.notes.delete('1.0', tk.END)
        self.locked.set(False)

    @debugger
    def set_form(self, db_index):
        '''
        Set the form from the database
        '''
        row = self.data.get_row_by_id('Contacts', db_index)
        if row is None:
            return True

        self.country.current(row['country_ID']-1)
        self.type.current(row['type_ID']-1)
        self.status.current(row['status_ID']-1)
        self.cont_class.current(row['class_ID']-1)

        # types are pretty good.
        self.name.set(row['name'])
        self.address1.set(row['address1'])
        self.address2.set(row['address2'])
        self.city.set(row['city'])
        self.state.set(row['state'])
        self.zip.set(row['zip'])
        self.email.set(row['email_address'])
        self.phone.set(row['phone_number'])
        self.web.set(row['web_site'])
        self.description.set(row['description'])
        self.notes.delete('1.0', tk.END)
        if not row['notes'] is None:
            self.notes.insert(tk.END, row['notes'])
        self.locked.set(row['locked'])

        return False

    @debugger
    def get_form(self):
        '''
        Read the form and save it to the database
        '''
        row = {'date_created': time.strftime('%m/%d/%Y', time.localtime()),
            'name': self.name.get(),
            'address1': self.address1.get(),
            'address2': self.address2.get(),
            'state': self.state.get(),
            'city': self.city.get(),
            'zip': self.zip.get(),
            'email_address': self.email.get(),
            'phone_number': self.phone.get(),
            'description': self.description.get(),
            'web_site': self.web.get(),
            'notes': self.notes.get(1.0, tk.END),
            'country_ID': self.country.current()+1,
            'type_ID': self.type.current()+1,
            'status_ID': self.status.current()+1,
            'class_ID': self.cont_class.current()+1,
            'locked': self.locked.get()}

        if self.data.if_rec_exists('Contacts', 'name', self.name.get()):
            id = self.data.get_id_by_name('Contacts', self.name.get())
            self.data.update_row_by_id('Contacts', row, id)
        else:
            self.data.insert_row('Contacts', row)

        self.data.commit()

