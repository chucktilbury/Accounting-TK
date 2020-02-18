import tkinter as tk
from tkinter import messagebox as mb
from utility import Logger, debugger
from database import  Database
from dialogs import SelectItem


class SetupFormBase(object):
    '''
    This class provides common services for forms in the setup notebook.
    '''

    def __init__(self, master, table, empty_ok=False):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Setup Dialog start constructor")

        self.master = master
        self.table = table
        self.empty_ok = empty_ok
        self.data = Database.get_instance()

        self.id_list = self.get_id_list()
        self.crnt_index = 0

    @debugger
    def get_id_list(self):
        '''
        This method exists so that a form can manage a smaller set of
        records than every single one. To do that, override this default
        method in the form class.
        '''
        return self.data.get_id_list(self.table)

    @debugger
    def select_button_command(self):
        self.id_list = self.get_id_list()
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
        if not self.id_list is None:
            self.get_form()

    @debugger
    def del_button_command(self):
        ''' Delete the item given in the form from the database '''
        if not self.id_list is None:
            val = mb.askokcancel("Sure?", "Are you sure you want to delete item from %s?"%(self.table))
            if val:
                self.logger.info("Deleting item %d from %s"%(self.id_list[self.crnt_index], self.table))
                self.data.delete_row(self.table, self.id_list[self.crnt_index])
                self.data.commit()
                self.id_list = self.get_id_list()
                if self.crnt_index >= len(self.id_list):
                    self.crnt_index -= 1
                self.set_form()

    @debugger
    def next_btn_command(self):
        ''' Go to the next item in the form table '''
        if not self.id_list is None:
            self.crnt_index += 1
            if self.crnt_index >= len(self.id_list):
                self.crnt_index = len(self.id_list)-1

            self.set_form()

    @debugger
    def prev_btn_command(self):
        ''' Go to the previous item in the table '''
        if not self.id_list is None:
            self.crnt_index -= 1
            if self.crnt_index < 0:
                self.crnt_index = 0

            self.set_form()

    @debugger
    def clear_form(self):
        '''
        Clear the form.
        '''
        for item in self.form_contents:
            print(item)
            item['self'].clear()
        self.id_list = None

    @debugger
    def set_form(self):#, row_id):
        '''
        Read the database and place the data in the form.
        '''
        if self.id_list is None:
            return

        try:
            self.id_list = self.get_id_list()
            row_id = self.id_list[self.crnt_index]
        except IndexError:
            if not self.empty_ok:
                self.logger.info('No records defined for table \'%s\''%(self.table))
                mb.showinfo('Records', 'There are no records available for this form: \'%s\".'%(self.table))
            self.clear_form()
            return

        row = self.data.get_row_by_id(self.table, row_id)
        if row is None:
            if not self.empty_ok:
                self.logger.info('No records defined for table \'%s\''%(self.table))
                mb.showinfo('Records', 'There are no records available for this table: \'%s\'.'%(self.table))
            self.clear_form()
            return

        print(self.form_contents)
        for item in self.form_contents:
            if not item['hasid'] is None:
                # swap in the value that the ID points to rather than the actual ID
                item['hasid']['id'] = int(row[item['column']])
                tmp_row = self.data.get_row_by_id(item['hasid']['table'], item['hasid']['id'])
                item['self'].write(tmp_row[item['hasid']['column']])
            else:
                item['self'].write(row[item['column']])

    @debugger
    def get_form(self):
        '''
        Read the form and place the data in the database.
        '''
        if self.id_list is None:
            return

        row = {}
        for item in self.form_contents:
            if not item['hasid'] is None:
                # If in the future, forms that require a writable ID in the
                # form is implemented, then this line will have to change.
                row[item['column']] = item['hasid']['id']
            else:
                row[item['column']] = item['self'].read()

        if self.id_list is None:
            self.data.insert_row(self.table, row)
        else:
            row_id = self.id_list[self.crnt_index]
            self.data.update_row_by_id(self.table, row, row_id)

        self.id_list = self.get_id_list()

