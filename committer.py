import time

from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk

from utility import Logger, debugger
from database import  Database

class CommitBase:

    def __init__(self, form_content, id):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Commit Base enter constructor")
        self.data = Database.get_instance()
        self.id = id
        self.form_content = form_content

    @debugger
    def get_account(self, name):
        '''
        Returns the (id, total).
        '''
        row = self.data.get_row_list_by_col('Account', 'name', name)[0]
        total = float(row['total'])
        id = row['ID']
        return (id, total)

    @debugger
    def make_generic_entry(self, gross, to_acc, from_acc, msg):

        row = {
            'date_committed': time.strftime('%m/%d/%Y'),
            'gross':gross,
            'description':msg,
            'to_account_ID':to_acc,
            'from_account_ID':from_acc,
        }
        id = self.data.insert_row('GenericTransaction', row)

        return id

    @debugger
    def connect_sale(self, id):
        row = {
            'generic_trans_ID': id,
            'sale_trans_ID': self.id
        }
        self.data.insert_row('SGenericTransaction', row)

    @debugger
    def connect_purchase(self, id):
        row = {
            'generic_trans_ID': id,
            'purchase_trans_ID': self.id
        }
        self.data.insert_row('PGenericTransaction', row)

class CommitSale(CommitBase):
    '''
    Commit a sale form to the database. Note that this class
    touches many of the tables in the database and they are
    all hard-coded.
    '''
    def __init__(self, form_content, id):

        super().__init__(form_content, id)
        self.logger.debug("Commit Sale enter constructor")

        customer_ID = 0
        gross = 0.0
        fee = 0.0
        shipping = 0.0
        # extract the lines that are important for this commit
        for item in self.form_content:
            if item['column'] == 'customer_ID':
                customer_ID = item['hasid']['id']
            elif item['column'] == 'gross':
                gross = float(item['self'].read())
            elif item['column'] == 'fees':
                fee = float(item['self'].read())
            elif item['column'] == 'shipping':
                shipping = float(item['self'].read())

        # get the effected accounts
        (cash_id, cash_total) = self.get_account('Cash')
        (ship_id, ship_total) = self.get_account('ShippingCollected')
        (fees_id, fees_total) = self.get_account('BankFees')

        # Add the gross to the Cash account
        gid = self.make_generic_entry(gross, cash_id, None, 'moving sale into Cash account')
        self.connect_sale(gid)
        cash_total = cash_total + gross

        # Add the fees to BankFees account and decrement Cash
        gid = self.make_generic_entry(fee, fees_id, cash_id, 'moving fee out of Cash into BankFees')
        self.connect_sale(gid)
        cash_total = cash_total - fee
        fees_total = fees_total + fee

        # Add the shipping to the ShippingCollected account and decrement Cash
        gid = self.make_generic_entry(shipping, ship_id, cash_id, 'moving shipping collected out of Cash into ShippingCollected')
        self.connect_sale(gid)
        cash_total = cash_total - shipping
        ship_total = ship_total + shipping

        # Commit the amounts to the accounts
        self.data.update_row_by_id('Account', {'total':cash_total}, cash_id)
        self.data.update_row_by_id('Account', {'total':fees_total}, fees_id)
        self.data.update_row_by_id('Account', {'total':ship_total}, ship_id)

        # Set the committed flag and update the SalesRecord
        self.data.update_row_by_id('SaleRecord', {'committed':True}, id)

        self.data.commit()
        self.logger.debug("Commit Sale leave constructor")


class CommitPurchase(CommitBase):
    '''
    Commit a purchase form to the database. Note that this class
    touches many of the tables in the database and they are all
    hard-coded.
    '''
    def __init__(self, form_content, id):
        super().__init__(form_content, id)
        self.logger.debug("Commit Purchase enter constructor")

        # extract the needed information from the form data
        vendor_ID = 0
        gross = 0.0
        tax = 0.0
        shipping = 0.0
        # extract the lines that are important for this commit
        for item in form_content:
            if item['column'] == 'vendor_ID':
                customer_ID = item['hasid']['id']
            elif item['column'] == 'gross':
                gross = float(item['self'].read())
            elif item['column'] == 'tax':
                tax = float(item['self'].read())
            elif item['column'] == 'shipping':
                shipping = float(item['self'].read())
            elif item['column'] == 'type_ID':
                commit_type = item['self'].read()

        # commit types
        # cogs = 1
        # other = 2
        # unknown = 3
        # cannot commit the record if the type is "unknown"
        if commit_type == 3:
            mb.showerror("ERROR", 'Cannot commit a purchase if the type is \"unknown\". Please select \"other\" or \"cogs\" to commit the record.')
            return

        # get the effected accounts
        (cash_id, cash_total) = self.get_account('Cash')
        (cogs_id, cogs_total) = self.get_account('Materials')
        (other_id, other_total) = self.get_account('OtherExpense')
        (tax_id, tax_total) = self.get_account('TaxesPayed')
        (ship_id, ship_total) = self.get_account('MaterialsShippingPayed')
        (owner_id, owner_total) = self.get_account('OwnerCapital')

        # Subtract the gross from the Cash account
        if commit_type == 1: # cogs
            gid = self.make_generic_entry(gross, cogs_id, cash_id, 'recording a COGS purchase')
            self.connect_purchase(gid)
            cash_total = cash_total - gross
            cogs_total = cogs_total + gross
        elif commit_type == 2: # other
            gid = self.make_generic_entry(gross, other_id, cash_id, 'recording a other expense purchase')
            self.connect_purchase(gid)
            cash_total = cash_total - gross
            other_total = other_total + gross
        else: # owner
            gid = self.make_generic_entry(gross, other_id, cash_id, 'recording a owner draw purchase')
            self.connect_purchase(gid)
            cash_total = cash_total - gross
            owner_total = owner_total + gross


        # Add the tax to the TaxesPayed account
        gid = self.make_generic_entry(shipping, tax_id, None, 'recording the tax that was payed')
        self.connect_purchase(gid)
        tax_total = tax_total + tax

        # Add the shipping to the MaterialsShippingPayed account
        gid = self.make_generic_entry(shipping, ship_id, None, 'recording the shipping that was payed')
        self.connect_purchase(gid)
        ship_total = ship_total + shipping

        # Commit the account totals
        self.data.update_row_by_id('Account', {'total':cash_total}, cash_id)
        self.data.update_row_by_id('Account', {'total':tax_total}, tax_id)
        self.data.update_row_by_id('Account', {'total':ship_total}, ship_id)
        if commit_type == 1:
            self.data.update_row_by_id('Account', {'total':cogs_total}, cogs_id)
        elif commit_type == 2:
            self.data.update_row_by_id('Account', {'total':other_total}, other_id)
        else:
            self.data.update_row_by_id('Account', {'total':owner_total}, owner_id)

        # Set the committed flag and update the SalesRecord
        self.data.update_row_by_id('PurchaseRecord', {'committed':True}, id)

        self.data.commit()
        self.logger.debug("Commit Purchase leave constructor")

