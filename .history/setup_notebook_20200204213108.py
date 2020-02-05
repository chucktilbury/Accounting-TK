

from contacts_form import ContactsForm
from notebk import NoteBk


class SetupNotebook(object):

    def __init__(self, master):

        notebook = NoteBk(master, height=600, width=900)
        notebook.add_tab('Contacts')
        notebook.add_tab('Accounts')
        notebook.add_tab('Inventory')
        notebook.add_tab('Trans Types')

        ContactsForm(notebook.get_frame('Contacts'))

class SetupBase(object):
    '''
    This class provides common services for forms in the setup notebook.
    '''

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
        box = tk.Frame(self)

        w = tk.Button(box, text="Done", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        box.grid()
