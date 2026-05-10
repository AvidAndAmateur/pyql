import sqlite3
import sys
import os
import time
def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
try:
    def setup():
        global db
        global SQLDB
        global cursor
        db = input("enter name or path of database: ")
        SQLDB = sqlite3.connect(f'{db}')
        cursor = SQLDB.cursor()
        main()
    def main():
        clear()
        print(f'connected to {db}')
        userinp = input("enter operation: ")
        if userinp == "lsT":
             query = "SELECT name FROM sqlite_master WHERE type='table';"
             cursor.execute(query)
             print(cursor.fetchall())
             time.sleep(5)
             main()
        if userinp == "updV":
             tblname = input("enter table name: ")
             upcolname = input("column name: ")
             valname = input("new value: ")
             oldvalname = input("old value: ")
             query = f"UPDATE {tblname} SET {upcolname} = '{valname}' WHERE {upcolname} ='{oldvalname}'"
             cursor.execute(query)
             SQLDB.commit()
             main()
        if userinp == "insV":
             tablname = input("enter table name: ")
             incolname = input("enter column name: ")
             addval = input("value to add: ")
             query = f"INSERT INTO {tablname} ({incolname}) VALUES ('{addval}')"
             cursor.execute(query)
             SQLDB.commit()
             main()
    args = sys.argv[1:]
    if  len(args)>0 and args[0].lower() == "-h":
        print("options: \n list tables (lsT), update values(updV) \n insert values (insV), delete values (delV) \n list all value \n find value")
        print("create table (crtT), delete table (delT) \n run sql query (SQLCMD)")
    else:
        setup()
except KeyboardInterrupt:
    clear()