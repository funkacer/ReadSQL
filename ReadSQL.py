#import socket
#print(socket.gethostname())

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
import socket
import time
import random

from importlib.metadata import version

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

RED, YELLOW, GREEN, BLUE, COM, INVGREEN, INVRED, END = '\033[91m', '\033[33m', '\033[4m', '\033[34m', '\033[4m', '\033[97m\033[42m', '\033[97m\033[101m', '\033[0m'
printRed = lambda sTxt: print(RED + sTxt + END)
printYellow = lambda sTxt: print(YELLOW + sTxt + END)
printBlue = lambda sTxt: print(BLUE + sTxt + END)
printCom = lambda sTxt: print(COM + sTxt + END)
printInvGreen = lambda sTxt: print(INVGREEN + sTxt + END)
printInvRed = lambda sTxt: print(INVRED + sTxt + END)
Assert = lambda bCond=False, sTxt='': printRed(sTxt) if not bCond else None

printInvRed("KO")
printInvGreen("OK")

row_format_l = lambda columns: "".join([f"{{:>{columns[c]}}}" for c in columns]) if isinstance(columns, dict) else "{:>15}" * (len(columns) + 1)

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
command_options["quit"]["altoption"] = []

command_options["folder"] = {}
command_options["folder"]["name"] = ["foldername"]
command_options["folder"]["required"] = [True]
command_options["folder"]["type"] = ["str"]
command_options["folder"]["default"] = [None]
command_options["folder"]["help1"] = "Help for command 'folder'"
command_options["folder"]["help2"] = ["Blabla1"]
command_options["folder"]["alternative"] = ["f"]
command_options["folder"]["altoption"] = [["f","fn"]]

command_options["sqlite3"] = {}
command_options["sqlite3"]["name"] = ["filename"]
command_options["sqlite3"]["required"] = [False]
command_options["sqlite3"]["type"] = ["str"]
command_options["sqlite3"]["default"] = [":memory:"]
command_options["sqlite3"]["help1"] = "Help for command 'folder'"
command_options["sqlite3"]["help2"] = ["Blabla1"]
command_options["sqlite3"]["alternative"] = ["sqlite", "sql3", "sql", "sq", "s"]
command_options["sqlite3"]["altoption"] = [["f"]]

command_options["mysql"] = {}
command_options["mysql"]["name"] = ["database", "user", "password", "host", "port"]
command_options["mysql"]["required"] = [False, False, False, False, False]
command_options["mysql"]["type"] = ["str", "str", "str", "str", "int"]
command_options["mysql"]["default"] = ["", "root", "admin", "localhost", 3306]
command_options["mysql"]["help1"] = "Help for command 'folder'"
command_options["mysql"]["help2"] = ["Bla1", "Bla2", "Bla3", "Bla4", "Bla5"]
command_options["mysql"]["alternative"] = ["my"]
command_options["mysql"]["altoption"] = [["d"],["u"],["p"],["h"],["po"]]

command_options["postgre"] = {}
command_options["postgre"]["name"] = ["database", "user", "password", "host", "port"]
command_options["postgre"]["required"] = [False, False, False, False, False]
command_options["postgre"]["type"] = ["str", "str", "str", "str", "int"]
command_options["postgre"]["default"] = ["", "postgres", "postgres1", "localhost", 5432]
command_options["postgre"]["help1"] = "Help for command 'folder'"
command_options["postgre"]["help2"] = ["Bla1", "Bla2", "Bla3", "Bla4", "Bla5"]
command_options["postgre"]["alternative"] = ["pg"]
command_options["postgre"]["altoption"] = [["d"],["u"],["p"],["h"],["po"]]

command_options["mssql"] = {}
command_options["mssql"]["name"] = ["database", "user", "password", "host", "port"]
command_options["mssql"]["required"] = [False, False, False, False, False]
command_options["mssql"]["type"] = ["str", "str", "str", "str", "int"]
command_options["mssql"]["default"] = ["", "root", "admin", "localhost", 3306]
command_options["mssql"]["help1"] = "Help for command 'folder'"
command_options["mssql"]["help2"] = ["Bla1", "Bla2", "Bla3", "Bla4", "Bla5"]
command_options["mssql"]["alternative"] = ["ms"]
command_options["mssql"]["altoption"] = [["d"],["u"],["p"],["h"],["po"]]

