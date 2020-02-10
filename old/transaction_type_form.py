
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase
from form_widgets import *

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

