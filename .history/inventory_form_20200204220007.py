
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter

from utility import Logger, debugger, raise_event, register_event
from database import  Database
from setup_form import SetupFormBase

# CREATE TABLE InventoryItem
#         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         stock_num INTEGER NOT NULL,
#         # date_added REAL NOT NULL,
#         name TEXT NOT NULL,
#         description TEXT,
#         note TEXT,
#         num_stock INTEGER NOT NULL,
#         price REAL NOT NULL,
#         cost REAL NOT NULL);


class Inventory(SetupFormBase):
    '''
    This is the main frame that "contains" the other frames.
    '''

    @debugger
    def __init__(self, master):

        self.title("Inventory")

        row = 0
        col = 0
        padx = 6
        pady = 2
        width = 54

        frame = tkinter.Frame(master, bd=1, relief=tkinter.RIDGE)
        frame.grid(row=0, column=0, padx=4, pady=7)
        tkinter.Label(frame, text="Setup Inventory", font=("Helvetica", 14)).grid(row=row, column=col, columnspan=4)

        #######################

        row += 1
        col = 1
        tkinter.Button(frame, text='Next', command=self.next_btn_command).grid(padx=padx, row=row, column=col)
        col+= 2
        tkinter.Button(frame, text='Prev', command=self.prev_btn_command).grid(padx=padx, row=row, column=col)

        ######################
        row += 1
        col = 0
        tkinter.Label(frame, text='Name:').grid(row=row, column=col)
        self.name = tkinter.StringVar(master)
        col += 1
        tkinter.Entry(frame, textvariable=self.name).grid(
                                        row=row, column=col, padx=padx, pady=pady, sticky=tkinter.W)


        ######################
        #row += 1
        col += 1
        tkinter.Label(frame, text='Stock Num:').grid(row=row, column=col)
        self.stock_num = tkinter.StringVar(master)
        col += 1
        tkinter.Entry(frame, textvariable=self.stock_num).grid(
                                        row=row, column=col, padx=padx, pady=pady, sticky=tkinter.W)

        ######################
        row += 1
        col = 0
        tkinter.Label(frame, text='Price:').grid(row=row, column=col)
        self.price = tkinter.StringVar(master)
        col += 1
        tkinter.Entry(frame, textvariable=self.price).grid(
                                        row=row, column=col, padx=padx, pady=pady, sticky=tkinter.W)

        #row += 1
        col += 1
        tkinter.Label(frame, text='Cost:').grid(row=row, column=col)
        self.cost = tkinter.StringVar(master)
        col += 1
        tkinter.Entry(frame, textvariable=self.cost).grid(
                                        row=row, column=col, padx=padx, pady=pady, sticky=tkinter.W)

        #######################
        row += 1
        col = 0
        tkinter.Label(frame, text='Description:').grid(row=row, column=col)
        self.description = tkinter.StringVar(master)
        col+= 1
        tkinter.Entry(frame, textvariable=self.description, width=width).grid(
                                        row=row, column=col, padx=padx, pady=pady, columnspan=3, sticky=tkinter.W)

        #######################
        row += 1
        tkinter.Label(frame, text='Notes:').grid(row=row)
        frame2 = tkinter.Frame(frame, bd=1, relief=tkinter.RIDGE)
        frame2.grid(row=row, column=1, rowspan=6, columnspan=3, padx=padx, pady=pady)
        self.notes = tkinter.Text(frame2, height=6, width=60)
        self.sb = tkinter.Scrollbar(frame2)
        self.sb.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.notes.pack(side=tkinter.LEFT)
        self.sb.config(command=self.notes.yview)
        self.notes.config(yscrollcommand=self.sb.set)
        self.notes.insert(tkinter.END, '')


        #######################
        row += 6
        col = 0
        tkinter.Label(frame, text='Stock:').grid(row=row, column=col)
        self.num_stock = tkinter.StringVar(master)
        col+= 1
        tkinter.Entry(frame, textvariable=self.num_stock).grid(
                                        row=row, column=col, padx=padx, pady=pady, sticky=tkinter.W)

        #######################

        frame1 = tkinter.Frame(master, bd=1, relief=tkinter.RIDGE)
        frame1.grid(row=1, column=0)
        col = 0
        row = 1
        tkinter.Button(frame1, text="Select", command=self.select_button_command).grid(padx=padx, row=row, column=col)
        col+= 1
        tkinter.Button(frame1, text="New", command=self.new_button_command).grid(padx=padx, row=row, column=col)
        col+= 1
        tkinter.Button(frame1, text="Save", command=self.save_button_command).grid(padx=padx, row=row, column=col)
        col+= 1
        tkinter.Button(frame1, text="Delete", command=self.del_button_command).grid(padx=padx, row=row, column=col)

    ####################################
    #
    # List of form vars
    #
    # self.name
    # self.stock_num
    # self.price
    # self.cost
    # self.description
    # self.notes
    # self.num_stock
    #
    ###################################

    @debugger
    def clear_form(self):
        self.name.set('')
        self.stock_num.set('')
        self.price.set('')
        self.cost.set('')
        self.num_stock.set('')
        self.description.set('')
        self.notes.delete('1.0', tkinter.END)


    @debugger
    def set_form(self, row_id):
        ''' Read the database and put the item given by the ID into the form '''

        row = self.data.get_row_by_id('InventoryItem', row_id)
        if row is None:
            return True

        self.name.set(row['name'])
        self.stock_num.set(row['stock_num'])
        self.price.set(row['price'])
        self.cost.set(row['cost'])
        self.num_stock.set(row['num_stock'])
        self.description.set(row['description'])
        self.notes.delete('1.0', tkinter.END)
        if not row['notes'] is None:
            self.notes.insert(tkinter.END, row['notes'])

        return False

    @debugger
    def get_form(self):
        ''' Read the form and save it to the database '''
        row = {'name': self.name.get(),
             'stock_num': self.stock_num.get(),
             'price': self.price.get(),
             'cost': self.cost.get(),
             'num_stock': self.num_stock.get(),
             'description': self.description.get(),
             'notes': self.notes.get(1.0, tkinter.END)}

        if self.data.if_rec_exists('InventoryItem', 'name', self.name.get()):
            id = self.data.get_id_by_name('InventoryItem', self.name.get())
            self.data.update_row_by_id('InventoryItem', row, id)
        else:
            self.data.insert_row('InventoryItem', row)

