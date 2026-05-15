import sqlite3
import sys
import os
import time
from pathlib import Path
import datetime
unlockcmd = False
uselogfile = False
def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
def helpmenu():
    print("options: \n list tables (lsT), update values(updV) \n insert values (insV), delete values (delV) \n list all value \n find value")
    print("create table (crtT), delete table (delT) \n run sql query (SQLCMD)")
    time.sleep(5)
    main()
def writetimetolog():
    global now
    now = datetime.datetime.now()
    logfile.write(f"{now.minute}:{now.second}\n")
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
            if uselogfile == True:
                logfile.write(f'connected to {db}'+"\n")
                writetimetolog()
                logfile.flush()
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
             if uselogfile == True:
                 logfile.write(query+"\n")
                 writetimetolog()
                 logfile.flush()
             time.sleep(5)
             main()
        if userinp == "updV":
             clear()
             tblname = input("enter table name: ")
             try:
                amounttoupd = int(input("enter how many values you want to update: "))
             except ValueError:
                 print("please type an integer")
                 time.sleep(2)
                 main()
             for i in range(0,amounttoupd):
                upcolname = input("column name: ")
                valname = input("new value: ")
                oldvalname = input("old value: ")
                query = f"UPDATE {tblname} SET {upcolname} = '{valname}' WHERE {upcolname} ='{oldvalname}'"
                cursor.execute(query)
                SQLDB.commit()
                print(f"updated {tblname} with the new value {valname} in the column {upcolname}, replacing {oldvalname}")
                if uselogfile == True:
                    logfile.write(query+"\n")
                    writetimetolog()
                    logfile.flush()
                time.sleep(1)
             time.sleep(3)
             main()
        if userinp == "insV":
             clear()
             tablname = input("enter table name: ")
             try:
                howmanycols = int(input("how many columns: "))
                howmanyvals = int(input("how many values: "))
             except ValueError:
                 print("please type an integer")
                 time.sleep(2)
                 main()
             for i in range(0,howmanycols):
                for i in range(0,howmanyvals):
                    incolname = input("enter column name: ")
                    addval = input("value to add: ")
                    query = f"INSERT INTO {tablname} ({incolname}) VALUES ('{addval}')"
                    cursor.execute(query)
                    SQLDB.commit()
                    print(f"inserted value {addval} into {incolname} in {tablname}")
                    if uselogfile == True:
                        logfile.write(query+"\n")
                        writetimetolog()
                        logfile.flush()
                    time.sleep(3)
             main()
        if userinp == "delV":
             clear()
             print("deleted values are gone PERMANENTLY")
             areyousure = input("are you sure?: ")
             if areyousure.lower() == "yes":
                tablname = input("enter table name: ")
                try:
                    howmanydelvals = int(input("how many values to be deleted: "))
                except ValueError:
                    print("enter a integer")
                    time.sleep(2)
                    main()
                for i in range(0,howmanydelvals):
                    valname = input("enter value name: ")
                    operator = input("operator: ")
                    valwhere = input(f"where value {operator}:  ")
                    query = f"DELETE FROM {tablname} WHERE {valname} {operator} '{valwhere}'"
                    cursor.execute(query)
                    SQLDB.commit()
                    print(f"deleted {valname} from {tablname} where {valname} {operator} {valwhere}")
                    if uselogfile == True:
                        logfile.write(query+"\n")
                        writetimetolog()
                        logfile.flush()
                    time.sleep(3)
                main()
             else:
                 print("returning to main")
                 time.sleep(2)
                 main()
        if userinp == "crtT":
             try:
                 howmanytbls = int(input("how many tables: "))
             except ValueError:
                 print("enter an integer")
                 time.sleep(2)
                 main()
             for i in range(0,howmanytbls):
                tablname = input("enter table name: ")
                column = input("column name: ")
                query = f"CREATE TABLE {tablname} ({column} TEXT)"
                cursor.execute(query)
                SQLDB.commit()
                print(f"created {tablname} with the column {column}")
                if uselogfile == True:
                    logfile.write(query+"\n")
                    writetimetolog()
                    logfile.flush()
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
                 if uselogfile == True:
                     logfile.write(query+"\n")
                     writetimetolog()
                     logfile.flush()
                 time.sleep(3)
                 main()
             else:
              print("cancelling operation")
              time.sleep(3)
              main()
        if userinp.upper() == "SQLCMD" and unlockcmd == True:
            clear()
            try:
                amountofcmds = int(input("enter how many commands you wish to execute: "))
                for i in range(0,amountofcmds):
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
            except ValueError:
                print("please enter an integer")
                time.sleep(2)
                main()
        elif userinp.upper() == "SQLCMD" and unlockcmd == False:
            print("advance mode is locked, please launch the script again using the -u argument")
        if userinp.lower() == "quit" or userinp.lower() == "exit":
            SQLDB.close()
            logfile.close()
            quit()
    args = sys.argv[1:]
    if  len(args)>0 and args[0].lower() == "-h":
        helpmenu()
    elif len(args)>0 and args[0].lower() == "-u":
        print("unlocked advance mode")
        unlockcmd = True
        logfile = open(f'log-{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}.txt','a')
        uselogfile = True
        time.sleep(3)
        setup()
    else:
        setup()
except KeyboardInterrupt:
    SQLDB.close()
    logfile.close()
    clear()