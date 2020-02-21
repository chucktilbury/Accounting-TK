from tkinter import messagebox as mbox
from tkinter import ttk
import tkinter as tk
import math
from utility import Logger, debugger
#from database import Database
#import utility
#from data_store import DataStore

help_text = """
Shop Timer
Chuck Tilbury (c) 2019

This software is open source under the MIT and BSD licenses.

-------------------------------------------
General use.
-------------------------------------------

-------------------------------------------
Saving a file
-------------------------------------------

-------------------------------------------
Loading a file
-------------------------------------------

-------------------------------------------
Reset to default settings
-------------------------------------------

"""

# see: https://effbot.org/tkinterbook/tkinter-dialog-windows.htm
class BaseDialog(tk.Toplevel):
    '''
    This class provides common services to simple data dialogs.
    '''

    def __init__(self, parent):# , title = None):

        #init the logger
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Base Dialog start constructor")

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        self.parent = parent

        self.result = None
        # get a copy of the data_store for the children

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.initial_focus.focus_set()

        #self.wait_window(self)
        self.logger.debug("Base Dialog leave constructor")

    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        return self

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        box.grid()

    #
    # standard button semantics
    @debugger
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    @debugger
    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks
    def validate(self):
        return True # override

    def apply(self):
        pass # override


###############################################################################
# Does not use BaseDialog
class helpDialog:

    def __init__(self, parent):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("enter constructor")

        self.top = tk.Toplevel(parent)
        self.tx = tk.Text(self.top, height=25, width=80)
        self.sb = tk.Scrollbar(self.top)
        self.sb.pack(side=tk.RIGHT,fill=tk.Y)
        self.tx.pack(side=tk.LEFT)
        self.sb.config(command=self.tx.yview)
        self.tx.config(yscrollcommand=self.sb.set)
        self.tx.insert(tk.END, help_text)
        self.tx.config(state='disabled')

        self.logger.debug("leave constructor")

###############################################################################
class TestDialog(BaseDialog):
    '''
    This implements a minimum dialog using the Base Dialog class.
    '''

    @debugger
    def body(self, master):

        tk.Label(master, text="First:").grid(row=0)
        tk.Label(master, text="Second:").grid(row=1)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    @debugger
    def validate(self):
        try:
            self.first = int(self.e1.get())
            self.second = int(self.e2.get())
        except ValueError as e:
            self.logger.error("Cannot convert values to an int: (%s, %s)"%(self.e1.get(), self.e2.get()))
            mbox.showerror("ERROR", "Cannot convert value to an int\n(%s, %s)"%(self.e1.get(), self.e2.get()))
            return False
        except Exception as e:
            self.logger.error("Unexpected exception while validating dialog: %s"%(str(e)))
            mbox.showerror("UNKNOWN ERROR", "Cannot convert value to an int\n(%s, %s)"%(self.e1.get(), self.e2.get()))
            return False
        return True


    @debugger
    def apply(self):
        print(self.first, self.second) # or something

###############################################################################
class NotesDialog(BaseDialog):
    '''
    Capture and store arbitrary notes.
    '''

    @debugger
    def body(self, master):
        self.title('Notes')
        self.tx = tk.Text(master, height=25, width=80)
        self.sb = tk.Scrollbar(master)
        self.sb.pack(side=tk.RIGHT,fill=tk.Y)
        self.tx.pack(side=tk.LEFT)
        self.sb.config(command=self.tx.yview)
        self.tx.config(yscrollcommand=self.sb.set)
        #self.notes = self.data_store.get_notes()
        self.tx.insert(tk.END, self.notes)

    @debugger
    def validate(self):
        self.notes = self.tx.get('1.0', tk.END)
        return True

    @debugger
    def apply(self):
        #self.data_store.set_notes(self.notes)
        pass

# this does not appear to work...
class TransientMessage(BaseDialog):

    def __init__(self, master, name=None, msg=None):

        self.msg = msg
        self.name = name

        super().__init__(master)

    @debugger
    def body(self, master):

        self.title(self.name)
        tk.Label(master, text=self.msg).grid()

