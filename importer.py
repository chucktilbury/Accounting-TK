import csv
import sys, re, time
import tkinter
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfile
from database import Database
from utility import Logger, debugger



class Importer(object):

    def __init__(self):#, master):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        #self.master = master

        self.legend = [
            'Date',
            'Time',
            'TimeZone',
            'Name',
            'Type',
            'Status',
            'Currency',
            'Gross',
            'Fee',
            'Net',
            'FromEmail',
            'ToEmail',
            'TransactionID',
            'ShippingAddress',
            'AddressStatus',
            'ItemTitle',
            'ItemID',
            'Shipping',
            'InsuranceAmount',
            'SalesTax',
            'Option1Name',
            'Option1Value',
            'Option2Name',
            'Option2Value',
            'ReferenceTxnID',
            'InvoiceNumber',
            'CustomNumber',
            'Quantity',
            'ReceiptID',
            'Balance',
            'AddressLine1',
            'AddressLine2',
            'City',
            'State',
            'PostalCode',
            'Country',
            'Phone',
            'Subject',
            'Note',
            'CountryCode',
            'BalanceImpact']

        self.data = Database.get_instance()

    @debugger
    def import_all(self):
        ''' Perform all of the steps to import the entire CSV file '''
        self.read_all()

        data = self.get_sales()
        self.import_country_codes(data)
        self.import_customer_contacts(data)
        self.do_sales_transactions(data)

        data = self.get_purchases()
        self.import_country_codes(data)
        self.import_vendor_contacts(data)
        self.do_purchase_transactions(data)

    @debugger
    def validate_email(self, email):
        if bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email)):
            return email
        else:
            return ''

    @debugger
    def read_file(self):
        ''' Handle the file IO for the CSV file '''
        #master = tkinter.Tk()
        fh = askopenfile(mode='r', filetypes=[('Spread Sheets', '*.csv *.CSV'), ('All Files', '*')])
        if fh is None:
            return None # error or cancel

        raw = []
        reader = csv.reader(fh)

        for line in reader:
            raw.append(line)

        fh.close()
        #master.destroy()
        #print(raw)
        return (raw, fh.name)

    @debugger
    def read_all(self):
        ''' Read all of the lines in the CSV into the database '''
        raw_data = self.read_file()
        if raw_data is None:
            return 0

        raw = raw_data[0]
        name = raw_data[1]
        if self.data.if_rec_exists('ImportedFileNames', 'name', name):
            mb.showwarning('WARNING', 'File name \"%s\" has already been imported. Rename file and try again.'%(name))
            return 0
        else:
            tmp = {'name':name, 'date':time.strftime('%m/%d/%Y', time.localtime())}
            self.data.insert_row('ImportedFileNames', tmp)

        data = []
        count = 0
        for line in raw:
            tmp = {}
            for idx, item in enumerate(line):
                tmp[self.legend[idx]] = item
            data.append(tmp)

            if tmp['Status'] == 'Completed': # and tmp['Name'] != '' and tmp['Name'] != 'PayPal':
                tmp['imported_country'] = False
                tmp['imported_customer'] = False
                tmp['imported_vendor'] = False
                tmp['imported_sale'] = False
                tmp['imported_purchase'] = False
                if not self.data.if_rec_exists('RawImport', 'TransactionID', tmp['TransactionID']):
                    self.data.insert_row('RawImport', tmp)
                    count+=1
        # BUG: Import all of the completed records into the Raw Import table.
        self.data.commit()
        return count

    @debugger
    def import_country_codes(self):
        ''' Find the new country codes and store them '''
        data = self.data.get_row_list('RawImport', 'imported_country = false')
        if data is None:
            return

        for item in data:
            if item['CountryCode'] != '' and not self.data.if_rec_exists('Country', 'abbreviation', item['CountryCode']):
                rec = {'name': item['Country'],
                        'abbreviation': item['CountryCode']}
                self.data.insert_row('Country', rec)
            self.data.update_row_by_id('RawImport', {'imported_country':True}, item['ID'])

        self.data.commit()

    @debugger
    def import_customer_contacts(self):
        ''' Store contact information for customers '''
        data = self.data.get_row_list('RawImport', 'imported_customer = false and BalanceImpact = \'Credit\'')
        if data is None:
            mb.showinfo('INFO', 'There are no customer contacts to import.')
            return

        count = 0
        for item in data:
            if item['Type'] == 'Website Payment' or item['Type'] == 'General Payment':
                # Yes it's a customer
                if not self.data.if_rec_exists('Customer', 'name', item['Name']):
                    rec = { 'date_created': item['Date'],
                            'name': item['Name'],
                            'address1': item['AddressLine1'],
                            'address2': item['AddressLine2'],
                            'state': item['State'],
                            'city': item['City'],
                            'zip': item['PostalCode'],
                            'email_address': item['FromEmail'],
                            'email_status_ID': self.data.get_id_by_row('EmailStatus', 'name', 'primary'),
                            'phone_number': item['Phone'],
                            'phone_status_ID': self.data.get_id_by_row('PhoneStatus', 'name', 'primary'),
                            'description': 'Imported from PayPal',
                            'notes': item['Subject'],
                            'country_ID': self.data.get_id_by_row('Country', 'abbreviation', item['CountryCode']),
                            'class_ID': self.data.get_id_by_row('ContactClass', 'name', 'retail')}

                    self.data.insert_row('Customer', rec)
                    count+=1
                # BUG: (fixed) When there are multiple instances of a name, the sale or purch record does not get imported
                # because the imported_customer field does not get updated due to the duplicate name interlock.
                self.data.update_row_by_id('RawImport', {'imported_customer':True}, item['ID'])
        self.data.commit()
        mb.showinfo('INFO', 'Imported %d customer contacts.'%(count))

    @debugger
    def import_vendor_contacts(self):
        ''' Store contact information for vendors '''
        data = self.data.get_row_list('RawImport', 'imported_vendor = false and BalanceImpact = \'Debit\'')
        if data is None:
            mb.showinfo('INFO', 'There are no customer contacts to import.')
            return

        count = 0
        for item in data:
            if item['Name'] != '' and item['Name'] != 'PayPal':
                if not self.data.if_rec_exists('Vendor', 'name', item['Name']):
                    rec = { 'date_created': item['Date'],
                            'name': item['Name'],
                            'contact_name':'',
                            'email_address': self.validate_email(item['ToEmail']),
                            'email_status_ID': self.data.get_id_by_row('EmailStatus', 'name', 'primary'),
                            'phone_number': '',
                            'phone_status_ID': self.data.get_id_by_row('PhoneStatus', 'name', 'primary'),
                            'description': item['ItemTitle'],
                            'notes': item['Subject'],
                            'type_ID': self.data.get_id_by_row('VendorType', 'name', 'unknown'),}

                    self.data.insert_row('Vendor', rec)
                    self.data.update_row_by_id('RawImport', {'imported_vendor':True}, item['ID'])
                    count+=1

        self.data.commit()
        mb.showinfo('INFO', 'Imported %d vendor contacts.'%(count))

    @debugger
    def do_purchase_transactions(self):
        ''' Handle all of the transaction details for purchases '''
        data = self.data.get_row_list('RawImport', 'imported_purchase = false and imported_vendor = true and BalanceImpact = \'Debit\'')
        if data is None:
            mb.showinfo('INFO', 'There are no purchase transcations to import.')
            return

        count = 0
        for item in data:
            if item['Name'] != '' and item['Name'] != 'PayPal':
                gross = item['Gross']
                tax = item['SalesTax']
                shipping = item['Shipping']
                rec = { 'date': item['Date'],
                        'raw_import_ID': int(item['ID']),
                        'vendor_ID': self.data.get_id_by_row('Vendor', 'name', item['Name']),
                        'status_ID': self.data.get_id_by_row('PurchaseStatus', 'name', 'complete'),
                        'type_ID': self.data.get_id_by_row('PurchaseType', 'name', 'unknown'),
                        'transaction_uuid': item['TransactionID'],
                        'gross': self.data.convert_value(item['Gross'], float),
                        'tax': self.data.convert_value(item['SalesTax'], float),
                        'shipping': self.data.convert_value(item['Shipping'], float),
                        'notes': item['Subject'] + '\n' +item['ItemTitle'],
                        'committed': False}

                self.data.insert_row('PurchaseRecord', rec)
                self.data.update_row_by_id('RawImport', {'imported_purchase':True}, item['ID'])
                count+=1

        self.data.commit()
        mb.showinfo('INFO', 'Imported %d purchase transactions.'%(count))

    @debugger
    def do_sales_transactions(self):
        ''' Do all sales transactions '''
        data = self.data.get_row_list('RawImport', 'imported_sale = false and imported_customer = true and BalanceImpact = \'Credit\'')
        if data is None:
            mb.showinfo('INFO', 'There are no sales transcations to import.')
            return

        count = 0
        for item in data:
            if item['Name'] != '' and item['Name'] != 'PayPal':
                rec = { 'date': item['Date'],
                        'customer_ID': self.data.get_id_by_row('Customer', 'name', item['Name']),
                        'raw_import_ID': int(item['ID']),
                        'status_ID': self.data.get_id_by_row('SaleStatus', 'name', 'complete'),
                        'transaction_uuid': item['TransactionID'],
                        'gross': self.data.convert_value(item['Gross'], float),
                        'fees': self.data.convert_value(item['Fee'], float),
                        'shipping': self.data.convert_value(item['Shipping'], float),
                        'notes': item['Subject'] + '\n' +item['ItemTitle'],
                        'committed': False}

                self.data.insert_row('SaleRecord', rec)
                count+=1
                self.data.update_row_by_id('RawImport', {'imported_sale':True}, item['ID'])

        self.data.commit()
        mb.showinfo('INFO', 'Imported %d sale transactions.'%(count))

