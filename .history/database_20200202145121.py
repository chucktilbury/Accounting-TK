import os
import time

import sqlite3 as sql
from tkinter import messagebox as mbox
from utility import Logger, debugger, register_event
#import utility


class Database(object):

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
        self.db_create_file = 'accounts.sqlite3'
        self.db_pop_file = 'populate.sqlite3'
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
            retv[item] = ''
        return cols

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





    # @debugger
    # def _insert(self, table, fields, values):
    #     '''
    #     Do a SQL "insert" command. Create a row in the database.
    #     table = the table name as a string
    #     fields = [field names as strings]
    #     values = [values for the fields]
    #     The values can be any arbitrary type that can be converted to a string.
    #     '''
    #     sv = []
    #     for v in values:
    #         if type(v) == str:
    #             sv.append("\'%s\'" % (v))
    #         else:
    #             sv.append(str(v))

    #     sql = 'insert into %s (%s) values (%s);' % (
    #         table, ','.join(fields), ','.join(sv))
    #     self.execute(sql)
    #     self.commit()

    # @debugger
    # def _select(self, table, fields=None, where=None):
    #     '''
    #     Do a SQL "select" command. Returns one or more rows as a database cursor.
    #     table = the table name as a string
    #     fields = [field names as strings]
    #     where = an optional expression presented as a string
    #     '''
    #     if fields is None:
    #         if not where is None:
    #             sql = "select * from %s where %s;" % (table, where)
    #         else:
    #             sql = "select * from %s;" % (table)
    #     elif type(fields) is str:
    #         if not where is None:
    #             sql = "select %s from %s where %s;" % (fields, table, where)
    #         else:
    #             sql = "select %s from %s;" % (fields, table)
    #     else:
    #         if not where is None:
    #             sql = "select %s from %s where %s;" % (
    #                 ','.join(fields), table, where)
    #         else:
    #             sql = "select %s from %s;" % (','.join(fields), table)

    #     return self.execute(sql)

    # @debugger
    # def _update(self, table, field, value, where):
    #     '''
    #     Do a SQL "update" command. Modifies a row.
    #     table = the table name as a string
    #     field = a single field name as a string, or a list of field names
    #     value = the value to put in the field, or a list of values. may be any type
    #     where = a required expression presented as a string

    #     If the fields and values are not the same size of array, it will throw
    #     an IndexError exception.
    #     '''
    #     if type(field) is list:
    #         # convert a list of field, value variables
    #         arr = []
    #         for idx, item in enumerate(field):
    #             if type(value[idx]) is str:
    #                 arr.append('%s = \'%s\'' % (item, str(value[idx])))
    #             else:
    #                 arr.append('%s = %s' % (item, str(value[idx])))
    #         val = ','.join(arr)
    #         sql = "update %s set %s where %s;" % (table, val, where)

    #     else:
    #         if type(value) is str:
    #             val = "\'%s\'" % (value)
    #         else:
    #             val = str(value)
    #         sql = "update %s set %s = %s where %s;" % (
    #             table, field, val, where)

    #     self.execute(sql)
    #     self.commit()

    # @debugger
    # def _delete(self, table, id):
    #     '''
    #     Do a SQL "delete" command. Delete a row from the database.
    #     table = the table name
    #     id = the row ID to delete
    #     '''
    #     sql = 'delete from %s where ID = %d;' % (table, id)
    #     self.execute(sql)
    #     self.commit()

    # @debugger
    # def get_columns(self, table):
    #     '''
    #     Return a list of all column names for the table specified.
    #     '''
    #     cols = self.execute('PRAGMA table_info(%s);' % (table))
    #     # for item in cols:
    #     #    print(item)
    #     return cols

    # @debugger
    # def convert_cursor(self, cursor, names):
    #     '''
    #     Returns a list of dicts where each row of data is in the dict with the
    #     name given in the order that it was read from the database.
    #     cursor = Sqlite3 database cursor
    #     names = list of names in the order they are expected
    #     '''
    #     ret_lst = []
    #     for row in cursor:
    #         val = {}
    #         for idx, item in enumerate(names):
    #             if not item is None:
    #                 val[item] = row[idx]
    #         ret_lst.append(val)

    #     return ret_lst

    # @debugger
    # def get_version(self):
    #     return self.data_version

    # # Utilities
    # @debugger
    # def validate_type(self, var, t):
    #     '''
    #     Validate the type of the argument. If it cannot be converted, then the program cannot continue.
    #     This is considered a developer error. The exceptions here only happen if the input validation
    #     from the GUI has failed.
    #     '''
    #     if type(var) != t:
    #         if t is float:
    #             try:
    #                 tmp = float(var)
    #                 return tmp
    #             except ValueError:
    #                 mbox.showerror("FATAL ERROR", "expected type %s but got type %s" % (
    #                     str(t), str(type(var))))
    #                 self.logger.fatal(
    #                     "expected type %s but got type %s" % (str(t), str(type(var))))
    #             except:
    #                 mbox.showerror("FATAL ERROR", "float type error.")
    #                 self.logger.fatal("float type error.")

    #         elif t is int:
    #             try:
    #                 tmp = int(var)
    #                 return tmp
    #             except ValueError:
    #                 mbox.showerror("FATAL ERROR", "expected type %s but got type %s" % (
    #                     str(t), str(type(var))))
    #                 self.logger.fatal(
    #                     "expected type %s but got type %s" % (str(t), str(type(var))))
    #             except:
    #                 mbox.showerror("FATAL ERROR", "int type error.")
    #                 self.logger.fatal("int type error.")

    #         elif t is bool:
    #             try:
    #                 tmp = bool(var)
    #                 return tmp
    #             except ValueError:
    #                 mbox.showerror("FATAL ERROR", "expected type %s but got type %s" % (
    #                     str(t), str(type(var))))
    #                 self.logger.fatal(
    #                     "expected type %s but got type %s" % (str(t), str(type(var))))
    #             except:
    #                 mbox.showerror("FATAL ERROR", "bool type error.")
    #                 self.logger.fatal("bool type error.")

    #         elif t is str:
    #             # anything can be converted to a str()
    #             return str(var)
    #         else:
    #             mbox.showerror("FATAL ERROR", "attempt to validate an unexpected type %s as type %s." % (
    #                 str(type(var)), str(t)))
    #             self.logger.fatal("attempt to validate an unexpected type %s as type %s." % (
    #                 str(type(var)), str(t)))
    #     else:
    #         return var

