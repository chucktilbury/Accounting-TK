import tkinter as tk
from tkinter import messagebox as mb
from utility import Logger, debugger
from database import  Database
from dialogs import SelectItem


class SetupFormBase(object):
    '''
    This class provides common services for forms in the setup notebook.
    '''

    def __init__(self, master, table):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Setup Dialog start constructor")

        self.master = master
        self.table = table
        self.data = Database.get_instance()

        self.id_list = self.data.get_id_list(self.table)
        self.crnt_index = 0

    @debugger
    def select_button_command(self):
        self.id_list = self.data.get_id_list(self.table)
        sel = SelectItem(self.master, self.table)

        #if not hasattr(sel, 'item_id'):
        if sel.item_id == -1:
            self.logger.debug('Select dialog was canceled')
        elif sel.item_id == 0:
            self.logger.debug('Select dialog item was not found')
        else:
            try:
                self.logger.debug('Select dialog item selected = %d'%(sel.item_id))
                self.crnt_index = self.id_list.index(sel.item_id)
                self.set_form()
            except TypeError:
                mb.showerror('ERROR', 'No record was selected. (no records are available?)')

    @debugger
    def new_button_command(self):
        ''' Clear the form '''
        self.clear_form()

    @debugger
    def save_button_command(self):
        ''' Save the form to the database '''
        if not self.name.read() == '':
            self.get_form()
            self.id_list = self.data.get_id_list(self.table)
        else:
            mb.showerror('Error', 'Name of %s type must not be blank.'%(self.table))

    @debugger
    def del_button_command(self):
        ''' Delete the item given in the form from the database '''
        if self.name.read() == '':
            return
        val = mb.askokcancel("Sure?", "Are you sure you want to delete item \"%s\" from %s?"%(self.name.read(), self.table))
        if val:
            self.logger.info("Deleting item: \"%s\""%(self.name.read()))
            self.data.delete_row(self.table, self.id_list[self.crnt_index])
            self.data.commit()
            self.id_list = self.data.get_id_list(self.table)
            self.crnt_index = 0
            #self.set_form(self.id_list[self.crnt_index])
            self.set_form()
        else:
            self.logger.debug("Do not delete item from %s: \"%s\""%(self.name.read(), self.table))

    @debugger
    def next_btn_command(self):
        ''' Go to the next item in the form table '''
        self.crnt_index += 1
        if self.crnt_index >= len(self.id_list):
            self.crnt_index = len(self.id_list)-1

        #self.set_form(self.id_list[self.crnt_index])
        self.set_form()

    @debugger
    def prev_btn_command(self):
        ''' Go to the previous item in the table '''
        self.crnt_index -= 1
        if self.crnt_index < 0:
            self.crnt_index = 0

        #self.set_form(self.id_list[self.crnt_index])
        self.set_form()

    @debugger
    def clear_form(self):
        '''
        Clear the form.
        '''
        for item in self.form_contents:
            print(item)
            item['self'].clear()

    @debugger
    def set_form(self):#, row_id):
        '''
        Read the database and place the data in the form.
        '''
        try:
            self.id_list = self.data.get_id_list(self.table)
            row_id = self.id_list[self.crnt_index]
        except IndexError:
            self.logger.info('No records defined for table \'%s\''%(self.table))
            mb.showinfo('Records', 'There are no records available for this form: \'%s\".'%(self.table))
            return

        row = self.data.get_row_by_id(self.table, row_id)
        if row is None:
            self.logger.info('No records defined for table \'%s\''%(self.table))
            mb.showinfo('Records', 'There are no records available for this table: \'%s\'.'%(self.table))
            return

        for item in self.form_contents:
            item['self'].write(row[item['column']])

    @debugger
    def get_form(self):
        '''
        Read the form and place the data in the database. Note that this
        function requires a unique name column to function.
        '''
        row = {}
        ctrl = None

        for item in self.form_contents:
            row[item['column']] = item['self'].read()
            if item['column'] == 'name':
                ctrl = item['self']

        if not ctrl is None:
            if self.data.if_rec_exists(self.table, 'name', ctrl.read()):
                id = self.data.get_id_by_name(self.table, ctrl.read())
                self.data.update_row_by_id(self.table, row, id)
            else:
                self.data.insert_row(self.table, row)

            self.data.commit()
        else:
            mb.showerror('ERROR', 'Cannot save a table that does not have a unique name to key off of.')
