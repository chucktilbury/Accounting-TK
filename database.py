import os
import time

import sqlite3 as sql
from tkinter import messagebox as mbox
from utility import Logger, debugger
#import utility


class Database(object):
    '''
    The goal of this class is to move all SQL composition out of the program
    logic and place it here.
    '''

    __instance = None

    @staticmethod
    def get_instance():
        '''
        This static method is used to get the singleton object for this class.
        '''
        if Database.__instance == None:
            Database()
        return Database.__instance

    def __init__(self):

        # gate the access to __init__()
        if Database.__instance != None:
            raise Exception("Database class is a singleton. Use get_instance() instead.")
        else:
            Database.__instance = self

        # Continue with init exactly once.
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug("enter constructor")
        self.data_version = '1.0'
        self.database_name = 'accounting.db'
        self.db_create_file = 'database.sql'
        self.db_pop_file = 'populate.sql'
        self.open()
        self.logger.debug("leave constructor")

    @debugger
    def open(self):

        if not os.path.isfile(self.database_name):
            self.create_database()

        self.db = sql.connect(self.database_name)
        self.db.row_factory = sql.Row

    @debugger
    def close(self):
        self.db.commit()
        self.db.close()

    @debugger
    def read_statement(self, fh):

        retv = ''
        for line in fh:
            # strip comments from the line
            idx = line.find('#')
            line = line[0:idx].strip()
            # If there is anything left, append it to the return value.
            if len(line) > 0:
                retv += " %s"%(line)
                if line[-1] == ';':
                    break

        return retv

    @debugger
    def run_file(self, db, name):

        with open(name) as fh:
            while True:
                line = self.read_statement(fh)
                if len(line) > 0:
                    db.execute(line)
                else:
                    break

    @debugger
    def create_database(self):
        # Load the DB creation file and create the database from that.
        self.logger.info("creating database")

        c = sql.connect(self.database_name)
        db = c.cursor()
        self.run_file(db, self.db_create_file)
        self.run_file(db, self.db_pop_file)
        c.commit()
        c.close()

    @debugger
    def get_columns(self, table):
        '''
        Return a dict where all column names are keys with blank data.
        '''
        retv = {}
        cols = self.execute('PRAGMA table_info(%s);' % (table))
        for item in cols:
            retv[item[1]] = ''
        return cols

    @debugger
    def get_column_list(self, table):
        '''
        Return a dict where all column names are keys with blank data.
        '''
        retv = []
        cols = self.execute('PRAGMA table_info(%s);' % (table))
        for item in cols:
            retv.append(item[1])
        return retv

    @debugger
    def execute(self, sql):
        self.logger.debug("SQL=%s" % (sql))
        return self.db.execute(sql)

    @debugger
    def commit(self):
        self.db.commit()

    @debugger
    def populate_list(self, table, name):
        curs = self.execute('select %s from %s;'%(name, table))
        retv = []
        for item in curs:
            retv.append(' '.join(item))
            #retv.append(item)
        return retv

    @debugger
    def get_row_by_id(self, table, ID):
        curs = self.execute('select * from %s where ID = %d;'%(table, ID)).fetchall()
        return dict(curs[0])

    @debugger
    def get_id_by_row(self, table, col, val):
        if type(val) is str:
            sql = 'SELECT ID FROM %s WHERE %s = \"%s\";'%(table, col, val)
        else:
            sql = 'SELECT ID FROM %s WHERE %s = %s;'%(table, col, val)
        row = self.execute(sql).fetchall()

        if len(row) == 0:
            return None
        else:
            return dict(row[0])['ID']

    @debugger
    def get_cursor(self):
        return self.db.cursor()

    @debugger
    def get_id_list(self, table):
        ''' Get a list of all of the IDs in the table '''
        retv = []
        sql = 'SELECT ID FROM %s;'%(table)
        cur = self.execute(sql)
        for item in cur:
            retv.append(item[0])

        return retv

    @debugger
    def get_row_list(self, table, where):
        ''' Get a generic list of rows based on more than one criteria '''
        retv = []
        sql = 'SELECT * FROM %s WHERE %s'%(table, where)
        cur = self.execute(sql)
        for item in cur:
            retv.append(dict(item))

        if len(retv) == 0:
            return None
        else:
            return retv

    @debugger
    def get_row_list_by_col(self, table, col, val):
        ''' Get the list of all rows where the column has a certain value '''
        retv = []
        if type(val) is str:
            sql = 'SELECT * FROM %s WHERE %s = \"%s\";'%(table, col, val)
        else:
            sql = 'SELECT * FROM %s WHERE %s = %s;'%(table, col, val)

        cur = self.execute(sql)
        for item in cur:
            retv.append(dict(item))

        if len(retv) == 0:
            return None
        else:
            return retv

    @debugger
    def get_id_by_name(self, table, name):
        sql = 'select ID from %s where name = \"%s\";'%(table, name)
        curs = self.execute(sql)
        recs = curs.fetchall()

        retv = None
        for row in recs:
            retv =  row[0]
            break

        return retv

    @debugger
    def insert_row(self, table, rec):
        ''' Insert a row from a dictionary '''

        keys = ','.join(rec.keys())
        qmks = ','.join(list('?'*len(rec)))
        vals = tuple(rec.values())

        sql = 'INSERT INTO %s (%s) VALUES (%s);'%(table, keys, qmks)
        self.logger.debug("SQL=%s (%s)" % (sql, vals))
        return self.db.execute(sql, vals)

    @debugger
    def update_row(self, table, rec, where):
        ''' Update a row from a dictionary '''

        keys = '=?,'.join(rec.keys())
        keys += '=?'
        vals = tuple(rec.values())

        sql = 'UPDATE %s SET %s WHERE %s;'%(table, keys, where)
        self.logger.debug("SQL=%s (%s)" % (sql, vals))
        return self.db.execute(sql, vals)

    @debugger
    def update_row_by_id(self, table, rec, id):
        ''' Update a row using a dictionary and the id of the row '''

        keys = '=?,'.join(rec.keys())
        keys += '=?'
        vals = tuple(rec.values())

        sql = 'UPDATE %s SET %s WHERE ID = %d;'%(table, keys, id)
        self.logger.debug("SQL=%s (%s)" % (sql, vals))
        return self.db.execute(sql, vals)

    @debugger
    def delete_row(self, table, id):
        ''' Delete the row given by the ID '''
        sql = 'DELETE FROM %s WHERE ID = %d;' % (table, id)
        self.logger.debug("SQL=%s" % (sql))
        return self.db.execute(sql)

    @debugger
    def if_rec_exists(self, table, column, value):
        ''' Return True if there is a row that has the column with the value '''

        if type(value) is int or type(value) is float:
            sql = 'SELECT %s FROM %s WHERE %s = %s;'%(column, table, column, str(value))
        else:
            sql = 'SELECT %s FROM %s WHERE %s = \"%s\";'%(column, table, column, value)
        cursor = self.db.execute(sql)
        if cursor.fetchone() is None:
            return False

        return True

