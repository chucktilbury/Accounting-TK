
from tkinter import ttk
from tkinter import messagebox
import tkinter

from utility import Logger, debugger, raise_event, register_event
from database import  Database
from dialogs import BaseDialog

class Transactions(BaseDialog):
    '''
    This is the main frame that "contains" the other frames.
    '''

    @debugger
    def body(self, master):

        self.title("Transactions")

        self.data = Database.get_instance()

        frame = tkinter.Frame(master, bd=1, relief=tkinter.RIDGE)
        frame.grid(row=0, column=0, padx=4, pady=7)
        tkinter.Label(frame, text="Transactions", font=("Helvetica", 14)).grid(row=0, column=0)
        tkinter.Button(frame, text="New Transaction", width=24, command=self.new_button_command).grid(row=1, column=0)
        tkinter.Button(frame, text="Edit Transaction", width=24, command=self.edit_button_command).grid(row=2, column=0)
        tkinter.Button(frame, text="Delete Transaction", width=24, command=self.del_button_command).grid(row=3, column=0)

    @debugger
    def new_button_command(self):
        NewTransaction(self.master)

    @debugger
    def edit_button_command(self):
        EditTransaction(self.master)

    @debugger
    def del_button_command(self):
        DeleteTransaction(self.master)

class NewTransaction(BaseDialog):

    @debugger
    def body(self, master):
        self.title("New Transaction")

class EditTransaction(BaseDialog):

    @debugger
    def body(self, master):
        self.title("Edit Transaction")

class DeleteTransaction(BaseDialog):

    @debugger
    def body(self, master):
        self.title("Delete Transaction")