command_options["read"] = {}
command_options["read"]["name"] = ["filename", "delimiter"]
command_options["read"]["required"] = [True, False]
command_options["read"]["type"] = ["str", "str"]
command_options["read"]["default"] = [None, ";"]
command_options["read"]["help1"] = "Help for command 'folder'"
command_options["read"]["help2"] = ["Blabla1", "Blablabla2"]
command_options["read"]["alternative"] = ["r"]
command_options["read"]["altoption"] = [["f"],["d"]]

command_options["export"] = {}
command_options["export"]["name"] = ["filename", "delimiter"]
command_options["export"]["required"] = [True, False]
command_options["export"]["type"] = ["str", "str"]
command_options["export"]["default"] = [None, ";"]
command_options["export"]["help1"] = "Help for command 'folder'"
command_options["export"]["help2"] = ["Blabla1", "Blablabla2"]
command_options["export"]["alternative"] = ["e"]
command_options["export"]["altoption"] = [["f"],["d"]]

command_options["load"] = {}
command_options["load"]["name"] = ["filename"]
command_options["load"]["required"] = [True]
command_options["load"]["type"] = ["str"]
command_options["load"]["default"] = [None]
command_options["load"]["help1"] = "Help for command 'folder'"
command_options["load"]["help2"] = ["Blabla1"]
command_options["load"]["alternative"] = ["l"]
command_options["load"]["altoption"] = [["f"]]

command_options["insert"] = {}
command_options["insert"]["name"] = ["tablename"]
command_options["insert"]["required"] = [True]
command_options["insert"]["type"] = ["str"]
command_options["insert"]["default"] = [None]
command_options["insert"]["help1"] = "Help for command 'folder'"
command_options["insert"]["help2"] = ["Blabla1"]
command_options["insert"]["alternative"] = ["i"]
command_options["insert"]["altoption"] = [["t"]]

