import csv
import sys, re
import tkinter
from tkinter.filedialog import askopenfile
from database import Database
from utility import Logger, debugger



class Importer(object):

    def __init__(self):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)

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
    def read_file(self):
        ''' Handle the file IO for the CSV file '''
        master = tkinter.Tk()
        fh = askopenfile(mode='r', filetypes=[('Spread Sheets', '*.csv *.CSV'), ('All Files', '*')])
        if fh is None:
            return None

        raw = []
        reader = csv.reader(fh)

        for line in reader:
            raw.append(line)
        fh.close()
        master.destroy()
        #print(raw)
        return raw

    @debugger
    def read_all(self):
        ''' Read all of the lines in the CSV into the database '''
        raw = self.read_file()

        data = []
        for line in raw:
            tmp = {}
            for idx, item in enumerate(line):
                tmp[self.legend[idx]] = item
            data.append(tmp)

            if tmp['Status'] == 'Completed':
                tmp['Completed'] = 0
                if not self.data.if_rec_exists('RawImport', 'TransactionID', tmp['TransactionID']):
                    self.data.insert_row('RawImport', tmp)

        self.data.commit()
        return data

    @debugger
    def get_sales(self):
        ''' Isolate "credit" transactions and return them as a list of dicts'''
        return self.data.get_row_list_by_col('RawImport', 'BalanceImpact', 'Credit')

    @debugger
    def import_country_codes(self, data):
        ''' Find the new country codes and store them '''
        for item in data:
            if item['CountryCode'] != '' and not self.data.if_rec_exists('Country', 'abbreviation', item['CountryCode']):
                rec = {'name': item['Country'],
                        'abbreviation': item['CountryCode']}
                self.data.insert_row('Country', rec)

        self.data.commit()

    @debugger
    def import_customer_contacts(self, data):
        ''' Store contact information for customers '''
        for item in data:
            if item['Type'] == 'Website Payment' or item['Type'] == 'General Payment':
                # Yes it's a customer
                if not self.data.if_rec_exists('Contacts', 'name', item['Name']):
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
                            'type_ID': self.data.get_id_by_row('ContactType', 'name', 'customer'),
                            'status_ID': self.data.get_id_by_row('ContactStatus', 'name', 'active'),
                            'class_ID': self.data.get_id_by_row('ContactClass', 'name', 'retail'),
                            'locked_ID': self.data.get_id_by_row('LockedState', 'name', 'no')}

                    self.data.insert_row('Contacts', rec)
        self.data.commit()

    @debugger
    def do_sales_transactions(self, data):
        ''' Do all sales transactions '''

    @debugger
    def get_purchases(self):
        ''' Isolate "debit" transactions and return them as a list of dicts '''
        return self.data.get_row_list_by_col('RawImport', 'BalanceImpact', 'Debit')

    @debugger
    def validate_email(self, email):
        if bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email)):
            return email
        else:
            return ''

    @debugger
    def import_vendor_contacts(self, data):
        ''' Store contact information for vendors '''
        for item in data:
            if item['Name'] != '' and item['Name'] != 'PayPal':
                if not self.data.if_rec_exists('Contacts', 'name', item['Name']):
                    rec = { 'date_created': item['Date'],
                            'name': item['Name'],
                            'address1': '',
                            'address2': '',
                            'state': '',
                            'city': '',
                            'zip': '',
                            'email_address': self.validate_email(item['ToEmail']),
                            'email_status_ID': self.data.get_id_by_row('EmailStatus', 'name', 'primary'),
                            'phone_number': '',
                            'phone_status_ID': self.data.get_id_by_row('PhoneStatus', 'name', 'primary'),
                            'description': item['ItemTitle'],
                            'notes': item['Subject'],
                            'country_ID': 1, #self.data.get_id_by_row('Country', 'abbreviation', item['CountryCode']),
                            'type_ID': self.data.get_id_by_row('ContactType', 'name', 'vendor'),
                            'status_ID': self.data.get_id_by_row('ContactStatus', 'name', 'active'),
                            'class_ID': self.data.get_id_by_row('ContactClass', 'name', 'retail'),
                            'locked_ID':self.data.get_id_by_row('LockedState', 'name', 'no')}
                    self.data.insert_row('Contacts', rec)
        self.data.commit()

    @debugger
    def do_purchase_transactions(self, data):
        ''' Handle all of the transaction details for purchases '''



    # @debugger
    # def import_customers(self):
    #     data = self.read_all()
    #     #self.do_contacts_table(data)

    # @debugger
    # def import_country_codes(self):
    #     data = self.read_all()
    #     self.do_country_codes(data)

    # @debugger
    # def get_id_by_trans_id(self, id):
    #     sql = 'select ID from RawImport where TransactionID = \'%s\';'%(id)
    #     curs = self.data.execute(sql)
    #     recs = curs.fetchall()

    #     retv = None
    #     for row in recs:
    #         retv =  row[0]
    #         break

    #     return retv

    # @debugger
    # def read_customers(self, data):

    #     customers = []
    #     for item in data:
    #         if item['Type'] == 'Website Payment' and item['BalanceImpact'] == 'Credit':
    #             customers.append(item)

    #     return customers

    # @debugger
    # def if_customer_exists(self, name):
    #     '''
    #     Check if the customer exists in the database. If it does then return True,
    #     else return False.
    #     '''
    #     sql = 'select name from Contacts where name = \'%s\';'%(name)
    #     cursor = self.data.execute(sql)
    #     if cursor.fetchone() is None:
    #         return False

    #     return True

    # @debugger
    # def if_country_exists(self, code):
    #     '''
    #     Check if the country code exists in the database. If it does then return True,
    #     else return False.
    #     '''
    #     sql = 'select ID from Country where abbreviation = \'%s\';'%(code)
    #     cursor = self.data.execute(sql)
    #     if cursor.fetchone() is None:
    #         return False

    #     return True

    # @debugger
    # def get_country_id_from_abbr(self, abbr):
    #     sql = 'select ID from Country where abbreviation = \'%s\';'%(abbr)
    #     cursor = self.data.execute(sql)
    #     for row in cursor:
    #         return row[0]

    # @debugger
    # def do_contacts_table(self, data):

    #     self.do_country_codes(data)
    #     customers = self.read_customers(data)

    #     if customers is None:
    #         return

    #     for line in customers:
    #         if not self.if_customer_exists(line['Name']):
    #             sql = '''INSERT INTO Contacts (
    #             date_created,
    #             name,
    #             address1,
    #             address2,
    #             state,
    #             city,
    #             zip,
    #             email_address,
    #             email_status_ID,
    #             phone_number,
    #             phone_status_ID,
    #             description,
    #             country_ID,
    #             type_ID,
    #             status_ID,
    #             class_ID,
    #             locked)
    #             VALUES (
    #             \'{Date}\',
    #             \'{Name}\',
    #             \'{AddressLine1}\',
    #             \'{AddressLine2}\',
    #             \'{State}\',
    #             \'{City}\',
    #             \'{PostalCode}\',
    #             \'{FromEmail}\',
    #             1,
    #             \'{Phone}\',
    #             1,
    #             \'imported from PayPal\',
    #             1,
    #             1,
    #             1,
    #             2,
    #             False);'''.format(**line)
    #             self.data.execute(sql)

    #             sql = 'UPDATE Contacts SET country_ID = ? WHERE name = ?;'
    #             cursor = self.data.db.cursor()
    #             dt = [self.get_country_id_from_abbr(line['Country Code']), line['Name']]
    #             cursor.execute(sql, dt)
    #             self.data.commit()

    # @debugger
    # def do_country_codes(self, data):
    #     #data = self.read_all()
    #     for item in data:
    #         if item['Country Code'] != '':
    #             code = item['Country Code']
    #             country = item['Country']
    #             if not self.if_country_exists(code):
    #                 sql = 'INSERT INTO Country (name, abbreviation) VALUES (\'%s\', \'%s\');'%(country, code)
    #                 self.data.execute(sql)
    #                 self.data.commit()



# if __name__ == '__main__':
#     imp = Importer()
#     data = imp.read_all()
#     imp.do_contacts_table(data)

