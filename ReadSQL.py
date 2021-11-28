# SELECT database();
# TODO: command {command} was not recognized
# TODO: no data returned must not delete global data
# TODO: delete:data Command
# TODO: pause: make clever

import sys
import os
import argparse
import sqlite3
import traceback
from importlib.metadata import version

import time

#from okno import zobraz

'''
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')

'''

RED, YELLOW, GREEN, BLUE, COM, INVGREEN, END = '\033[91m', '\033[33m', '\033[4m', '\033[34m', '\033[4m', '\033[35m\033[42m', '\033[0m'
printRed = lambda sTxt: print(RED + sTxt + END)
printYellow = lambda sTxt: print(YELLOW + sTxt + END)
printBlue = lambda sTxt: print(BLUE + sTxt + END)
printCom = lambda sTxt: print(COM + sTxt + END)
printInvGreen = lambda sTxt: print(INVGREEN + sTxt + END)
Assert = lambda bCond=False, sTxt='': printRed(sTxt) if not bCond else None

conn = None
sqls = {}
data = None
columns = None
folder_exists = None
folder_name = None
db_version = "None: "
show_cases = 5
print_max_default = 100

command_options = {}
command_options["quit"] = {}
command_options["quit"]["name"] = []
command_options["quit"]["required"] = []
command_options["quit"]["type"] = []
command_options["quit"]["default"] = []
command_options["quit"]["help1"] = "Help for command 'folder'"
command_options["quit"]["help2"] = []
command_options["quit"]["alternative"] = ["q"]

command_options["folder"] = {}
command_options["folder"]["name"] = ["foldername"]
command_options["folder"]["required"] = [True]
command_options["folder"]["type"] = ["str"]
command_options["folder"]["default"] = [None]
command_options["folder"]["help1"] = "Help for command 'folder'"
command_options["folder"]["help2"] = ["Blabla1"]
command_options["folder"]["alternative"] = ["f"]

command_options["sqlite3"] = {}
command_options["sqlite3"]["name"] = ["filename"]
command_options["sqlite3"]["required"] = [True]
command_options["sqlite3"]["type"] = ["str"]
command_options["sqlite3"]["default"] = [None]
command_options["sqlite3"]["help1"] = "Help for command 'folder'"
command_options["sqlite3"]["help2"] = ["Blabla1"]
command_options["sqlite3"]["alternative"] = ["f"]

command_options["read"] = {}
command_options["read"]["name"] = ["filename"]
command_options["read"]["required"] = [True]
command_options["read"]["type"] = ["str"]
command_options["read"]["default"] = [None]
command_options["read"]["help1"] = "Help for command 'folder'"
command_options["read"]["help2"] = ["Blabla1"]
command_options["read"]["alternative"] = ["f"]

command_options["import"] = {}
command_options["import"]["name"] = ["filename"]
command_options["import"]["required"] = [True]
command_options["import"]["type"] = ["str"]
command_options["import"]["default"] = [None]
command_options["import"]["help1"] = "Help for command 'folder'"
command_options["import"]["help2"] = ["Blabla1"]
command_options["import"]["alternative"] = ["f"]

command_options["mysql"] = {}
command_options["mysql"]["name"] = ["schema"]
command_options["mysql"]["required"] = [True]
command_options["mysql"]["type"] = ["str"]
command_options["mysql"]["default"] = [None]
command_options["mysql"]["help1"] = "Help for command 'folder'"
command_options["mysql"]["help2"] = ["Blabla1"]
command_options["mysql"]["alternative"] = ["f"]

command_options["insert"] = {}
command_options["insert"]["name"] = ["tablename"]
command_options["insert"]["required"] = [True]
command_options["insert"]["type"] = ["str"]
command_options["insert"]["default"] = [None]
command_options["insert"]["help1"] = "Help for command 'folder'"
command_options["insert"]["help2"] = ["Blabla1"]
command_options["insert"]["alternative"] = ["f"]

