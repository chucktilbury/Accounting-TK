#!/usr/bin/python3

from tkinter import ttk
from tkinter import messagebox as mbox
from tkinter import filedialog
import tkinter as tk

import traceback, sys
from utility import Logger, debugger
from database import Database
from dialogs import BaseDialog
#from setup import Setup
from importer import Importer
from notebk import NoteBk
from setup_notebook import SetupNotebook

class MainFrame(tk.Frame):
    '''
    This is the main frame that "contains" the other frames.
    '''

    def __init__(self):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)

        self.master = tk.Tk()
        self.master.wm_title("Accounting")

        self.data = Database.get_instance()

        notebook = NoteBk(self.master, height=600, width=1000)
        notebook.add_tab('Sales')
        notebook.add_tab('Purchase')
        notebook.add_tab('Import')
        notebook.add_tab('Reports')
        notebook.add_tab('Queries')
        notebook.add_tab('Setup')

        # add window contents here
        SetupNotebook(notebook.get_frame('Setup'))

        # activate a frame for initial display
        notebook.show_frame('Sales')

    @debugger
    def main(self):

        try:
            self.logger.debug("start main loop")
            self.master.mainloop()
            self.logger.debug('close database')
            self.data.close()
            self.logger.debug("end main loop")

        except Exception:
            traceback.print_exception(*sys.exc_info())

class Sales(BaseDialog):

    @debugger
    def body(self, master):
        self.title("Sales")

class Purchase(BaseDialog):

    @debugger
    def body(self, master):
        self.title("Purchase")

class Import(BaseDialog):

    @debugger
    def body(self, master):
        self.title("Import")

class Queries(BaseDialog):

    @debugger
    def body(self, master):
        self.title("Queries")

class Reports(BaseDialog):

    @debugger
    def body(self, master):
        self.title("Reports")

if __name__ == "__main__":
    MainFrame().main()


    #     tk.Frame.__init__(self, self.master)
    #     self.master.protocol("WM_DELETE_WINDOW", self.close_window_command)

    #     frame = tk.Frame(self.master, bd=1, relief=tk.RIDGE)
    #     frame.grid(row=0, column=0, padx=4, pady=7)

    #     tk.Label(frame, text="Accounting", font=("Helvetica", 14)).grid(row=0, column=0)

    #     width = 24
    #     tk.Button(frame, text="Sales", width=width, command=self.sales_button_command).grid(row=1, column=0)
    #     tk.Button(frame, text="Purchase", width=width, command=self.purchase_button_command).grid(row=2, column=0)
    #     tk.Button(frame, text="Import", width=width, command=self.import_button_command).grid(row=3, column=0)
    #     tk.Button(frame, text="Reports", width=width, command=self.reports_button_command).grid(row=4, column=0)
    #     tk.Button(frame, text="Queries", width=width, command=self.queries_button_command).grid(row=5, column=0)
    #     tk.Button(frame, text="Setup", width=width, command=self.setup_button_command).grid(row=6, column=0)

    #     tk.Button(self.master, text="Quit", width=width, command=self.close_window_command).grid(row=1, column=0)


    # @debugger
    # def sales_button_command(self):
    #     Sales(self.master)

    # @debugger
    # def purchase_button_command(self):
    #     Purchase(self.master)

    # @debugger
    # def import_button_command(self):
    #     #Import(self.master)
    #     imp = Importer()
    #     imp.import_all()

    # @debugger
    # def setup_button_command(self):
    #     Setup(self.master)

    # @debugger
    # def queries_button_command(self):
    #     Queries(self.master)

    # @debugger
    # def reports_button_command(self):
    #     Reports(self.master)

    # @debugger
    # def close_window_command(self):
    #     if mbox.askokcancel("Quit", "Exit the accounting program?"):
    #         self.logger.debug('main quit')
    #         self.master.quit()
    #     else:
    #         self.logger.debug('do not quit')
