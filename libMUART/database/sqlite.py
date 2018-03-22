#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import sqlite3 as lite

#Usage
#  air=G3(baudrate=9600)
#  pmdata = (air.read("/dev/ttyS0"))
#  print (pmdata[3], pmdata[4], pmdata[5])

class sqlitedb():
    def __init__(self, debug=False):
        if debug: print ("init")
        self.con = None
        self.debug = debug

    def connectDB(self, dbname):
        try:
            self.con = lite.connect(dbname)
            cur = self.con.cursor()
            cur.execute('SELECT SQLITE_VERSION()')
            data = cur.fetchone()
            if self.debug: print ("SQLite version: %s" % data )

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def createTable(self, tableName, columns="(Id INT, Name TEXT)"):
        try:
            cur = self.con.cursor()    
            cur.execute("CREATE TABLE {} {}".format(tableName, columns))

        except:
            print("Unexpected error:", sys.exc_info()[0])
            pass

    def insertData(self, tableName, columns, data):
        cur = self.con.cursor()
        cur.execute("INSERT INTO {} ({}) VALUES({})".format(tableName, columns, data))

    def sqlSelect(self, sqlString="SELECT * FROM Users"):
        cur = self.con.cursor()  
        cur.execute(sqlString)
        self.rows = cur.fetchall()

