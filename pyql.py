import sqlite3
import sys
import os
import time
from pathlib import Path
unlockcmd = False
def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
def helpmenu():
    print("options: \n list tables (lsT), update values(updV) \n insert values (insV), delete values (delV) \n list all value \n find value")
    print("create table (crtT), delete table (delT) \n run sql query (SQLCMD)")
    time.sleep(5)
    main()
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
        if userinp == "help":
            helpmenu()
        if userinp == "lsT":
             query = "SELECT name FROM sqlite_master WHERE type='table';"
             cursor.execute(query)
             print(f"Tables in {db}")
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
             print(f"updated {tablname} with the new value {valname} in the column {upcolname}, replacing {oldvalname}")
             time.sleep(3)
             main()
        if userinp == "insV":
             clear()
             tablname = input("enter table name: ")
             incolname = input("enter column name: ")
             addval = input("value to add: ")
             query = f"INSERT INTO {tablname} ({incolname}) VALUES ('{addval}')"
             cursor.execute(query)
             SQLDB.commit()
             print(f"inserted value {addval} into {incolname} in {tablname}")
             time.sleep(3)
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
             print(f"deleted {valname} from {tablname} where {valname} {operator} {valwhere}")
             time.sleep(3)
             main()
        if userinp == "crtT":
             tablname = input("enter table name: ")
             column = input("column name: ")
             query = f"CREATE TABLE {tablname} ({column} TEXT)"
             cursor.execute(query)
             SQLDB.commit()
             print(f"created {tablname} with the column {column}")
             time.sleep(3)
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
                 print(f"deleted {tablname}")
                 time.sleep(3)
                 main()
             else:
              print("cancelling operation")
              time.sleep(3)
              main()
        if userinp.upper() == "SQLCMD" and unlockcmd == True:
            clear()
            cmd = input("Enter sql cmd: ")
            fetching = input("fetching vals: ")
            if fetching.lower() == "yes":
                cursor.execute(cmd)
                print(cursor.fetchall())
                time.sleep(5)
                main()
            elif "DROP" in cmd or "DELETE" in cmd:
                print("are you sure you want to execute this? \n it contains permanent value modifications")
                sure = input("yes/no: ")
                if sure.lower() == "yes":
                    cursor.execute(cmd)
                    SQLDB.commit()
                    print(f"executed {cmd}")
                    main()
                else:
                    print("operation cancelled, returning to main menu")
                    time.sleep(3)
                    main()
            else:
                cursor.execute(cmd)
                SQLDB.commit()
                print(f"executed {cmd}")
                time.sleep(3)
                main()
        elif userinp.upper() == "SQLCMD" and unlockcmd == False:
            print("advance mode is locked, please launch the script again using the -u argument")
        if userinp.lower() == "quit" or userinp.lower() == "exit":
            quit()
    args = sys.argv[1:]
    if  len(args)>0 and args[0].lower() == "-h":
        helpmenu()
    elif len(args)>0 and args[0].lower() == "-u":
        print("unlocked advance mode")
        unlockcmd = True
        time.sleep(3)
        setup()
    else:
        setup()
except KeyboardInterrupt:
    clear()