command_options["print data"] = {}
command_options["print data"]["name"] = ["from", "to", "step", "random", "list", "columns", "what"]
command_options["print data"]["required"] = [False, False, False, False, False, False, False]
command_options["print data"]["type"] = ["int", "int", "int", "int", "intlist", "strlist",["data"]]
command_options["print data"]["default"] = [0, 0, 1, 0, "[]", "[]", "data"]
command_options["print data"]["help1"] = "Help for command 'folder'"
command_options["print data"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6", "Bla7"]
command_options["print data"]["alternative"] = ["pd"]
command_options["print data"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["w"]]

command_options["print columns"] = {}
command_options["print columns"]["name"] = ["what", "from", "to", "step", "list", "columns"]
command_options["print columns"]["required"] = [False, False, False, False, False, False]
command_options["print columns"]["type"] = [["columns"], "int", "int", "int", "intlist", "strlist"]
command_options["print columns"]["default"] = ["columns", 0, print_max_default, 1, None, None]
command_options["print columns"]["help1"] = "Help for command 'folder'"
command_options["print columns"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6"]
command_options["print columns"]["alternative"] = ["pc"]
command_options["print columns"]["altoption"] = [["f"], ["t"], ["s"], ["l"], ["c"], ["w"]]

command_options["print"] = {}
command_options["print"]["name"] = ["what", "from", "to", "step", "list", "columns"]
command_options["print"]["required"] = [False, False, False, False, False, False]
command_options["print"]["type"] = [["data","columns"], "int", "int", "int", "intlist", "strlist"]
command_options["print"]["default"] = ["data", 0, print_max_default, 1, None, None]
command_options["print"]["help1"] = "Help for command 'folder'"
command_options["print"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6"]
command_options["print"]["alternative"] = ["p"]
command_options["print"]["altoption"] = [["w"],["f"], ["t"], ["s"], ["l"], ["c"]]

command_options["break"] = {}
command_options["break"]["name"] = ["what", "from", "to", "step", "list", "columns"]
command_options["break"]["required"] = [False, False, False, False, False, False]
command_options["break"]["type"] = [["data","columns"], "int", "int", "int", "intlist", "strlist"]
command_options["break"]["default"] = ["data", 0, print_max_default, 1, None, None]
command_options["break"]["help1"] = "Help for command 'folder'"
command_options["break"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6"]
command_options["break"]["alternative"] = ["b"]
command_options["break"]["altoption"] = [["w"],["f"], ["t"], ["s"], ["l"], ["c"]]

def data_select():
    global fromm, too, stepp, randd, listt, colss, listi
    nrows = len(data)
    ncols = len(columns)
    colsi = range(1, ncols + 1)
    if len(colss) > 0:
        colsi = []
        for cols in colss:
            if cols in columns:
                colsi.append(columns.index(cols) + 1)
            else:
                printRed(f"Column '{cols}' not in columns!")
    #columns_show = [columns[i] for i in colsi] # only existing
    rowsi = []
    listi = []
    if len(listt) > 0:
        #assert list in range of cases
        for l in listt:
            if l < 0: l += nrows + 1
            if l <= 0: l = 1    # if l was lower than -nrows
            if l > nrows: l = nrows
            if l not in listi: listi.append(l)
    if fromm < 0:
        fromm += nrows + 1
        if too == 0: too = nrows
    if too < 0:
        too += nrows + 1
        if fromm == 0: fromm = nrows
    if too < fromm:
        pom = fromm
        fromm = too
        too = pom
    if stepp <= 0: stepp = 1
    if too > nrows: too = nrows
    if fromm < 1: fromm = 1
    if randd > 0:
        if too == 0: too = nrows
        if len(listi) > 0:
            # select from listt
            # cannot select 2 same cases in list when 0,1 or >nrows => make set
            #listi = list(set(listi))
            if randd > len(listi): randd = len(listi)
            for i in range(randd):
                r = random.choice(listi)
                while r in rowsi:
                    r = random.choice(listi)
                rowsi.append(r)
        else:
            # select fromm-too-stepp
            randmax = int((too-fromm)/stepp) + 1
            #print(fromm, too, stepp, randd, randmax)
            if randd > randmax: randd = randmax
            #if randd == 0: randd = 1
            for i in range(randd):
                r = random.randrange(fromm, too+1, stepp)
                while r in rowsi:
                    r = random.randrange(fromm, too+1, stepp)
                rowsi.append(r)
        #print(listt_show)
    else:
        if len(listi) > 0:
            rowsi = listi
        else:
            rowsi = range(fromm, too+1, stepp)
    return rowsi, colsi


def data_profile(rowsi, colsi):
    nrows = len(data)
    ncols = len(columns)
    colsw = {}
    colsw['(Row)'] = 5  # Columns 0 is Row number with header '(Row)' = 5 chars
    for ci in colsi:
        colsw[columns[ci-1]] = len(columns[ci-1]) + 1
    for ri in rowsi:
        if len(str(ri)) > colsw['(Row)']: colsw['(Row)'] = len(str(ri))
        for ci in colsi:
            w = len(str(data[ri-1][ci-1])) + 1
            if w > colsw[columns[ci-1]]: colsw[columns[ci-1]] = w
    return colsw

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

def parseText(myText, delimiter):

    #print("Uvozovky", myText.count('"'), myText.count("'"))

    lst_new = []
    apos = None
    maxs = -1
    spl = delimiter
    for i, chr in enumerate(myText):
        if not apos and (chr == spl):
            app_text = myText[maxs+1:i].strip()
            if app_text != "": lst_new.append(app_text)
            maxs = i
        elif not apos and (chr == '"' or chr == "'" or chr == "["):
            # Are there any items before the first apostrophe?
            #lst_new += [o.strip() for o in myText[maxx+1:i].split(spl) if o.strip() is not ""]
            apos = chr
            if apos == "[": apos = "]"
            #print(lst_new)
            #print(chr, i)
        elif chr == apos:
            # first line for strlistsplit, senond for sql parse
            #lst_new.append(myText[apos+1:i])
            #lst_new.append(myText[maxs+1:i].strip())
            #print(chr, i)
            apos = None
        # Are there any items after the last apostrophe?
        #if maxa < len(myText): lst_new += [o.strip() for o in myText[maxa+1:].split(spl) if o.strip() is not ""]

    app_text = myText[maxs+1:].strip()
    if app_text != "": lst_new.append(app_text)

    #print(lst_new)

    return lst_new


def parseCommand(command_line):
    command = ""
    options = {}
    #error = 0
    execute = True
    #command_line = command_line.replace(" ", "")
    command_line = command_line[1:].strip() #no slash
    #print (command_line)
    for c in command_options:
        #print(c)
        if command_line[:len(c)].lower() == c:
            command = c
            command_line_list = parseText(command_line[len(c):], ",")
            #print(f"Parse command {command} with ',':", command_line_list)
        else:
            for a in command_options[c]["alternative"]:
                if command_line[:len(a)].lower() == a:
                    command = c
                    command_line_list = parseText(command_line[len(a):], ",")
                if command != "": break
                print(a)
        if command != "": break
        print(c)

    print(command)
    for i, cl in enumerate(command_line_list):
        cl = cl.strip()
        if "=" in cl:
            cll = cl.split("=")
            does_exist = 0
            for j, o in enumerate(command_options[command]["name"]):
                if cll[0].strip() == o:
                    options[o] = cll[1].strip()
                    does_exist = 1
                else:
                    for a in command_options[command]["altoption"][j]:
                        if cll[0].strip().lower() == a:
                            options[o] = cll[1].strip()
                            does_exist = 1
                        if does_exist: break
                        print(a)
            if not does_exist:
                printRed(f'''Unknown option '{cll[0]}'. I will not use your '{cll[1]}' value in any way.''')
        elif cl != "":
            if i < len (command_options[command]["name"]):
                #print(f'''I will use '{cl}' for option '{command_options[c]["name"][i]}'.''')
                options[command_options[command]["name"][i]] = cl
            else:
                printRed(f'''Too many options given. I will not use your '{cl}' value in any way.''')

    for i, z in enumerate(zip(command_options[command]["name"], command_options[command]["required"], command_options[command]["default"], command_options[command]["type"])):
        n, r, d, t = z[0], z[1], z[2], z[3]
        #print(f'''i:{i}, name:{n}, required:{r}, default:{d}, type:{t}''')
        if r:
            #assert command_options[command]["name"][i] in options
            if n not in options:
                printRed(f'''Missing required argument '{n}'. Command not executed.''')
                execute = False
                break
        if n not in options and d is not None:
            #print(f'''Default argument '{n}' set to '{d}'.''')
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
            elif t == "str":
                #options[n] = options[n].strip('"')
                if len(options[n]) > 0:
                    if options[n][0] == '"' and options[n][-1] == '"':
                        options[n] = options[n].strip('"')
                    elif options[n][0] == "'" and options[n][-1] == "'":
                        options[n] = options[n].strip("'")
                #print(f"Parse option '{n}' as string:", options[n])
                #command = "quit"
            elif t == "int":
                try:
                    options[n] = int(options[n])
                except Exception as e:
                    traceback.print_exc()
                assert isinstance(options[n], int)
                #print(f"Parse option '{n}' as integer:", options[n])
            elif t == "intlist":
                if options[n][0] == "[" and options[n][-1] == "]":
                    lst_old = parseText(options[n][1:-1], ",")
                    #print(f"Parse intlist {options[n]} with ',':", lst_old)
                else:
                    lst_old = parseText(options[n], " ")
                    #print(f"Parse intlist {options[n]} with ' ':", lst_old)
                #print(lst_old)
                #lst_old = options[n].split(" ")
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
                if options[n][0] == "[" and options[n][-1] == "]":
                    lst_old = parseText(options[n][1:-1], ",")
                    #print(f"Parse strlist {options[n]} with ',':", lst_old)
                else:
                    lst_old = parseText(options[n], " ")
                    #print(f"Parse strlist {options[n]} with ' ':", lst_old)
                #print(lst_old)
                lst_new = []
                for l_old in lst_old:
                    if l_old[0] == '"' and l_old[-1] == '"':
                        lst_new.append(l_old.strip('"'))
                    elif l_old[0] == "'" and l_old[-1] == "'":
                        lst_new.append(l_old.strip("'"))
                    else:
                        lst_new.append(l_old)
                options[n] = lst_new

    if not execute:
        command = ""
        options = []
        print()
    else:
        printoptions = {}
        for op in options:
            if isinstance(options[op], str):
                printoptions[op] = "'" + options[op] + "'"
            else:
                printoptions[op] = options[op]
        printYellow(f'''Command '{command}' with options {', '.join([str(str(op) + "=" + str(printoptions[op])) for op in printoptions])}.''')
        print()

    return command, options

def get_sql_queries_dict(lst):
    sqls_local = {}
    for sql_filename in lst:
        #print("SQL file:", sql_file)
        file_exists, full_filename = check_filename(sql_filename)
        #print("Check if file exists:", sql_file_exists)
        if file_exists:
            with open(full_filename, mode="r", encoding="utf-8") as f:
                sql = f.read()
                #print("SQL file query:")
                #print(sql.strip(), sql.count(";"))
                sqls_local[full_filename] = parseText(sql, ";")
        else:
            printRed(f'''! SQL file '{full_filename}' does not exist !''')
    return sqls_local

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

def print_data():
    global fromm, too, stepp, randd, listt, colss
    nrows = len(data)
    ncols = len(columns)
    fromm = 1
    too = nrows
    stepp = 1
    colss = []
    listt = []
    randd = 0

    if nrows <= show_cases*2:
        rowsi, colsi = data_select()
        #print(rows_show)
        colsw = data_profile(rowsi, colsi)
        row_format = row_format_l(colsw)
        #print(row_format)
        printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing all cases with all columns.")
        print(row_format.format(*colsw))
        for ri in rowsi:
            print(row_format.format(str(ri), *[str(col) for col in [data[ri-1][ci-1] for ci in colsi]]))    # Null to None
    else:
        listt = list(range(1,show_cases+1))
        listt += list(range(nrows-show_cases+1, nrows +1))
        #print(listt)
        rowsi, colsi = data_select()
        #print(rows_show)
        colsw = data_profile(rowsi, colsi)
        row_format = row_format_l(colsw)
        #print(row_format)
        printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing first / last {show_cases} cases with all columns.")
        print(row_format.format(*colsw))
        for ri in range(1,show_cases+1):
            print(row_format.format(str(ri), *[str(col) for col in [data[ri-1][ci-1] for ci in colsi]]))    # Null to None
        print(row_format.format("...", *["" for c in columns]))
        for ri in range(nrows-show_cases+1, nrows +1):
            print(row_format.format(str(ri), *[str(col) for col in [data[ri-1][ci-1] for ci in colsi]]))    # Null to None

def do_sql(sql):

    global conn, data, columns, db_filename, folder_exists, folder_name, db_version, db_schema, \
            fromm, too, stepp, randd, listt, colss

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
            #"database", "user", "password", "host", "port"
            database = options["database"]
            user = options["user"]
            password = options["password"]
            host = options["host"]
            port = options["port"]
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
                    conn = MySQLdb.connect(database = database, \
                    user = user, password = password, host = host, \
                    port = port, use_unicode=True,charset="utf8")
                    conn.autocommit(True)
                    #conn = mysql.connector.connect(host = "localhost", user = "root", password="admin", use_unicode=True,charset="utf8")
                    db_version = f"MySQL (Add schema!): "
                except Exception as e:
                    traceback.print_exc()

            except Exception as e:
                print("No MySQL support. Please run 'pip install mysqlclient'.\n")
                traceback.print_exc()

        elif command == "postgre":
            #"database", "user", "password", "host", "port"
            database = options["database"]
            user = options["user"]
            password = options["password"]
            host = options["host"]
            port = options["port"]
            try:
                print("Using psycopg2 version:", version("psycopg2"))
                import psycopg2
                try:
                    conn = psycopg2.connect(database = database, \
                    user = user, password = password, host = host, \
                    port = port)
                    conn.set_session(autocommit=True)
                    #conn = mysql.connector.connect(host = "localhost", user = "root", password="admin", use_unicode=True,charset="utf8")
                    db_version = f"PostgreSQL (Add schema!): "
                except Exception as e:
                    traceback.print_exc()
            except Exception as e:
                print("No MySQL support. Please run 'pip install mysqlclient'.\n")
                traceback.print_exc()

        elif command == "mssql":
            #"database", "user", "password", "host", "port"
            database = options["database"]
            user = options["user"]
            password = options["password"]
            host = options["host"]
            port = options["port"]
            server = socket.gethostname()
            try:
                print("Using pyodbc version:", version("pyodbc"))
                import pyodbc
                try:
                    conn = pyodbc.connect('Driver={SQL Server};'
                      f'Server={server}\SQLEXPRESS;'
                      f'Database={database};'
                      'Trusted_Connection=yes;')
                    conn.autocommit = True
                    #conn = mysql.connector.connect(host = "localhost", user = "root", password="admin", use_unicode=True,charset="utf8")
                    db_version = f"MsSQL (Add schema!): "
                except Exception as e:
                    traceback.print_exc()
            except Exception as e:
                print("No MsSQL support. Please run 'pip install pyodbc'.\n")
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
                    printRed(f'''Folder '{folder_name}' does not exist. Using current folder '{folder_name_old}'.''')
                    folder_exists = folder_exists_old
                    folder_name = folder_name_old
                else:
                    # folder_name_old is None if sql imported file has wrong \folder command
                    printRed("Folder '{}' does not exist. Using working directory '{}'.".format(folder_name, os.getcwd()))
                    folder_name = os.getcwd()

        elif command == "read":
            read_filename = options["filename"]
            read_delimiter = options["delimiter"]
            file_exists, full_filename = check_filename(read_filename)
            #print("Read: '{}'".format(read_filename))
            try:
                with open(full_filename, "r", encoding = "utf-8") as f:
                    data_new = []
                    columns_new = []
                    i = 0
                    data_line = f.readline()
                    while data_line:
                        if data_line[-1] == "\n": data_line = data_line[:-1]
                        row_new = []
                        for c in data_line.split(read_delimiter):
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
                    #print(data_new)
                    if len(data_new) > 0:
                        data = data_new
                        columns = columns_new
                        print_data()
                    else:
                        print()
                        print("! There are no data returned from this sql query !")
            except Exception as e:
                traceback.print_exc()

        elif command == "export":
            export_filename = options["filename"]
            export_delimiter = options["delimiter"]
            file_exists, full_filename = check_filename(export_filename)
            #print("Export: '{}'".format(export_filename))
            col_len = len(columns)-1
            try:
                with open(full_filename, mode="w", encoding="utf-8") as f:
                    for i, c in enumerate(columns):
                        if i < col_len:
                            f.write(str(c) + export_delimiter)
                        else:
                            f.write(str(c))
                    f.write("\n")
                    for d in data:
                        for i, c in enumerate(d):
                            if i < col_len:
                                f.write(str(c) + export_delimiter)
                            else:
                                f.write(str(c))
                        f.write("\n")
            except Exception as e:
                traceback.print_exc()

        elif command == "load":
            #Vratit zpatky db_version a folder pred load
            sql_filename = options["filename"]
            '''
            file_exists, full_filename = check_filename(sql_filename)
            #print("Check if file exists:", sql_file_exists)
            if file_exists:
                with open(full_filename, mode="r", encoding="utf-8") as f:
                    sql = f.read()
                    #print("SQL file query:")
                    #print(sql.strip(), sql.count(";"))
                    sqls_load = parseText(sql, ";")
                for i, sql in enumerate(sqls_load):
                    printCom(f"\n\\\\ SQL file '{full_filename}' loaded command no {str(i+1)} \\\\")
                    do_sql(sql)
            else:
                printRed(f"! SQL file '{full_filename}' does not exist !")
            '''
            sqls_load = get_sql_queries_dict([sql_filename])
            for full_filename in sqls_load.keys():
                #OK_returned = 1
                for i, sql_load in enumerate(sqls_load[full_filename]):
                    printCom(f"\n\\\\ SQL file '{full_filename}' command no {str(i+1)} \\\\")
                    #print(sql)
                    #print()
                    OK_returned = do_sql(sql_load)
                    if OK_returned == 0: break

        elif command == "insert":
            tablename = options["tablename"]
            #print(columns)
            #print("\n" + "Insert:", tablename)
            part1 = ""
            part2 = ""
            if db_version[:7] == "Sqlite3":
                for i, c in enumerate(columns):
                    if i == 0:
                        #part1 += '''{{0[{}]}}'''.format(str(i))
                        part1 += f"{{0[{str(i)}]}}"
                        #part2 += '''?'''.format(str(i))
                        part2 += "?"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",?"
                    #print(i)
                sql = f'''insert into "{tablename}" ({part1}) values ({part2})'''
                columns_print = []
                for col in columns:
                    columns_print.append(f'''"{col}"''')

            elif db_version[:5] == "MySQL":
                for i, c in enumerate(columns):
                    if i == 0:
                        part1 += f"{{0[{str(i)}]}}"
                        part2 += "%s"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",%s"
                    #print(i)
                sql = f'''insert into `{tablename}` ({part1}) values ({part2})'''
                columns_print = []
                for col in columns:
                    columns_print.append(f'''`{col}`''')

            elif db_version[:10] == "PostgreSQL":
                for i, c in enumerate(columns):
                    if i == 0:
                        part1 += f"{{0[{str(i)}]}}"
                        part2 += "%s"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",%s"
                    #print(i)
                sql = f'''insert into "{tablename}" ({part1}) values ({part2})'''
                columns_print = []
                for col in columns:
                    columns_print.append(f'''"{col}"''')

            elif db_version[:5] == "MsSQL":
                for i, c in enumerate(columns):
                    if i == 0:
                        part1 += f"{{0[{str(i)}]}}"
                        part2 += "?"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",?"
                    #print(i)
                sql = f'''insert into "{tablename}" ({part1}) values ({part2})'''
                columns_print = []
                for col in columns:
                    columns_print.append(f'''"{col}"''')

            print()
            print(db_version + sql)
            #print(columns, data)
            try:
                c = conn.cursor()
                #print(columns_print)
                print(sql.format(columns_print))
                c.executemany(sql.format(columns_print), data)
                conn.commit()
                print("! There are no data returned from this sql query !")
            except Exception as e:
                traceback.print_exc()

        elif command == "print" or command == "print data" or command == "print columns":
            if options["what"] == "columns":
                print(", ".join([str(c) for c in columns]))
            elif options["what"] == "data":
                fromm = options["from"]
                too = options["to"]
                stepp = options["step"]
                listt = options["list"]
                randd = options["random"]
                colss = options["columns"]
                #print(fromm, too, stepp)

                nrows = len(data)
                ncols = len(columns)

                rowsi, colsi = data_select()
                #print(rows_show)

                columns_show = [columns[ci-1] for ci in colsi]

                if len(listt) > 0 and randd == 0:
                    if len(colss) > 0:
                        printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with selected columns {columns_show}.")
                    else:
                        printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with all columns.")
                elif len(listt) > 0 and randd > 0:
                    if len(colss) > 0:
                        printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with selected columns {columns_show}.")
                    else:
                        printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with all columns.")
                elif randd > 0:
                    if len(colss) > 0:
                        printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with selected columns {columns_show}.")
                    else:
                        printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with all columns.")
                else:
                    if len(colss) > 0:
                        printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with selected columns {columns_show}.")
                    else:
                        printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with all columns.")

                colsw = data_profile(rowsi, colsi)
                row_format = row_format_l(colsw)
                #print(row_format)

                print(row_format.format(*colsw))
                for ri in rowsi:
                    print(row_format.format(str(ri), *[str(col) for col in [data[ri-1][ci-1] for ci in colsi]]))    # Null to None

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
        columns_new = None
        error = 0
        try:
            c = conn.cursor()
            #c.execute(""'{}'"".format(sql))
            c.execute(f"{sql}")
        except Exception as e:
            traceback.print_exc()
            print()
        try:
            #conn.commit()
            #print(c.statusmessage)
            data_new = c.fetchall()
            if c.description:
                columns_new = [col[0] for col in c.description]
            #conn.close()
        except Exception as e:
            #traceback.print_exc()
            printInvRed("! Error exexuting this sql query !")
            error = 1
        if data_new or columns_new:
            data = data_new
            columns = columns_new
            print_data()
        elif not error:
            printInvGreen("! There are no data returned from this sql query !")

    # this checks dtb
    if db_version[:5] == "MySQL":
        #print(conn.get_proto_info())
        try:
            c = conn.cursor()
            c.execute("SELECT database();")
            data_new = c.fetchall()
            db_schema = data_new[0][0]
            db_version = f'''MySQL (`{db_schema}`): '''
        except Exception as e:
            traceback.print_exc()
    if db_version[:5] == "MsSQL":
        #print(conn.get_proto_info())
        try:
            c = conn.cursor()
            c.execute("SELECT DB_NAME();")
            data_new = c.fetchall()
            db_schema = data_new[0][0]
            db_version = f'''MsSQL ("{db_schema}"): '''
        except Exception as e:
            traceback.print_exc()
    if db_version[:10] == "PostgreSQL":
        #print(conn.get_proto_info())
        try:
            c = conn.cursor()
            c.execute("SELECT current_database();")
            data_new = c.fetchall()
            db_schema = data_new[0][0]
            db_version = f'''PostgreSQL ("{db_schema}"): '''
        except Exception as e:
            db_version = "None: "
            db_schema = None
            conn = None
            traceback.print_exc()
    # SELECT current_database();
    sql = ""
    return OK

def main(argv):

    global folder_name, sqls

    default_options = 8
    for key1 in command_options.keys():
        assert len(command_options[key1].keys()) == default_options, \
f'''Command {key1} has {len(command_options[key1].keys())} options \
instead of default {default_options}.'''
        for key2 in command_options[key1].keys():
            if key2 != "help1" and key2 != "alternative":
                assert len(command_options[key1]["name"]) == len(command_options[key1][key2]), \
f'''Command option {key1} has {len(command_options[key1]["name"])} names \
but {len(command_options[key1][key2])} '{key2}'.'''
        for key2 in command_options.keys():
            if key1 != key2:
                for a1 in command_options[key1]["alternative"]:
                    for a2 in command_options[key2]["alternative"]:
                        assert a1 != a2, f"Command '{key1}' has the same alternative as command '{key2}': '{a1}'."

    namespace = parseArgv(argv)
    """
    for k,v in vars(namespace).items():
        print(k, v)
    """

    if len(vars(namespace)["sql_files"]) > 0:
        sqls = get_sql_queries_dict(vars(namespace)["sql_files"])
        #print(sqls)
        for full_filename in sqls.keys():
            #OK_returned = 1
            for i, sql in enumerate(sqls[full_filename]):
                printCom(f"\n\\\\ SQL file '{full_filename}' command no {str(i+1)} \\\\")
                #print(sql)
                #print()
                OK_returned = do_sql(sql)
                if OK_returned == 0: break


    if len(vars(namespace)["sql_files"]) == 0 and isinstance(vars(namespace)["interactive"], str) or vars(namespace)["interactive"]:
        print("\nEntering interactive mode. Type '\quit' to quit.")

        if conn:
            if db_version[:7] == "Sqlite3":
                print(f'''Using Sqlite3 filename "{db_filename}". Use \sqlite3 filename' for change.''')
            elif db_version[:5] == "MySQL":
                print(f'''Using MySQL database `{db_schema}`. Use '\mysql database' for change.''')
            elif db_version[:5] == "MsSQL":
                print(f'''Using MsSQL database "{db_schema}". Use '\mssql database' for change.''')
            elif db_version[:10] == "PostgreSQL":
                print(f'''Using PostgreSQL database "{db_schema}". Use '\mysql database' for change.''')
            else:
                printRed("Sorry, no db_version.")
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

            sql_filename = "interactive pass " + str(interactive_pass)
            sqls[sql_filename] = parseText(sql, ";")
            #OK_returned = 1
            for i, sql in enumerate(sqls[sql_filename]):
                printCom(f'''\n\\\\ SQL file '{sql_filename}' command no {str(i+1)} \\\\''')
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
