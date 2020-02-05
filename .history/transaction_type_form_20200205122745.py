
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase

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

        super().__init__("TransactionType")

        row = 0
        col = 0
        padx = 6
        pady = 2
        width = 54
        self.master = master

        frame = tkinter.Frame(master, bd=1, relief=tkinter.RIDGE)
        frame.grid(row=0, column=0, padx=4, pady=7)
        tkinter.Label(frame, text="Setup Transaction Type", font=("Helvetica", 14)).grid(row=row, column=col, columnspan=4)

        #######################

        row += 1
        col = 1
        tkinter.Button(frame, text='Prev', command=self.prev_btn_command).grid(padx=padx, row=row, column=col)
        col+= 2
        tkinter.Button(frame, text='Next', command=self.next_btn_command).grid(padx=padx, row=row, column=col)

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
        tkinter.Label(frame, text='Number:').grid(row=row, column=col)
        self.number = tkinter.StringVar(master)
        col += 1
        tkinter.Entry(frame, textvariable=self.number).grid(
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
        col = 0
        self.inc_acct_list = self.data.populate_list('Account', 'name')
        tkinter.Label(frame, text='Inc Account:').grid(row=row, column=col)
        col += 1
        self.inc_acct = ttk.Combobox(frame, values=self.inc_acct_list)
        self.inc_acct.grid(row=row, column=col, padx=padx, pady=pady, sticky=tkinter.W)
        self.inc_acct.current(0)

        col += 1
        self.dec_acct_list = self.data.populate_list('Account', 'name')
        tkinter.Label(frame, text='Dec Account:').grid(row=row, column=col)
        col += 1
        self.dec_acct = ttk.Combobox(frame, values=self.dec_acct_list)
        self.dec_acct.grid(row=row, column=col, padx=padx, pady=pady, sticky=tkinter.W)
        self.dec_acct.current(0)

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

        self.set_form(self.crnt_index)

    ####################################
    #
    # List of form vars
    #
    # self.name
    # self.number
    # self.description
    #
    ###################################

    @debugger
    def clear_form(self):
        ''' Clear the form. override from base class '''
        self.name.set('')
        self.number.set('')
        self.description.set('')
        self.dec_acct.current(0)
        self.inc_acct.current(0)

    @debugger
    def set_form(self, row_id):
        ''' Read the database and put the item given by the ID into the form '''

        row = self.data.get_row_by_id('TransactionType', row_id)
        if row is None:
            return True

        self.name.set(row['name'])
        self.number.set(row['number'])
        self.description.set(row['description'])
        self.dec_acct.current(row['dec_account_ID']-1)
        self.inc_acct.current(row['inc_account_ID']-1)

        return False

    @debugger
    def get_form(self):
        ''' Read the form and save it to the database '''
        if self.dec_acct.current() == self.inc_acct.current():
            mb.showerror('Error', 'Increment and Decrement accounts cannot be the same account.')
            return

        row = {'name': self.name.get(),
             'number': self.number.get(),
             'description': self.description.get(),
             'dec_account_ID': self.dec_acct.current()+1,
             'inc_account_ID': self.inc_acct.current()+1}

        if self.data.if_rec_exists('TransactionType', 'name', self.name.get()):
            id = self.data.get_id_by_name('TransactionType', self.name.get())
            self.data.update_row_by_id('TransactionType', row, id)
        else:
            self.data.insert_row('TransactionType', row)

        self.data.commit()

