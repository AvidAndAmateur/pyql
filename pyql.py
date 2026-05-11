import sqlite3
import sys
import os
import time
from pathlib import Path
def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
try:
    def setup():
        clear()
        global db
        global SQLDB
        global cursor
        db = Path(input("enter name or path of database: "))
        if db.exists():
            SQLDB = sqlite3.connect(f'{db}')
            cursor = SQLDB.cursor()
            main()
        else:
            print("database does not exist, returning to setup")
            time.sleep(3)
            setup()
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
             clear()
             tblname = input("enter table name: ")
             upcolname = input("column name: ")
             valname = input("new value: ")
             oldvalname = input("old value: ")
             query = f"UPDATE {tblname} SET {upcolname} = '{valname}' WHERE {upcolname} ='{oldvalname}'"
             cursor.execute(query)
             SQLDB.commit()
             main()
        if userinp == "insV":
             clear()
             tablname = input("enter table name: ")
             incolname = input("enter column name: ")
             addval = input("value to add: ")
             query = f"INSERT INTO {tablname} ({incolname}) VALUES ('{addval}')"
             cursor.execute(query)
             SQLDB.commit()
             main()
        if userinp == "del":
             clear()
             tablname = input("enter table name: ")
             valname = input("enter value name: ")
             operator = input("operator: ")
             valwhere = input(f"where value {operator}:  ")
             query = f"DELETE FROM {tablname} WHERE {valname} {operator} '{valwhere}'"
             cursor.execute(query)
             SQLDB.commit()
             main()
        if userinp == "crtT":
             tablname = input("enter table name: ")
             column = input("column name: ")
             query = f"CREATE TABLE {tablname} ({column} TEXT)"
             cursor.execute(query)
             SQLDB.commit()
             main()
        if userinp == "delT":
             clear()
             tablname = input("enter table name: ")
             print("THIS CHANGE IS PERMANENT")
             areyousure = input("please type yes if you're sure: ") 
             if areyousure.lower() == "yes":
                 query = f"DROP TABLE {tablname}"
                 cursor.execute(query)
                 SQLDB.commit()
                 main()
             else:
              print("cancelling operation")
              time.sleep(3)
              main()
        if userinp.upper() == "SQLCMD":
            clear()
            cmd = input("Enter sql cmd: ")
            fetching = input("fetching vals: ")
            if fetching.lower() == "yes":
                cursor.execute(cmd)
                print(cursor.fetchall())
                time.sleep(5)
                main()
            elif "DROP" or "DELETE" in cmd:
                print("are you sure you want to execute this? \n it contains permanent value modifications")
                sure = input("yes/no: ")
                if sure.lower() == "yes":
                    cursor.execute(cmd)
                    SQLDB.commit()
                    main()
                else:
                    print("operation cancelled, returning to main menu")
                    time.sleep(3)
                    main()
            else:
                cursor.execute(cmd)
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