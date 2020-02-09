
import tkinter as tk
from tkinter import ttk

from utility import Logger, debugger
from database import Database
from events import EventHandler

class Header(tk.Frame):
    '''
    Create the title of the form.
    '''
    def __init__(self, master, name):
        super().__init__(master)
        tk.Label(self, text=name, font=("Helvetica", 14)).grid(row=0, column=0, sticky=(tk.E, tk.W))

class EntryBox(tk.Frame):
    '''
    Implement a consistent interface to the entry widget
    '''
    def __init__(self, master, table, column, width=None, *args, **kargs):
        '''
        master = the frame to bind this frame to
        name   = the text of the label
        table  = the name of the database table that is associated with this widget
        column = the name of the column this widget associates with
        lw = label width
        cw = control width
        '''
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("EntryBox enter constructor")

        super().__init__(master, *args, **kargs)

        self.table = table
        self.column = column
        self.content = tk.StringVar(master)
        entry = tk.Entry(self, textvariable=self.content, width=width)
        entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.logger.debug("EntryBox leave constructor")

    @debugger
    def read(self):
        return self.content.get()

    @debugger
    def write(self, val):
        self.content.set(val)

    @debugger
    def clear(self):
        self.content.set('')

    @debugger
    def get_line(self):
        '''
        Return the form entry to update the form.
        '''
        return {'table': self.table, 'column':self.column, 'self':self}

class ComboBox(tk.Frame):
    '''
    Implement a Combobox. Note that this requires that the table
    that it uses to populate the list must have a column called "name".
    '''
    def __init__(self, master, table, column, *args, **kargs):
        '''
        master = the frame to bind this frame to
        name   = the text of the label
        table  = the name of the database table that is associated with this widget
        column = the name of the column this widget associates with
        lw = label width
        cw = control width
        '''
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("ComboBox enter constructor")

        super().__init__(master, *args, **kargs)

        self.table = table
        self.column = column
        self.data = Database.get_instance()

        self.content = ttk.Combobox(self)
        self.content.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.logger.debug("ComboBox leave constructor")

    @debugger
    def populate(self, table, column):
        self.content_list = self.data.populate_list(table, column)
        self.content.configure(values=self.content_list)

    @debugger
    def read(self):
        return self.content.current()+1

    @debugger
    def write(self, val):
        print(self.content_list)
        self.content.current(int(val)-1)

    @debugger
    def clear(self):
        try:
            self.content.current(0)
        except tk.TclError:
            pass

    @debugger
    def get_line(self):
        '''
        Return the form entry to update the form.
        '''
        return {'table': self.table, 'column':self.column, 'self':self}

class NotesBox(tk.Frame):
    '''
    Implement a notes widget and provide a regular interface to it, same as the
    other form widgets.
    '''
    def __init__(self, master, table, column, *args, **kargs):
        '''
        master = the frame to bind this frame to
        name   = the text of the label
        table  = the name of the database table that is associated with this widget
        column = the name of the column this widget associates with
        lw = label width
        cw = control width
        ch = control height
        '''
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("NotesBox enter constructor")

        super().__init__(master, *args, **kargs)

        self.column = column
        self.table = table
        frame2 = tk.Frame(self, bd=1, relief=tk.RIDGE)
        frame2.grid(row=0, column=1)
        self.content = tk.Text(frame2, height=10, width=70)
        self.sb = tk.Scrollbar(frame2)
        self.sb.pack(side=tk.RIGHT,fill=tk.Y)
        self.content.pack(side=tk.LEFT)
        self.sb.config(command=self.content.yview)
        self.content.config(yscrollcommand=self.sb.set)
        self.content.insert(tk.END, '')

        self.logger.debug("NotesBox leave constructor")

    @debugger
    def read(self):
        return self.content.get(1.0, tk.END)

    @debugger
    def write(self, val):
        self.content.delete('1.0', tk.END)
        if not val is None:
            self.content.insert(tk.END, val)

    @debugger
    def clear(self):
        self.content.delete('1.0', tk.END)

    @debugger
    def get_line(self):
        '''
        Return the form entry to update the form.
        '''
        return {'table': self.table, 'column':self.column, 'self':self}

class ButtonBox(tk.Frame):
    '''
    Make the button box and register the events.
    '''
    def __init__(self, master, form, *args, **kargs):
        '''
        master = The frame to bind the widgets to.
        form = Name of the form to bind the events to.
        '''
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("NotesBox enter constructor")

        super().__init__(master, *args, **kargs)

        self.form = form
        self.events = EventHandler.get_instance()
        tk.Button(self, text='Next', command=self.next_btn).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text='Prev', command=self.prev_btn).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self, text='Select', command=self.select_btn).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self, text='New', command=self.new_btn).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self, text='Save', command=self.save_btn).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self, text='Delete', command=self.delete_btn).grid(row=1, column=3, padx=5, pady=5)

    @debugger
    def register_events(self, next, prev, select, new, save, delete):
        '''
        next = callback for the next button
        prev = callback for the prev button
        select = callback for the select button
        new = callback for the new button
        save = callback for the save button
        delete = callback for the delete button
        '''
        self.events.register_event('next_btn_%s'%(self.form), next)
        self.events.register_event('prev_btn_%s'%(self.form), prev)
        self.events.register_event('select_btn_%s'%(self.form), select)
        self.events.register_event('new_btn_%s'%(self.form), new)
        self.events.register_event('save_btn_%s'%(self.form), save)
        self.events.register_event('delete_btn_%s'%(self.form), delete)

    @debugger
    def next_btn(self):
        self.events.raise_event('next_btn_%s'%(self.form))

    @debugger
    def prev_btn(self):
        self.events.raise_event('prev_btn_%s'%(self.form))

    @debugger
    def select_btn(self):
        self.events.raise_event('select_btn_%s'%(self.form))

    @debugger
    def new_btn(self):
        self.events.raise_event('new_btn_%s'%(self.form))

    @debugger
    def save_btn(self):
        self.events.raise_event('save_btn_%s'%(self.form))

    @debugger
    def delete_btn(self):
        self.events.raise_event('delete_btn_%s'%(self.form))



