from tkinter import messagebox as mbox
from tkinter import ttk
import tkinter
import math
from utility import Logger, debugger
from database import Database
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
class BaseDialog(tkinter.Toplevel):
    '''
    This class provides common services to simple data dialogs.
    '''

    def __init__(self, parent):# , title = None):

        #init the logger
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Base Dialog start constructor")

        tkinter.Toplevel.__init__(self, parent)
        self.transient(parent)

        self.parent = parent

        self.result = None
        # get a copy of the data_store for the children
        #self.data_store = DataStore.get_instance()

        body = tkinter.Frame(self)
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
        box = tkinter.Frame(self)

        w = tkinter.Button(box, text="OK", width=10, command=self.ok, default=tkinter.ACTIVE)
        w.pack(side=tkinter.LEFT, padx=5, pady=5)
        w = tkinter.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tkinter.LEFT, padx=5, pady=5)

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
        self.logger.debug("enter constructer")

        self.top = tkinter.Toplevel(parent)
        self.tx = tkinter.Text(self.top, height=25, width=80)
        self.sb = tkinter.Scrollbar(self.top)
        self.sb.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.tx.pack(side=tkinter.LEFT)
        self.sb.config(command=self.tx.yview)
        self.tx.config(yscrollcommand=self.sb.set)
        self.tx.insert(tkinter.END, help_text)
        self.tx.config(state='disabled')

        self.logger.debug("leave constructer")

###############################################################################
class TestDialog(BaseDialog):
    '''
    This implements a minimum dialog using the Base Dialog class.
    '''

    @debugger
    def body(self, master):

        tkinter.Label(master, text="First:").grid(row=0)
        tkinter.Label(master, text="Second:").grid(row=1)

        self.e1 = tkinter.Entry(master)
        self.e2 = tkinter.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    @debugger
    def validate(self):
        try:
            self.first = int(self.e1.get())
            self.second = int(self.e2.get())
        except ValueError as e:
            self.logger.error("Cannot convert values to ints: (%s, %s)"%(self.e1.get(), self.e2.get()))
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
        self.tx = tkinter.Text(master, height=25, width=80)
        self.sb = tkinter.Scrollbar(master)
        self.sb.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.tx.pack(side=tkinter.LEFT)
        self.sb.config(command=self.tx.yview)
        self.tx.config(yscrollcommand=self.sb.set)
        #self.notes = self.data_store.get_notes()
        self.tx.insert(tkinter.END, self.notes)

    @debugger
    def validate(self):
        self.notes = self.tx.get('1.0', tkinter.END)
        return True

    @debugger
    def apply(self):
        #self.data_store.set_notes(self.notes)
        pass

class SelectItem(BaseDialog):
    '''
    Create a list of items called 'name' from a table and return the database
    ID of the item in item_id.
    '''

    def __init__(self, master, table, thing=None):

        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug('SelectItem enter constructor')
        self.table = table
        if thing is None:
            self.thing = 'Item'
        else:
            self.thing = thing

        self.item_id = -1
        super().__init__(master)
        self.wait_window(self)
        self.logger.debug('SelectItem leave constructor')

    @debugger
    def body(self, master):
        self.title("Select %s"%(self.thing))
        self.data = Database.get_instance()

        padx = 6
        pady = 2

        frame = tkinter.Frame(master, bd=1, relief=tkinter.RIDGE)
        frame.grid(row=0, column=0, padx=4, pady=7)
        tkinter.Label(frame, text="Select %s"%(self.thing), font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2)

        ######################
        # Populate the combo boxes
        lst = self.data.populate_list(self.table, 'name')
        lst.sort()

        ######################
        # Show the boxes
        tkinter.Label(frame, text='Name:').grid(row=1, column=0)
        self.cbb = ttk.Combobox(frame, values=lst)
        self.cbb.grid(row=1, column=1, padx=padx, pady=pady)
        self.cbb.current(0)

    @debugger
    def validate(self):
        # Since the name was selected from the list, there is no need to
        # validate.
        return True

    @debugger
    def apply(self):
        ''' Populate the form with the selected data. '''
        id = self.data.get_id_by_name(self.table, self.cbb.get())
        self.item_id = id

class SetupDialog(BaseDialog):
    '''
    This class implements the logic of the setup dialogs.
    '''

    def __init__(self, master, table):

        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Setup Dialog start constructor")

        self.table = table
        self.data = Database.get_instance()
        self.name = tkinter.StringVar() #WARNING: This must be overridden by the child class

        self.id_list = self.data.get_id_list(self.table)
        self.crnt_index = 1

        super().__init__(master)
        self.set_form(self.crnt_index)

        self.logger.debug("Setup Dialog end constructor")

    @debugger
    def set_current(self):
        self.id_list = self.data.get_id_list(self.table)
        self.crnt_index = 1
        self.set_form(self.crnt_index)

    @debugger
    def select_button_command(self):
        sel = SelectItem(self.master, self.table)

        #if not hasattr(sel, 'item_id'):
        if sel.item_id == -1:
            self.logger.debug('Select dialog was canceled')
        elif sel.item_id == 0:
            self.logger.debug('Select dialog item was not found')
        else:
            self.logger.debug('Select dialog item selected = %d'%(sel.item_id))
            self.crnt_index = self.id_list.index(sel.item_id)
            self.set_form(self.id_list[self.crnt_index])

    @debugger
    def new_button_command(self):
        ''' Clear the form '''
        self.clear_form()

    @debugger
    def save_button_command(self):
        ''' Save the form to the database '''
        if not self.name.get() == '':
            self.get_form()
            self.id_list = self.data.get_id_list(self.table)
        else:
            mbox.showerror('Error', 'Name of %s type must not be blank.'%(self.table))

    @debugger
    def del_button_command(self):
        ''' Delete the item given in the form from the database '''
        if self.name.get() == '':
            return
        val = mbox.askokcancel("Sure?", "Are you sure you want to delete item \"%s\" from %s?"%(self.name.get(), self.table))
        if val:
            self.logger.info("Deleting item: \"%s\""%(self.name.get()))
            self.data.delete_row(self.table, self.id_list[self.crnt_index])
            self.data.commit()
            self.id_list = self.data.get_id_list(self.table)
            self.crnt_index = self.id_list[0]
            self.set_form(self.id_list[self.crnt_index])
        else:
            self.logger.debug("Do not delete item from %s: \"%s\""%(self.name.get(), self.table))

    @debugger
    def next_btn_command(self):
        ''' Go to the next item in the form table '''
        self.crnt_index += 1
        if self.crnt_index >= len(self.id_list):
            self.crnt_index = len(self.id_list)-1

        self.set_form(self.id_list[self.crnt_index])

    @debugger
    def prev_btn_command(self):
        ''' Go to the previous item in the table '''
        self.crnt_index -= 1
        if self.crnt_index < 0:
            self.crnt_index = 0

        self.set_form(self.id_list[self.crnt_index])

    @debugger
    def buttonbox(self):
        box = tkinter.Frame(self)

        w = tkinter.Button(box, text="Done", width=10, command=self.cancel)
        w.pack(side=tkinter.LEFT, padx=5, pady=5)

        box.grid()

    @debugger
    def clear_form(self):
        raise Exception("Clear Form function must have override in child class.")

    @debugger
    def set_form(self, index):
        raise Exception("Set Form function must have override in child class.")

    @debugger
    def get_form(self):
        raise Exception("Get Form function must have override in child class.")

