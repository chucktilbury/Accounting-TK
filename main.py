#!/usr/bin/python3

from tkinter import ttk
from tkinter import messagebox as mb
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

        menubar = tk.Menu(self.master, tearoff=0)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file_menu)
        menubar.add_cascade(label='Help', menu=help_menu)

        file_menu.add_command(label='Import', command=self.do_import)
        file_menu.add_command(label='Export', command=self.do_export)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', command=self.do_quit)

        help_menu.add_command(label='Help', command=self.do_help)
        help_menu.add_command(label='About', command=self.do_about)

        notebook = NoteBk(self.master, height=700, width=1050)
        notebook.add_tab('Sales')
        notebook.add_tab('Purchase')
        notebook.add_tab('Reports')
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

    @debugger
    def do_import(self):
        '''
        Import from a CSV file
        '''

    @debugger
    def do_export(self):
        '''
        Export to a CSV file
        '''

    @debugger
    def do_quit(self):
        '''
        Quit with a prompt
        '''
        self.master.quit()

    @debugger
    def do_help(self):
        '''
        Show the help text dialog
        '''
        mb.showinfo('HELP!', 'Help me please.')

    @debugger
    def do_about(self):
        '''
        Show the About dialog
        '''
        mb.showinfo('About', 'Account according to Chuck!')


if __name__ == "__main__":
    MainFrame().main()






# class Sales(BaseDialog):

#     @debugger
#     def body(self, master):
#         self.title("Sales")

# class Purchase(BaseDialog):

#     @debugger
#     def body(self, master):
#         self.title("Purchase")

# class Import(BaseDialog):

#     @debugger
#     def body(self, master):
#         self.title("Import")

# class Queries(BaseDialog):

#     @debugger
#     def body(self, master):
#         self.title("Queries")

# class Reports(BaseDialog):

#     @debugger
#     def body(self, master):
#         self.title("Reports")

