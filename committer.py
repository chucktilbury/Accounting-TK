from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database

class CommitSale:
    '''
    Commit a sale form to the database. Note that this class
    touches many of the tables in the database and they are
    all hard-coded.
    '''
    def __init__(self, form_content, id):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Commit Sale enter constructor")
        self.data = Database.get_instance()

        print('\n\n%s\n\n'%(str(form_content)))
        # extract the lines that are important for this commit
        for item in form_content:
            if item['column'] == 'customer_ID':
                customer_ID = item['hasid']['id']
            elif item['column'] == 'gross':
                gross = item['self'].read()
            elif item['column'] == 'fee':
                fee = item['self'].read()
            elif item['column'] == 'shipping':
                shipping = item['self'].read()

        # Add the gross to the Cash account
        # Add the fees to BankFees account and decrement Cash
        # Add the shipping to the ShippingCollected account and decrement Cash

        # Commit the transaction record

        # Set the committed flag and update the SalesRecord

        self.logger.debug("Commit Sale leave constructor")

class CommitPurchase:
    '''
    Commit a purchase form to the database. Note that this class
    touches many of the tables in the database and they are all
    hard-coded.
    '''
    def __init__(self, form_content, id):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Commit Purchase enter constructor")
        self.data = Database.get_instance()

        print('\n\n%s\n\n'%(str(form_content)))
        # extract the needed information from the form data

        # Subtract the gross from the Cash account
        # Add the tax to the TaxesPayed account
        # Add the shipping to the MaterialsShippingPayed account

        # Commit the transaction record

        # Set the committed flag and update the SalesRecord

        self.logger.debug("Commit Purchase leave constructor")
