
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


class LabelBox(tk.Frame):
    '''
    Implement a consistent interface to the entry widget
    '''
    def __init__(self, master, table, column, *args, **kargs):
        '''
        master = the frame to bind this frame to
        name   = the text of the label
        table  = the name of the database table that is associated with this widget
        column = the name of the column this widget associates with
        '''
        self.logger = Logger(self, level=Logger.INFO)
        self.logger.debug("LabelBox enter constructor")

        super().__init__(master, *args, **kargs)

        self.table = table
        self.column = column
        self.content = tk.StringVar(master)
        self.entry = tk.Label(self, textvariable=self.content)
        self.entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.row = {'table': self.table, 'column':self.column, 'self':self, 'hasid':None}
        self.logger.debug("LabelBox leave constructor")

    @debugger
    def set_id(self, table, column, id=0):
        '''
        When the column has a ID, rather than a value, use this to get the record
        that the ID references.
        '''
        self.row['hasid'] = {'table':table, 'column':column, 'id':id}
        return id

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
        return self.row

class EntryBox(tk.Frame):
    '''
    Implement a consistent interface to the entry widget
    '''
    def __init__(self, master, table, column, width=None, readonly=False, *args, **kargs):
        '''
        master = the frame to bind this frame to
        name   = the text of the label
        table  = the name of the database table that is associated with this widget
        column = the name of the column this widget associates with
        lw = label width
        cw = control width
        '''
        self.logger = Logger(self, level=Logger.INFO)
        self.logger.debug("EntryBox enter constructor")

        super().__init__(master, *args, **kargs)

        self.table = table
        self.column = column
        self.readonly = readonly
        self.content = tk.StringVar(master)
        self.entry = tk.Entry(self, textvariable=self.content, width=width)
        self.entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        if self.readonly:
            self.entry.configure(state='readonly')

        self.row = {'table': self.table, 'column':self.column, 'self':self, 'hasid':None}
        self.logger.debug("EntryBox leave constructor")

    @debugger
    def read(self):
        return self.content.get()

    @debugger
    def write(self, val):
        if self.readonly:
            self.entry.configure(state='normal')
        self.content.set(val)
        if self.readonly:
            self.entry.configure(state='readonly')

    @debugger
    def clear(self):
        self.content.set('')

    @debugger
    def get_line(self):
        '''
        Return the form entry to update the form.
        '''
        return self.row

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
        column = the name of the database column this widget associates with
        '''
        self.logger = Logger(self, level=Logger.INFO)
        self.logger.debug("ComboBox enter constructor")

        super().__init__(master, *args, **kargs)

        self.table = table
        self.column = column
        self.data = Database.get_instance()

        self.content = ttk.Combobox(self, state='readonly')
        self.content.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.row = {'table': self.table, 'column':self.column, 'self':self, 'hasid':None}
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
        return self.row

class NotesBox(tk.Frame):
    '''
    Implement a notes widget and provide a regular interface to it, same as the
    other form widgets.
    '''
    def __init__(self, master, table, column, height=20, width=60, *args, **kargs):
        '''
        master = the frame to bind this frame to
        name   = the text of the label
        table  = the name of the database table that is associated with this widget
        column = the name of the column this widget associates with
        lw = label width
        cw = control width
        ch = control height
        '''
        self.logger = Logger(self, level=Logger.INFO)
        self.logger.debug("NotesBox enter constructor")

        super().__init__(master, *args, **kargs)

        self.column = column
        self.table = table

        frame2 = tk.Frame(self, bd=1, relief=tk.RIDGE)
        frame2.grid(row=0, column=1)
        self.content = tk.Text(frame2, height=height, width=width, wrap=tk.NONE)
        self.content.insert(tk.END, '')

        # see https://www.homeandlearn.uk/tkinter-scrollbars.html
        self.vsb = tk.Scrollbar(frame2, orient=tk.VERTICAL)
        self.vsb.config(command=self.content.yview)
        self.content.config(yscrollcommand=self.vsb.set)
        self.vsb.pack(side=tk.RIGHT,fill=tk.Y)

        self.hsb = tk.Scrollbar(frame2, orient=tk.HORIZONTAL)
        self.hsb.config(command=self.content.xview)
        self.content.config(xscrollcommand=self.hsb.set)
        self.hsb.pack(side=tk.BOTTOM,fill=tk.X)

        self.content.pack(side=tk.LEFT)

        self.row = {'table': self.table, 'column':self.column, 'self':self, 'hasid':None}
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
        return self.row

class ButtonBox(tk.Frame):
    '''
    Make the button box and register the events.
    '''
    def __init__(self, master, form, disable_select=False, disable_new=False, *args, **kargs):
        '''
        master = The frame to bind the widgets to.
        form = Name of the form to bind the events to.
        '''
        self.logger = Logger(self, level=Logger.INFO)
        self.logger.debug("NotesBox enter constructor")

        super().__init__(master, *args, **kargs)

        row = 0
        col = 0

        self.form = form
        self.events = EventHandler.get_instance()
        tk.Button(self, text='Prev', command=self.prev_btn).grid(row=row, column=col, padx=5, pady=5)
        col+=1
        tk.Button(self, text='Next', command=self.next_btn).grid(row=row, column=col, padx=5, pady=5)
        if not disable_select:
            col+=1
            tk.Button(self, text='Select', command=self.select_btn).grid(row=row, column=col, padx=5, pady=5)
        if not disable_new:
            col+=1
            tk.Button(self, text='New', command=self.new_btn).grid(row=row, column=col, padx=5, pady=5)
        col+=1
        tk.Button(self, text='Save', command=self.save_btn).grid(row=row, column=col, padx=5, pady=5)
        col+=1
        tk.Button(self, text='Delete', command=self.delete_btn).grid(row=row, column=col, padx=5, pady=5)

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

class SingleButtonBox(tk.Frame):
    '''
    Make the button box and register the events.
    '''
    def __init__(self, master, form, text=None, *args, **kargs):
        '''
        master = The frame to bind the widgets to.
        form = Name of the form to bind the events to.
        '''
        self.logger = Logger(self, level=Logger.INFO)
        self.logger.debug("NotesBox enter constructor")

        super().__init__(master, *args, **kargs)

        self.form = form
        self.name = text.lower()
        self.events = EventHandler.get_instance()
        tk.Button(self, text=text, command=self.btn_callback).grid(row=1, column=2, padx=5, pady=5)
        self.logger.debug("NotesBox leave constructor")

    @debugger
    def register_events(self, save):
        '''
        save = callback for the save button
        '''
        self.events.register_event('%s_btn_callback_%s'%(self.name, self.form), save)

    @debugger
    def btn_callback(self):
        self.events.raise_event('%s_btn_callback_%s'%(self.name, self.form))

class LineWidget(tk.Frame):
    '''
    This is a special widget used to show and edit product entries for a sale
    form. It implements a single line in the list.
    '''
    def __init__(self, master, form, line, *args, **kargs):
        '''
        master = The frame to bind the widgets to.
        form = Name of the form to bind the events to.
        line = The line number of the line, displayed as a label
        '''
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Line Widget enter constructor")
        self.data = Database.get_instance()

        super().__init__(master, *args, **kargs)

        self.form = form
        self.events = EventHandler.get_instance()
        #self.data = Database.get_instance()

        self.values = self.data.populate_list('InventoryItem', 'name')
        self.values.insert(0, '') # first line is blank

        tk.Label(self, text='%d'%(int(line))).grid(row=0, column=0)
        self.quan = tk.Spinbox(self, from_=1, to=99, width=2)
        self.quan.grid(row=0, column=1, padx=5, pady=5)
        self.prod = ttk.Combobox(self, values=self.values, width=40)
        self.prod.grid(row=0, column=2)

        self.logger.debug("Line Widget leave constructor")

    @debugger
    def get_str(self):
        return self.prod.get()

    @debugger
    def read(self):
        val = self.prod.get()
        if not val is None and val != '':
            return (int(self.quan.get()), val)
        else:
            return None

    # There is no get line or write function because this is managed by the
    # LineBox widget.

class LineBox(tk.Frame):
    '''
    This is a container for the line widgets. It holds a variable number of
    line boxes and has the ability to write them all to the database when the
    write method is called.
    '''
    def __init__(self, master, form=None, *args, **kargs):
        '''
        master = The frame to bind the widgets to.
        name_id = The id of the line containing the customer to associate
        form = Name of the form to bind the events to.
        '''
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Line Widget enter constructor")

        super().__init__(master, bd=1, relief=tk.RIDGE, *args, **kargs)

        #self.name_id = int(name_id)
        self.form = form
        self.events = EventHandler.get_instance()
        self.data = Database.get_instance()
        self.line_list = []
        self.crnt_index = 0
        self.events.register_event('next_button', self.clear)
        self.events.register_event('prev_button', self.clear)

        # add button
        tk.Button(self, text="Add", command=self.add).grid(row=0, column=0)
        # reset button
        tk.Button(self, text="Reset", command=self.clear).grid(row=0, column=1)

        # add one line widget
        self.add()
        # self.row = {'table': None, 'column':None, 'self':self, 'hasid':None}
        self.logger.debug("Line Widget leave constructor")

    @debugger
    def add(self):
        '''
        Method that actually adds the line to the widget.
        '''
        line = LineWidget(self, None, self.crnt_index+1)
        line.grid(row=self.crnt_index+1, column=0, columnspan=2, padx=5)
        self.line_list.append(line)
        self.crnt_index += 1

    # @debugger
    # def get_line(self):
    #     return self.row

    @debugger
    def clear(self):
        '''
        Reset the widget to having one blank line.
        '''
        for item in self.line_list:
            item.grid_forget()
        self.line_list = []
        self.crnt_index = 0
        self.add()

    @debugger
    def read(self, sale_id):
        '''
        Read method saves the contects to the database
        '''
        for item in self.line_list:
            (quan, name) = item.read()
            if name != '':
                row = {
                    'sale_record_ID': sale_id,
                    'quantity': quan,
                    'inventory_ID': self.data.get_id_by_name('InventoryItem', name)
                }
                self.data.insert_row('ProductList', row)

        self.data.commit()

    @debugger
    def write(self):
        '''
        This function does nothing for this widget
        '''
        self.clear()