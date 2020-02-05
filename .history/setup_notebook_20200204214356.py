

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

        notebook.show_frame('Contacts')

