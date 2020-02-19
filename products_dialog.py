import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

from dialogs import BaseDialog
from database import Database
from utility import Logger, debugger
from form_widgets import *


class LineWidget(tk.Frame):

    def __init__(self, master, line, *args, **args):
        super().__init__(master, *args, **args)
        tk.Label(self, text="%d"%(int(line))).grid(row=0, column=0)
        self.quan_str = tk.StringVar('0')
        tk.Entry(self, textvariable=self.quan_str, width=4).grid(row=0, column=1)

        self.thing = ttk.Combobox(self,


class ProductsDialog(BaseDialog):
    '''
    This dialog associates products from the inventory table with contacts in
    the Customer table. It allows tracking of what customer bought what and
    in what quantity.
    '''

    @debugger
    def body(self, master):
        self.title('Products')

        btn_frame = tk.Frame(master)
        tk.Button(master, text='ADD', command=self.add_btn_callback).grid(row=0, column=0)
        tk.Button(master, text='DEL', command=self.del_btn_callback).grid(row=0, column=1)
        btn_frame.grid(row=0, column=0, columnspan=2)

        tk.Label(master, text='')

    @debugger
    def apply(self):
        pass