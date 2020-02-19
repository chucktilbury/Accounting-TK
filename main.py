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
from notebk import NoteBk, DummyClass
from setup_notebook import SetupNotebook
from events import EventHandler

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

        notebook = NoteBk(self.master, height=700, width=1050)
        notebook.add_tab('Sales', DummyClass)
        notebook.add_tab('Purchase', DummyClass)
        notebook.add_tab('Reports', DummyClass)
        notebook.add_tab('Setup', SetupNotebook)

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

            # ev = EventHandler.get_instance()
            # ev.dump_events()
        except Exception:
            traceback.print_exception(*sys.exc_info())

if __name__ == "__main__":
    MainFrame().main()
