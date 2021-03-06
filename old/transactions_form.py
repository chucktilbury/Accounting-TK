
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase
from form_widgets import *

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

