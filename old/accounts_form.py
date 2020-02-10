
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase
from form_widgets import *

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
