
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter

from utility import Logger, debugger
from database import  Database
from setup_form import SetupFormBase

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

        super().__init__('Account')

        row = 0
        col = 0
        padx = 6
        pady = 2
        width = 54
        self.master = master

        frame = tkinter.Frame(master, bd=1, relief=tkinter.RIDGE)
        frame.grid(row=0, column=0, padx=4, pady=7)
        tkinter.Label(frame, text="Setup Accounts", font=("Helvetica", 14)).grid(row=row, column=col, columnspan=4)

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
        self.type_list = self.data.populate_list('AccountTypes', 'name')
        tkinter.Label(frame, text='Type:').grid(row=row, column=col)
        col += 1
        self.type = ttk.Combobox(frame, values=self.type_list)
        self.type.grid(row=row, column=col, padx=padx, pady=pady, sticky=tkinter.W)
        self.type.current(0)

        col += 1
        tkinter.Label(frame, text='Total:').grid(row=row, column=col)
        self.total = tkinter.StringVar(master)
        col += 1
        tkinter.Entry(frame, textvariable=self.total).grid(
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
    # self.number
    # self.type
    # self.total
    # self.description
    # self.notes
    #
    ###################################

    @debugger
    def clear_form(self):
        self.name.set('')
        self.number.set('')
        self.type.current(0)
        self.total.set('')
        self.description.set('')
        self.notes.delete('1.0', tkinter.END)


    @debugger
    def set_form(self, row_id):
        ''' Read the database and put the item given by the ID into the form '''

        row = self.data.get_row_by_id('Account', row_id)
        if row is None:
            return True

        self.name.set(row['name'])
        self.number.set(row['number'])
        self.type.current(row['type_ID']-1)
        self.total.set(row['total'])
        self.description.set(row['description'])
        self.notes.delete('1.0', tkinter.END)
        if not row['notes'] is None:
            self.notes.insert(tkinter.END, row['notes'])

        return False

    @debugger
    def get_form(self):
        ''' Read the form and save it to the database '''
        row = {'name': self.name.get(),
             'number': self.number.get(),
             'type_ID': self.type.current()+1,
             'total': self.total.get(),
             'description': self.description.get(),
             'notes': self.notes.get(1.0, tkinter.END)}

        if self.data.if_rec_exists('Account', 'name', self.name.get()):
            id = self.data.get_id_by_name('Account', self.name.get())
            self.data.update_row_by_id('Account', row, id)
        else:
            self.data.insert_row('Account', row)

        self.data.commit()