command_options["print"] = {}
command_options["print"]["name"] = ["what", "from", "to", "step", "list", "columns"]
command_options["print"]["required"] = [False, False, False, False, False, False]
command_options["print"]["type"] = [["data","columns"], "int", "int", "int", "intlist", "strlist"]
command_options["print"]["default"] = ["data", 0, print_max_default, 1, None, None]
command_options["print"]["help1"] = "Help for command 'folder'"
command_options["print"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6"]
command_options["print"]["alternative"] = ["f"]

def parseArgv(argument_list):

    parser = argparse.ArgumentParser()

    parser.add_argument("sql_files", metavar="(SQL_filenames)", type=str, nargs="*",
                    help="Optional list of *.sql filenames (strings) separated by space")
    parser.set_defaults(sql_files="")

    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument("--interactive", dest="interactive", action="store_true")
    feature_parser.add_argument("--no-interactive", dest="interactive", action="store_false")
    parser.set_defaults(interactive="")

    return parser.parse_args(argument_list)

def parseSql(sql_filename, sql):
    global sqls
    sqls[sql_filename] = []
    if sql.count(";") > 0:
        for s in sql.split(";"):
            if s.strip() != "": sqls[sql_filename].append(s.strip())
    else:
        sqls[sql_filename].append(sql.strip())
    return None

def parseCommand(command_line):
    command = ""
    options = {}
    error = 0
    #command_line = command_line.replace(" ", "")
    command_line = command_line[1:].lower().strip() #no slash
    print (command_line)
    for c in command_options:
        #print(c)
        if command_line[:len(c)] == c:
            command = c
            command_line_list = command_line[len(c):].split(",")
            for i, cl in enumerate(command_line_list):
                cl = cl.strip()
                if "=" in cl:
                    cll = cl.split("=")
                    for o in command_options[c]["name"]:
                        if cll[0].strip() == o:
                            options[o] = cll[1].strip()
                    if cll[0].strip() not in options:
                        printRed(f'''Unknown option '{cll[0]}'. I will not use your '{cll[1]}' value in any way.''')
                elif cl != "":
                    if i < len (command_options[c]["name"]):
                        print(f'''I will use '{cl}' for option '{command_options[c]["name"][i]}'.''')
                        options[command_options[c]["name"][i]] = cl
                    else:
                        printRed(f'''Too many options given. I will not use your '{cl}' value in any way.''')
            break

    for i, z in enumerate(zip(command_options[command]["name"], command_options[command]["required"], command_options[command]["default"], command_options[command]["type"])):
        n, r, d, t = z[0], z[1], z[2], z[3]
        execute = True
        print(f'''i:{i}, name:{n}, required:{r}, default:{d}, type:{t}''')
        if r:
            #assert command_options[command]["name"][i] in options
            if n not in options:
                printRed(f'''Missing required argument '{n}'. Command won't be executed.''')
                execute = False
                break
        if n not in options and d is not None:
            print(f'''Default argument '{n}' set to '{d}'.''')
            options[n] = d
        if n in options:
            if isinstance(t, list):
                bCond = options[n] in t
                #print(options[n], t, bCond)
                sTxt = f'''Value '{options[n]}' is not valid for option '{n}'. Use one of these options: {t}.'''
                Assert(bCond, sTxt)
                if not bCond:
                    execute = False
                    break
            elif t == "int":
                try:
                    options[n] = int(options[n])
                except Exception as e:
                    traceback.print_exc()
                assert isinstance(options[n], int)
            elif t == "intlist":
                lst_old = options[n].split(" ")
                lst_new = []
                for l_old in lst_old:
                    l_new = None
                    try:
                        l_new = int(l_old)
                    except Exception as e:
                        traceback.print_exc()
                    assert isinstance(l_new, int)
                    if l_new not in lst_new: lst_new.append(l_new)
                options[n] = lst_new
            elif t == "strlist":
                if '"' in options[n] or "'" in options[n]:
                    print("Uvozovky")
                else:
                    lst_old = options[n].split(" ")
                    lst_new = []
                    for l_old in lst_old:
                        if l_old not in lst_new: lst_new.append(l_old)
                    options[n] = lst_new

    if not execute:
        command = ""
        options = []
    else:
        printoptions = {}
        for op in options:
            if isinstance(options[op], str):
                printoptions[op] = "'" + options[op] + "'"
            else:
                printoptions[op] = options[op]
        printYellow(f'''Comand '{command}' with options {', '.join([str(str(op) + "=" + str(printoptions[op])) for op in printoptions])}.''')

    return command, options

def get_sql_queries_dict(lst):
    for sql_filename in lst:
        #print("SQL file:", sql_file)
        file_exists, full_filename = check_filename(sql_filename)
        #print("Check if file exists:", sql_file_exists)
        if file_exists:
            with open(full_filename, mode="r", encoding="utf-8") as f:
                sql = f.read()
                #print("SQL file query:")
                #print(sql.strip(), sql.count(";"))
                parseSql(full_filename, sql)
        else:
            print("! SQL file:", sql_filename, "does not exist !")
    return None

def check_foldername(foldername, foldername_old):
    folder_exists = False
    full_foldername = None
    if not os.path.isabs(foldername):
        if foldername_old:
            full_foldername = os.path.join(foldername_old, foldername)
            folder_exists = os.path.isdir(full_foldername)
        else:
            full_foldername = os.path.join(os.getcwd(), foldername)
            folder_exists = os.path.isdir(full_foldername)
    else:
        folder_exists = os.path.isdir(foldername)
        full_foldername = foldername
    return folder_exists, full_foldername

def check_filename(filename):
    file_exists = False
    full_filename = None
    if folder_exists and not os.path.isabs(filename):
        full_filename = os.path.realpath(os.path.join(folder_name, os.path.expanduser(filename)))
    else:
        full_filename = filename
    file_exists = os.path.isfile(full_filename)
    #print(full_filename)
    return file_exists, full_filename

def show_data():
    row_format = "{:>15}" * (len(columns) + 1)
    nrows = len(data)
    if nrows <= show_cases*2:
        printInvGreen("There are {} rows. Showing all cases.".format(str(nrows)))
        print(row_format.format("(Row)", *columns))
        for i, row in enumerate(data):
            #print(row_format.format(str(i), *row)) # not posiible to pass None (Null in db)
            print(row_format.format(str(i+1), *[str(r) for r in row]))    # Null to None
    else:
        printInvGreen("There are {} rows. Showing first / last {} cases.".format(str(nrows), str(show_cases)))
        print(row_format.format("(Row)", *columns))
        for i, row in enumerate(data[:show_cases]):
            print(row_format.format(str(i+1), *[str(r) for r in row]))    # Null to None
        print("\n","...","\n")
        for i, row in enumerate(data[-show_cases:]):
            print(row_format.format(str(nrows-show_cases+i+1), *[str(r) for r in row]))    # Null to None

def do_sql(sql):

    global conn, data, columns, db_filename, folder_exists, folder_name, db_version, db_schema

    time.sleep(1)

    OK = 1
    if sql.startswith("\\"):
        command, options = parseCommand(sql)
        if command == "quit" or command == "q":
            OK = 0

        elif command == "sqlite3":
            if options["filename"] == ":memory:":
                print("\n" + "Using database in memory. Save or loose!")
                try:
                    conn = sqlite3.connect(":memory:")
                    db_version = "Sqlite3 (memory): "
                except Exception as e:
                    traceback.print_exc()
            else:
                db_filename = options["filename"]
                file_exists, full_filename = check_filename(db_filename)
                if file_exists:
                    print("Using database '{}'.".format(full_filename))
                else:
                    print("Creating database '{}'.".format(full_filename))
                try:
                    conn = sqlite3.connect(full_filename)
                    db_version = f"Sqlite3 ({full_filename}): "
                except Exception as e:
                    traceback.print_exc()

        elif command == "mysql":
            db_schema = options["schema"]
            try:
                print("Using mysqlclient version:", version("mysqlclient"))
                import MySQLdb
                #import mysql.connector
                #from mysql.connector import errorcode
                #can use errno

                #cnx = mysql.connector.connect(user="scott", database="test")
                #cursor = cnx.cursor()
                #connpars = parse_connstring(connstring)
                #print(connpars["server"])
                #print(connpars["user"])
                #print(connpars["password"])
                try:
                    conn = MySQLdb.connect("localhost", "root", "admin", use_unicode=True,charset="utf8")
                    #conn = mysql.connector.connect(host = "localhost", user = "root", password="admin", use_unicode=True,charset="utf8")
                    try:
                        c = conn.cursor()
                        c.execute("""use {}""".format(db_schema))
                        conn.commit()
                        db_version = f"MySQL ({db_schema}): "
                    except Exception as e:
                        traceback.print_exc()
                        db_version = f"MySQL (No schema!): "
                        print(e.__class__)

                except Exception as e:
                    traceback.print_exc()

            except Exception as e:
                print("No MySQL support. Please run 'pip install mysqlclient'.\n")
                traceback.print_exc()

        elif command == "folder":
            folder_exists_old = folder_exists
            folder_name_old = folder_name
            #folder_name = sql[len("\folder:"):]
            folder_name = options["foldername"]
            #folder = os.path.isdir(folder_name)
            folder_exists, full_foldername = check_foldername(folder_name, folder_name_old)
            if folder_exists:
                print(f'''Using folder '{full_foldername}'.''')
                folder_name = full_foldername
            else:
                if folder_exists_old:
                    print(f'''Folder '{folder_name}' does not exist. Using current folder '{folder_name_old}'.''')
                    folder_exists = folder_exists_old
                    folder_name = folder_name_old
                else:
                    # folder_name_old is None if sql imported file has wrong \folder command
                    print("Folder '{}' does not exist. Using working directory '{}'.".format(folder_name, os.getcwd()))
                    folder_name = os.getcwd()

        elif command == "read":
            read_filename = options["filename"]
            file_exists, full_filename = check_filename(read_filename)
            print("Read: '{}'".format(read_filename))
            try:
                with open(full_filename, "r", encoding = "utf-8") as f:
                    data_new = []
                    columns_new = []
                    i = 0
                    data_line = f.readline()
                    if data_line[-1:] == "\n": data_line = data_line[:-1]
                    while data_line:
                        row_new = []
                        for c in data_line.split(";"):
                            if i == 0:
                                columns_new.append(c)
                            else:
                                if c != "":
                                    row_new.append(c)
                                else:
                                    row_new.append(None)
                        if i > 0: data_new.append(row_new)
                        i += 1
                        data_line = f.readline()
                        if data_line[-1:] == "\n": data_line = data_line[:-1]
                    #print(data_new)
                    if len(data_new) > 0:
                        data = data_new
                        columns = columns_new
                        show_data()
                    else:
                        print()
                        print("! There are no data returned from this sql query !")
            except Exception as e:
                traceback.print_exc()

        elif command == "import":
            sql_filename = options["filename"]
            file_exists, full_filename = check_filename(sql_filename)
            #print("Check if file exists:", sql_file_exists)
            if file_exists:
                with open(full_filename, "r") as f:
                    sql = f.read()
                    #print("SQL file query:")
                    #print(sql.strip(), sql.count(";"))
                    parseSql(full_filename, sql)
                for i, sql in enumerate(sqls[full_filename]):
                    print(f'''\n\\\\ SQL file '{full_filename}' command no {str(i+1)} \\\\''')
                    do_sql(sql)
            else:
                print(f'''\n! SQL file '{full_filename}' does not exist !''')

        elif command == "insert":
            tablename = options["tablename"]
            #print("\n" + "Insert:", tablename)
            part1 = ""
            part2 = ""
            try:
                for i, c in enumerate(columns):
                    if i == 0:
                        part1 += "{{0[{}]}}".format(str(i))
                        if db_version[:7] == "Sqlite3":
                            part2 += "?".format(str(i))
                        elif db_version[:5] == "MySQL":
                            part2 += "%s".format(str(i))
                    else:
                        part1 += ",{{0[{}]}}".format(str(i))
                        if db_version[:7] == "Sqlite3":
                            part2 += ",?".format(str(i))
                        elif db_version[:5] == "MySQL":
                            part2 += ",%s".format(str(i))
                sql = f'''insert into {tablename} ({part1}) values ({part2})'''
                print()
                print(db_version + sql)
                #print(columns, data)
                c = conn.cursor()
                c.executemany(sql.format(columns), data)
                conn.commit()
                print("! There are no data returned from this sql query !")
            except Exception as e:
                traceback.print_exc()

        elif sql.startswith("\save:"):
            save_filename = sql[len("\save:"):]
            file_exists, full_filename = check_filename(save_filename)
            print("Save: '{}'".format(save_filename))
            try:
                with open(full_filename, "w") as f:
                    for c in columns:
                        f.write(str(c) + "\t")
                    f.write("\n")
                    for d in data:
                        for c in d:
                            f.write(str(c) + "\t")
                        f.write("\n")
            except Exception as e:
                traceback.print_exc()

        elif command == "print":
            if options["what"] == "columns":
                print(", ".join([str(c) for c in columns]))

            elif options["what"] == "data":
                fromm = options["from"]
                too = options["to"]
                stepp = options["step"]
                print(fromm, too, stepp)
                row_format = "{:>15}" * (len(columns) + 1)
                nrows = len(data)
                if fromm <= 0: fromm = 1
                if too <= 0: too = 1
                if stepp <= 0: stepp = 1
                if too > nrows: too = nrows
                print("There are {} rows. Showing cases {} to {} step {}.".format(str(nrows), str(fromm), str(too), str(stepp)))
                print(row_format.format("(Row)", *columns))
                for i, row in enumerate(data[fromm-1:too:stepp]):
                    print(row_format.format(str(fromm+i*stepp), *[str(r) for r in row]))    # Null to None
                print("\n")

        elif sql.startswith("\pause:"):
            if "ask" in sql:
                asked = ""
                while asked != "c" and asked != "q":
                    asked = input("Paused. C for continue, D for data view, Q for quit: ").lower()
                    print(asked)
                    if asked == "d":
                        show = "Error"
                        if data:
                            #columns = [col[0] for col in c.description]
                            row_format = "{:>15}" * (len(columns) + 1)
                            nrows = len(data)
                            if nrows > 0:   #< 100
                                show = "There are {} rows. Showing all cases.".format(str(nrows))
                                show += "\n"
                                show += row_format.format("(Row)", *columns)
                                show += "\n"
                                for i, row in enumerate(data):
                                    #print(row_format.format(str(i), *row)) # not posiible to pass None (Null in db)
                                    show += row_format.format(str(i+1), *[str(r) if len(str(r)) <= 15 else str(r)[:13]+".." for r in row])    # Null to None
                                    show += "\n"
                            else:
                                print("There are {} rows. Showing first / last {} cases.".format(str(nrows), str(10)))
                                print(row_format.format("(Row)", *columns))
                                for i, row in enumerate(data[:10]):
                                    print(row_format.format(str(i+1), *[str(r) for r in row]))    # Null to None
                                print("\n","...","\n")
                                for i, row in enumerate(data[-10:]):
                                    print(row_format.format(str(nrows-10+i+1), *[str(r) for r in row]))
                        zobraz(show)
                    elif asked == "q":
                        OK = 0


        else:
            print("! Command was not recognized or missing arguments !")
    else:
        printBlue(db_version + sql + "\n")
        data_new = None
        try:
            c = conn.cursor()
            c.execute(""'{}'"".format(sql))
            data_new = c.fetchall()
            if data_new:
                data = data_new
                columns = [col[0] for col in c.description]
                show_data()
            else:
                print("! There are no data returned from this sql query !")
            conn.commit()
            #conn.close()
        except Exception as e:
            traceback.print_exc()
            data = None
            columns = None
    #print()
    # this checks dtb
    if db_version[:5] == "MySQL":
        #print(conn.get_proto_info())
        try:
            c = conn.cursor()
            c.execute(""'{}'"".format("SELECT database();"))
            data_new = c.fetchall()
            db_schema = data_new[0][0]
            db_version = f"MySQL ({db_schema}): "
        except Exception as e:
            traceback.print_exc()
    sql = ""
    return OK

def main(argv):

    global folder_name

    default_options = 7
    for key1 in command_options.keys():
        assert len(command_options[key1].keys()) == default_options, \
f'''Command {key1} has {len(command_options[key1].keys())} options \
instead of default {default_options}.'''
        for key2 in command_options[key1].keys():
            if key2 != "help1" and key2 != "alternative":
                assert len(command_options[key1]["name"]) == len(command_options[key1][key2]), \
f'''Command option {key1} has {len(command_options[key1]["name"])} names \
but {len(command_options[key1][key2])} '{key2}'.'''

    namespace = parseArgv(argv)
    """
    for k,v in vars(namespace).items():
        print(k, v)
    """

    if len(vars(namespace)["sql_files"]) > 0:
        get_sql_queries_dict(vars(namespace)["sql_files"])
        #print(sqls)

        for sql_filename in sqls.keys():
            #OK_returned = 1
            for i, sql in enumerate(sqls[sql_filename]):
                printCom("\n\\\\" + " SQL file '{}' command no {} ".format(sql_filename, str(i+1)) + "\\\\")
                #print(sql)
                #print()
                OK_returned = do_sql(sql)
                if OK_returned == 0: break

    if len(vars(namespace)["sql_files"]) == 0 and isinstance(vars(namespace)["interactive"], str) or vars(namespace)["interactive"]:
        print("\nEntering interactive mode. Type '\quit' to quit.")

        if conn:
            if db_version[:7] == "Sqlite3":
                print("Using Sqlite3 database '{}'. Use \sqlite3 filename' for change.".format(db_filename))
            elif db_version[:5] == "MySQL":
                print("Using MySQL schema '{}'. Use '\mysql schema' for change.".format(db_schema))
            else:
                print("Sorry, no db_version.")
        else:
            print("Database is not specified. Please use '\sqlite3 filename' for example.")

        if folder_exists:
            print("Using folder '{}'.".format(folder_name))
        else:
            folder_name = os.getcwd()
            print("Folder is not specified. Using working directory '{}'.".format(folder_name))
        print()

        interactive_pass = 0
        sql = input(db_version)
        OK_returned = 1

        while OK_returned == 1:

            interactive_pass += 1

            sql_file = "interactive pass " + str(interactive_pass)
            parseSql(sql_file, sql)
            #OK_returned = 1
            for i, sql in enumerate(sqls[sql_file]):
                printCom(f'''\n\\\\ SQL file '{sql_file}' command no {str(i+1)} \\\\''')
                #print(sql)
                #print()
                OK_returned = do_sql(sql)
                if OK_returned == 0: break
            if OK_returned == 1:
                print()
                sql = input(db_version)

    try:
        conn.close()
    except Exception as e:
        #traceback.print_exc()
        pass
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
