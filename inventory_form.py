
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase
from form_widgets import *

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

        try:
            self.set_form(self.crnt_index)
        except IndexError:
            self.logger.info('No records defined for table \'%s\''%(self.table))

