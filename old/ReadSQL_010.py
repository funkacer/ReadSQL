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
from datetime import timedelta
import random

from importlib.metadata import version

#from okno import zobraz

'''
#import time, sys
def loading():
    print ("Loading...")
    for i in range(0, 100):
        #time.sleep(.1)
        #sys.stdout.write(u"\u001b[1000D")
        #sys.stdout.write("\033[1000D")
        #sys.stdout.flush()
        #time.sleep(.1)
        #sys.stdout.write(str(i + 1) + "%")
        #sys.stdout.flush()
        time.sleep(0.1)
        width = (i + 1) / 4
        bar = "[" + "#" * int(width) + " " * int(25 - width) + "]"
        #sys.stdout.write(u"\u001b[1000D" +  bar)
        sys.stdout.write(u"\u001b[1000D" +  str(i + 1) + "%")
        sys.stdout.flush()
    print()

loading()


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


print (u"\u001b[30m A \u001b[31m B \u001b[32m C \u001b[33m D \u001b[0m")
print (u"\u001b[34m E \u001b[35m F \u001b[36m G \u001b[37m H \u001b[0m")
print (u"\u001b[30;1m A \u001b[31;1m B \u001b[32;1m C \u001b[33;1m D \u001b[0m")
print (u"\u001b[34;1m E \u001b[35;1m F \u001b[36;1m G \u001b[37;1m H \u001b[0m")

import sys
for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
    print (u"\u001b[0m")

print (u"\u001b[40m A \u001b[41m B \u001b[42m C \u001b[43m D \u001b[0m")
print (u"\u001b[44m A \u001b[45m B \u001b[46m C \u001b[47m D \u001b[0m")
print (u"\u001b[40;1m A \u001b[41;1m B \u001b[42;1m C \u001b[43;1m D \u001b[0m")
print (u"\u001b[44;1m A \u001b[45;1m B \u001b[46;1m C \u001b[47;1m D \u001b[0m")

import sys
for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        sys.stdout.write(u"\u001b[48;5;" + code + "m " + code.ljust(4))
    print (u"\u001b[0m")

print (u"\u001b[1m BOLD \u001b[0m\u001b[4m Underline \u001b[0m\u001b[7m Reversed \u001b[0m")
print (u"\u001b[1m\u001b[4m\u001b[7m BOLD Underline Reversed \u001b[0m")

aa = ["", "\033[1m", "\033[4m", "\033[1m\033[4m"]
for a in range(3):
    for i in range(0, 16):
        for j in range(0, 16):
            code1 = str(i * 16 + j)
            code2 = str(j * 16 + i)
            print(aa[a] + '\033[38;5;' + code1 + 'm' + '\033[48;5;' + code2 + 'm' + " Ahoj " + '\033[0m')
            #print('\033[48;5;' + code + 'm' + "Ahoj" + '\033[0m')

i = "1"
while i != "":
    a = 0
    i = input()
    code1 = int(i[:4])
    if code1 > 3000:
        code1 -= 3000
        a = 3
    if code1 > 2000:
        code1 -= 2000
        a = 2
    if code1 > 1000:
        code1 -= 1000
        a = 1
    if len(i) > 4:
        code2 = int(i[4:])
        print(aa[a] + '\033[38;5;' + str(code1) + 'm' + '\033[48;5;' + str(code2) + 'm' + " Ahoj " + '\033[0m')
    else:
        print(aa[a] + '\033[38;5;' + str(code1) + 'm' + " Ahoj " + '\033[0m')


colors = {}
cls = ['\033[1m', '\033[95m', '\033[91m', '\033[33m', '\033[92m', '\033[96m', '\033[4m', '\033[97m\033[42m', '\033[97m\033[101m']

for i in range(9):
    colors[i] = (cls[i], '\033[0m')

#printColor = lambda sTxt, color: print(colors[color][0] + sTxt + colors[color][1])

'''

#\033[34m too dark blue text
os.system('color')
RED, YELLOW, GREEN, BLUE, COM, INVGREEN, INVRED, END = '\033[91m', '\033[33m', '\033[92m', '\033[96m', '\033[4m', '\033[97m\033[42m', '\033[97m\033[101m', '\033[0m'
printRed = lambda sTxt: print(RED + sTxt + END)
printGreen = lambda sTxt: print(GREEN + sTxt + END)
printYellow = lambda sTxt: print(YELLOW + sTxt + END)
printBlue = lambda sTxt: print(BLUE + sTxt + END)
printCom = lambda sTxt: print(COM + sTxt + END)
printInvGreen = lambda sTxt: print(INVGREEN + sTxt + END)
printInvRed = lambda sTxt: print(INVRED + sTxt + END)
Assert = lambda bCond=False, sTxt='': printRed(sTxt) if not bCond else None

printColor = lambda sTxt, mColor: print(mColor + sTxt + END)

#printInvRed("KO")
printInvGreen("OK")

row_format_l = lambda columns: "".join([f"{{:>{columns[c]['w']}}}" for c in columns]) if isinstance(columns, dict) else "{:>15}" * (len(columns) + 1)

conn = None
sqls = {}
data = None
columns = None
data_old = None
columns_old = None
folder_exists = None
folder_name = None
db_version = "None: "
show_cases = 5
print_max_default = 10
profile_max_categorical = 100
profile_show_categorical = 5
rows_label = "(Row)"
command_history = []
default_columns_name = "Column_"
commands = {}
variables = {}


variables["$all"] = {}
variables["$all"]["shorts"] = ["$a","$al"]
variables["$all"]["print data"] = {}
variables["$all"]["print data"]["value"] = 0
variables["$all"]["print data"]["print"] = {}
variables["$all"]["print data"]["print data"] = {}
variables["$all"]["print data"]["print data easy"] = {}
#variables["$all"]["print data"]["print data easy"]["what"] = []
variables["$all"]["print data"]["data select easy"] = {}
variables["$all"]["print history"] = {}
variables["$all"]["print history"]["value"] = 0
variables["$all"]["print history"]["print history"] = {}
variables["$red"] = {}
variables["$red"]["shorts"] = ["$r"]
variables["$red"]["user"] = {}
variables["$red"]["user"]["value"] = 1
variables["$green"] = {}
variables["$green"]["shorts"] = ["$g"]
variables["$green"]["user"] = {}
variables["$green"]["user"]["value"] = 2
variables["$invgreen"] = {}
variables["$green"]["shorts"] = ["$invg","$ig"]
variables["$invgreen"]["user"] = {}
variables["$invgreen"]["user"]["value"] = 20255


#variables["$a"] = 0

command_options = {}
command_options["#"] = {}
command_options["#"]["name"] = []
command_options["#"]["required"] = []
command_options["#"]["type"] = []
command_options["#"]["default"] = []
command_options["#"]["help1"] = "Help for command 'folder'"
command_options["#"]["help2"] = []
command_options["#"]["alternative"] = ["q"]
command_options["#"]["altoption"] = []

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
command_options["folder"]["alternative"] = ["folder", "f"]
command_options["folder"]["altoption"] = [["f","fn"]]

command_options["set"] = {}
command_options["set"]["name"] = ["what", "variable"]
command_options["set"]["required"] = [True, False]
command_options["set"]["type"] = [["user", "u"], "str"]
command_options["set"]["default"] = [None, None]
command_options["set"]["help1"] = "Help for command 'set'"
command_options["set"]["help2"] = ["Blabla1", "Blabla2"]
command_options["set"]["alternative"] = ["s"]
command_options["set"]["altoption"] = [["w"], ["v"]]

command_options["connect sqlite3"] = {}
command_options["connect sqlite3"]["name"] = ["filename"]
command_options["connect sqlite3"]["required"] = [False]
command_options["connect sqlite3"]["type"] = ["str"]
command_options["connect sqlite3"]["default"] = [":memory:"]
command_options["connect sqlite3"]["help1"] = "Help for command 'connect'"
command_options["connect sqlite3"]["help2"] = ["Blabla1"]
command_options["connect sqlite3"]["alternative"] = ["connect sqlite3", "connect sqlite", "connect sql3", "connect sql", "connect s", "c sqlite3", "c sqlite", "c sql3", "c sql", "c s",  "csqlite3", "csqlite", "csql3", "csql", "cs"]
command_options["connect sqlite3"]["altoption"] = [["f"]]

command_options["connect mysql"] = {}
command_options["connect mysql"]["name"] = ["database", "user", "password", "host", "port"]
command_options["connect mysql"]["required"] = [False, False, False, False, False]
command_options["connect mysql"]["type"] = ["str", "str", "str", "str", "int"]
command_options["connect mysql"]["default"] = ["", "root", "admin", "localhost", 3306]
command_options["connect mysql"]["help1"] = "Help for command 'folder'"
command_options["connect mysql"]["help2"] = ["Bla1", "Bla2", "Bla3", "Bla4", "Bla5"]
command_options["connect mysql"]["alternative"] = ["c mysql", "c my", "cmysql", "cmy"]
command_options["connect mysql"]["altoption"] = [["d"],["u"],["p"],["h"],["po"]]

command_options["connect postgre"] = {}
command_options["connect postgre"]["name"] = ["database", "user", "password", "host", "port"]
command_options["connect postgre"]["required"] = [False, False, False, False, False]
command_options["connect postgre"]["type"] = ["str", "str", "str", "str", "int"]
command_options["connect postgre"]["default"] = ["", "postgres", "postgres1", "localhost", 5432]
command_options["connect postgre"]["help1"] = "Help for command 'folder'"
command_options["connect postgre"]["help2"] = ["Bla1", "Bla2", "Bla3", "Bla4", "Bla5"]
command_options["connect postgre"]["alternative"] = ["c postgre", "c pg", "c p", "cpostgre", "cpg", "cp"]
command_options["connect postgre"]["altoption"] = [["d"],["u"],["p"],["h"],["po"]]

command_options["connect mssql"] = {}
command_options["connect mssql"]["name"] = ["database", "user", "password", "host", "port"]
command_options["connect mssql"]["required"] = [False, False, False, False, False]
command_options["connect mssql"]["type"] = ["str", "str", "str", "str", "int"]
command_options["connect mssql"]["default"] = ["", "root", "admin", "localhost", 3306]
command_options["connect mssql"]["help1"] = "Help for command 'folder'"
command_options["connect mssql"]["help2"] = ["Bla1", "Bla2", "Bla3", "Bla4", "Bla5"]
command_options["connect mssql"]["alternative"] = ["c mssql", "c ms", "cmssql", "cms"]
command_options["connect mssql"]["altoption"] = [["d"],["u"],["p"],["h"],["po"]]

command_options["read"] = {}
command_options["read"]["name"] = ["filename", "delimiter", "text_qualifier", "read_columns", "strip_columns", "lines"]
command_options["read"]["required"] = [True, False, False, False, False, False]
command_options["read"]["type"] = ["str", "str", "str", "bool", "bool", "int"]
command_options["read"]["default"] = [None, "	", None, True, True, None]
command_options["read"]["help1"] = "Help for command 'folder'"
command_options["read"]["help2"] = ["Blabla1", "Blabla2", "Blabla3", "Blabla4", "Blabla5", "Blabla6"]
command_options["read"]["alternative"] = ["read", "r"]
command_options["read"]["altoption"] = [["f"],["d"],["t","tq"], ['r','rc'], ['s','sc'], ["l"]]

command_options["export"] = {}
command_options["export"]["name"] = ["filename", "delimiter", "none"]
command_options["export"]["required"] = [True, False, False]
command_options["export"]["type"] = ["str", "str", "str"]
command_options["export"]["default"] = [None, "	", ""]
command_options["export"]["help1"] = "Help for command 'folder'"
command_options["export"]["help2"] = ["Blabla1", "Blabla2", "Blabla3"]
command_options["export"]["alternative"] = ["e"]
command_options["export"]["altoption"] = [["f"],["d"],["null","n"]]

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
command_options["insert"]["alternative"] = ["insert", "i"]
command_options["insert"]["altoption"] = [["t"]]

# print data via command print
command_options["print"] = {}
command_options["print"]["name"] = ["from", "to", "step", "random", "list", "columns"]
command_options["print"]["required"] = [False, False, False, False, False, False]
command_options["print"]["type"] = ["int", "int", "int", "int", "intlist", "strlist"]
command_options["print"]["default"] = [0, 0, 1, 0, "[]", "[]"]
command_options["print"]["help1"] = "Help for command 'folder'"
command_options["print"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6"]
command_options["print"]["alternative"] = ["print", "p"]
command_options["print"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"]]

command_options["print data easy"] = {}
command_options["print data easy"]["name"] = ["from", "to", "step", "random", "list", "columns", "nones", "nones_option", "title", "note", "title_color", "note_color"]
command_options["print data easy"]["required"] = [False, False, False, False, False, False, False, False, False, False, False, False]
command_options["print data easy"]["type"] = ["int", "int", "int", "int", "intlist", "strlist", "strlist", ["any","all","none"], "str", "str", "int", "int"]
command_options["print data easy"]["default"] = [0, 0, 1, 0, "[]", "[]", "[]", "any", None, None, None, None]
command_options["print data easy"]["help1"] = "Help for command 'folder'"
command_options["print data easy"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11","Bla12"]
command_options["print data easy"]["alternative"] = ["print data", "pd",  "p"]
command_options["print data easy"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["nulls", "ns", "n"], ["no"], ["tt"], ["nt"], ["tc"], ["nc"]]

command_options["print data"] = {}
command_options["print data"]["name"] = ["what", "from", "to", "step", "random", "list", "columns", "title", "note", "title_color", "note_color"]
command_options["print data"]["required"] = [False, False, False, False, False, False, False, False, False, False, False]
command_options["print data"]["type"] = [["data","d"], "int", "int", "int", "int", "intlist", "strlist", "str", "str", "int", "int"]
command_options["print data"]["default"] = ["data", 0, 0, 1, 0, "[]", "[]", None, None, None, None]
command_options["print data"]["help1"] = "Help for command 'folder'"
command_options["print data"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11"]
command_options["print data"]["alternative"] = ["print", "p"]
command_options["print data"]["altoption"] = [["w"], ["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["tt"], ["nt"], ["tc"], ["nc"]]

command_options["print columns"] = {}
command_options["print columns"]["name"] = ["what"]
command_options["print columns"]["required"] = [True]
command_options["print columns"]["type"] = [["columns", "c"]]
command_options["print columns"]["default"] = ["columns"]
command_options["print columns"]["help1"] = "Help for command 'folder'"
command_options["print columns"]["help2"] = ["Bla1"]
command_options["print columns"]["alternative"] = ["print", "p"]
command_options["print columns"]["altoption"] = [["w"]]

command_options["print history"] = {}
command_options["print history"]["name"] = []
command_options["print history"]["required"] = []
command_options["print history"]["type"] = []
command_options["print history"]["default"] = []
command_options["print history"]["help1"] = "Help for command 'folder'"
command_options["print history"]["help2"] = []
command_options["print history"]["alternative"] = ["print h", "p h", "ph"]
command_options["print history"]["altoption"] = []

'''
command_options["print"] = {}
command_options["print"]["name"] = ["what", "from", "to", "step", "random", "list", "columns", "title", "note", "title_color", "note_color"]
command_options["print"]["required"] = [False, False, False, False, False, False, False, False, False, False, False]
command_options["print"]["type"] = [["data","columns","history","d","c","h"], "int", "int", "int", "int", "intlist", "strlist", "str", "str", "int", "int"]
command_options["print"]["default"] = ["data", 0, 0, 1, 0, "[]", "[]", None, None, None, None]
command_options["print"]["help1"] = "Help for command 'folder'"
command_options["print"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11"]
command_options["print"]["alternative"] = ["p"]
command_options["print"]["altoption"] = [["w"], ["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["tt"], ["nt"], ["tc"], ["nc"]]
'''

command_options["break"] = {}
command_options["break"]["name"] = ["what", "from", "to", "step", "list", "columns"]
command_options["break"]["required"] = [False, False, False, False, False, False]
command_options["break"]["type"] = [["data","columns"], "int", "int", "int", "intlist", "strlist"]
command_options["break"]["default"] = ["data", 0, print_max_default, 1, None, None]
command_options["break"]["help1"] = "Help for command 'folder'"
command_options["break"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6"]
command_options["break"]["alternative"] = ["b"]
command_options["break"]["altoption"] = [["w"],["f"], ["t"], ["s"], ["l"], ["c"]]

command_options["data fill easy"] = {}
command_options["data fill easy"]["name"] = ["formats", "nones", "title", "note", "title_color", "note_color"]
command_options["data fill easy"]["required"] = [False, False, False, False, False, False]
command_options["data fill easy"]["type"] = ["dictlist", "dictlist", "str", "str", "int", "int"]
command_options["data fill easy"]["default"] = [None, None, None, None, None, None]
command_options["data fill easy"]["help1"] = "Help for command 'data fill easy'"
command_options["data fill easy"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6"]
command_options["data fill easy"]["alternative"] = ["data fill", "data f", "d f ", "df"]
command_options["data fill easy"]["altoption"] = [["fs", "f"], ["nulls", "ns", "n"], ["tt"], ["nt"], ["tc"], ["nc"]]

command_options["data select easy"] = {}
command_options["data select easy"]["name"] = ["from", "to", "step", "random", "list", "columns", "nones", "nones_option", "title", "note", "title_color", "note_color"]
command_options["data select easy"]["required"] = [False, False, False, False, False, False, False, False, False, False, False, False]
command_options["data select easy"]["type"] = ["int", "int", "int", "int", "intlist", "strlist", "strlist", ["any","all","none"],"str", "str", "int", "int"]
command_options["data select easy"]["default"] = [0, 0, 1, 0, "[]", "[]", "[]", "any", None, None, None, None]
command_options["data select easy"]["help1"] = "Help for command 'data select easy'"
command_options["data select easy"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10", "Bla10", "Bla11"]
command_options["data select easy"]["alternative"] = ["data select", "data s", "d s", "ds"]
command_options["data select easy"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["nulls", "ns", "n"], ["no"], ["tt"], ["nt"], ["tc"], ["nc"]]

command_options["data select"] = {}
command_options["data select"]["name"] = ["what", "from", "to", "step", "random", "list", "columns", "title", "note", "title_color", "note_color"]
command_options["data select"]["required"] = [True, False, False, False, False, False, False, False, False, False, False]
command_options["data select"]["type"] = [["select","se","s"], "int", "int", "int", "int", "intlist", "strlist", "str", "str", "int", "int"]
command_options["data select"]["default"] = ["select", 0, 0, 1, 0, "[]", "[]", None, None, None, None]
command_options["data select"]["help1"] = "Help for command 'folder'"
command_options["data select"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11"]
command_options["data select"]["alternative"] = ["data", "d"]
command_options["data select"]["altoption"] = [["w"], ["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["tt"], ["nt"], ["tc"], ["nc"]]

command_options["data profile easy"] = {}
command_options["data profile easy"]["name"] = ["from", "to", "step", "random", "list", "columns", "title", "note", "title_color", "note_color"]
command_options["data profile easy"]["required"] = [False, False, False, False, False, False, False, False, False, False]
command_options["data profile easy"]["type"] = ["int", "int", "int", "int", "intlist", "strlist", "str", "str", "int", "int"]
command_options["data profile easy"]["default"] = [0, 0, 1, 0, "[]", "[]", None, None, None, None]
command_options["data profile easy"]["help1"] = "Help for command 'folder'"
command_options["data profile easy"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10"]
command_options["data profile easy"]["alternative"] = ["data profile", "d profile", "d pr", "d p", "dpr", "dp"]
command_options["data profile easy"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["tt"], ["nt"], ["tc"], ["nc"]]

command_options["data profile"] = {}
command_options["data profile"]["name"] = ["what", "from", "to", "step", "random", "list", "columns", "title", "note", "title_color", "note_color"]
command_options["data profile"]["required"] = [False, False, False, False, False, False, False, False, False, False, False]
command_options["data profile"]["type"] = [["profile","pr","p"], "int", "int", "int", "int", "intlist", "strlist", "str", "str", "int", "int"]
command_options["data profile"]["default"] = ["profile", 0, 0, 1, 0, "[]", "[]", None, None, None, None]
command_options["data profile"]["help1"] = "Help for command 'folder'"
command_options["data profile"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11"]
command_options["data profile"]["alternative"] = ["data", "d"]
command_options["data profile"]["altoption"] = [["w"], ["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["tt"], ["nt"], ["tc"], ["nc"]]

command_options["data reset"] = {}
command_options["data reset"]["name"] = ["what"]
command_options["data reset"]["required"] = [True]
command_options["data reset"]["type"] = [["reset","rs","r"]]
command_options["data reset"]["default"] = ["reset"]
command_options["data reset"]["help1"] = "Help for command 'folder'"
command_options["data reset"]["help2"] = ["Bla1"]
command_options["data reset"]["alternative"] = ["data", "d"]
command_options["data reset"]["altoption"] = [["w"]]


def colorCode(color):
    cc = ""
    cc0 = ["", "\033[1m", "\033[4m", "\033[1m\033[4m"]
    colorcode0 = 0
    colorcode1 = 0
    colorcode2 = 0
    if color >= 10000:
        colorcode2 = int(color/10000)
        colorcode1 = color - colorcode2*10000
    else:
        colorcode1 = color
    if colorcode1 >= 3000:
        colorcode1 = colorcode1-int(colorcode1/1000)*1000
        colorcode0 = 3
    elif colorcode1 >= 2000:
        colorcode1 -= 2000
        colorcode0 = 2
    elif colorcode1 >= 1000:
        colorcode1 -= 1000
        colorcode0 = 1
    #print(colorcode0, colorcode1, colorcode2)
    if color >= 10000:
        cc = cc0[colorcode0] + '\033[38;5;' + str(colorcode1) + 'm' + '\033[48;5;' + str(colorcode2) + 'm'
    else:
        cc = cc0[colorcode0] + '\033[38;5;' + str(colorcode1) + 'm'
    return cc


def terminal_resize(colsp):
    columns, rows = os.get_terminal_size()
    #print(columns, rows)
    width = 0
    screen = 1
    first = 0
    for col in colsp:
        if first == 0: first = colsp[col]['w']
        width += colsp[col]['w']
        if width > columns:
            screen += 1
            width = first + colsp[col]['w']
        colsp[col]['screen'] = screen
        #print(col, screen)


def data_profile(rowsi, colsi, data, columns, rows, rows_label, progress_indicator = False):
    #print("Len rowsi", len(rowsi))
    nrows = len(data)
    ncols = len(columns)
    colsp = {}
    colsp[0] = {}
    colsp[0]['name'] = rows_label
    colsp[0]['w'] = len(str(rows_label))  # Columns 0 is Row number with header '(Row)' = 5 chars
    colsp[0]['t'] = "Quantitative"
    colsp[0]['fnq'] = None
    colsp[0]['n'] = 0
    colsp[0]['v'] = 0
    colsp[0]['c'] = {}
    colsp[0]['sum'] = 0
    colsp[0]['min'] = 0
    colsp[0]['max'] = 0
    colsp[0]['mean'] = 0
    for ci in colsi:
        colsp[ci] = {}
        colsp[ci]['name'] = columns[ci-1]
        colsp[ci]['w'] = len(columns[ci-1]) + 1
        #colsp[columns[ci-1]]['t'] = "Categorical"
        colsp[ci]['t'] = "Quantitative"
        colsp[ci]['fnq'] = None
        colsp[ci]['n'] = 0
        colsp[ci]['v'] = 0
        colsp[ci]['c'] = {}
        colsp[ci]['sum'] = 0
        colsp[ci]['m'] = []
        colsp[ci]['q1'] = None
        colsp[ci]['q2'] = None
        colsp[ci]['q3'] = None
        colsp[ci]['smd2'] = 0
        colsp[ci]['smd3'] = 0
    for ri in rowsi:
        if len(str(rows[ri-1])) > colsp[0]['w']: colsp[0]['w'] = len(str(rows[ri-1]))
        for ci in colsi:
            w = len(str(data[ri-1][ci-1])) + 1
            if w > colsp[ci]['w']: colsp[ci]['w'] = w
            if data[ri-1][ci-1] is not None:
                colsp[ci]['v'] += 1
                if colsp[ci]['t'] == "Quantitative":
                    try:
                        a = float(data[ri-1][ci-1])
                        if colsp[ci]['v'] == 1:
                            colsp[ci]['min'] = data[ri-1][ci-1]
                            colsp[ci]['max'] = data[ri-1][ci-1]
                        elif data[ri-1][ci-1] < colsp[ci]['min']:
                            colsp[ci]['min'] = data[ri-1][ci-1]
                        elif data[ri-1][ci-1] > colsp[ci]['max']:
                            colsp[ci]['max'] = data[ri-1][ci-1]
                        colsp[ci]['sum'] += data[ri-1][ci-1]
                        colsp[ci]['m'].append(data[ri-1][ci-1])
                    except:
                        colsp[ci]['t'] = "Categorical"
                        if colsp[ci]['fnq'] is None:
                            colsp[ci]['fnq'] = data[ri-1][ci-1]
                if data[ri-1][ci-1] not in colsp[ci]['c']:
                    colsp[ci]['c'][data[ri-1][ci-1]] = 1
                else:
                    colsp[ci]['c'][data[ri-1][ci-1]] += 1
            else:
                #count None
                colsp[ci]['n'] += 1
        if progress_indicator:
            proc = int(ri/len(rowsi)*90)
            sys.stdout.write(u"\u001b[1000D" +  "Processed: " + str(proc) + "% ")
            sys.stdout.flush()

    for ci in colsi:
        if colsp[ci]['v'] > 0 and colsp[ci]['t'] == "Quantitative":
            colsp[ci]['mean'] = colsp[ci]['sum'] / colsp[ci]['v']
            lenc = len(colsp[ci]['m'])
            if lenc > 0:
                #print(ci, sorted(colsp[ci]['m']))
                colsp[ci]['m'] = sorted(colsp[ci]['m'])
                if lenc >= 1 and lenc % 2:
                    colsp[ci]['q2'] = colsp[ci]['m'][int((lenc+1)/2)-1]
                if lenc >= 2 and (lenc % 2) == 0:
                    colsp[ci]['q2'] = (colsp[ci]['m'][int(lenc/2)-1] + colsp[ci]['m'][int(lenc/2)])/2    #mean of mid cases
            lenc = int(len(colsp[ci]['m'])/2)
            if lenc > 0:
                #print(ci, sorted(colsp[ci]['m']))
                #colsp[ci]['m'] = sorted(colsp[ci]['m'])
                if lenc >= 1 and lenc % 2:
                    colsp[ci]['q1'] = colsp[ci]['m'][int((lenc+1)/2)-1]
                if lenc >= 2 and (lenc % 2) == 0:
                    colsp[ci]['q1'] = (colsp[ci]['m'][int(lenc/2)-1] + colsp[ci]['m'][int(lenc/2)])/2    #mean of mid cases
                if lenc >= 1 and lenc % 2:
                    colsp[ci]['q3'] = colsp[ci]['m'][-1*int((lenc+1)/2)]
                if lenc >= 2 and (lenc % 2) == 0:
                    colsp[ci]['q3'] = (colsp[ci]['m'][-1*int(lenc/2)] + colsp[ci]['m'][-1*(int(lenc/2))-1])/2    #mean of mid cases
            for i in colsp[ci]['m']:
                colsp[ci]['smd2'] += (i - colsp[ci]['mean'])**2
                colsp[ci]['smd3'] += (i - colsp[ci]['mean'])**3
        else:
            colsp[ci]['min'] = None
            colsp[ci]['max'] = None
            colsp[ci]['sum'] = None
            colsp[ci]['mean'] = None
            colsp[ci]['q1'] = None
            colsp[ci]['q2'] = None
            colsp[ci]['q3'] = None
        if len(colsp[ci]['c']) > 0:
            colsp[ci]['c'] = {k:v for k, v in sorted(colsp[ci]['c'].items(), reverse = True, key = lambda x: x[1])[:profile_max_categorical]}
        if progress_indicator:
            proc = int(90+ci/len(colsi)*10)
            sys.stdout.write(u"\u001b[1000D" +  "Processed: " + str(proc) + "% ")
            sys.stdout.flush()

    if progress_indicator:
        print("\nQuantitative:", [colsp[ci]['name'] for ci in colsi if colsp[ci]['t'] == "Quantitative"])
        variables["$columns_quantitative"] = {}
        variables["$columns_quantitative"]["shorts"] = ["$columns_quant","$cq"]
        variables["$columns_quantitative"]["print data"] = {}
        variables["$columns_quantitative"]["print data"]["value"] = [colsp[ci]['name'] for ci in colsi if colsp[ci]['t'] == "Quantitative"]
        variables["$columns_quantitative"]["print data"]["print"] = {}
        variables["$columns_quantitative"]["print data"]["print data"] = {}
        variables["$columns_quantitative"]["print data"]["print data easy"] = {}

    #print(colsp)
    return colsp


def print_data(rowsi, colsi, data, columns, rows, rows_label):
    #print(rows_show)
    colsp = data_profile(rowsi, colsi, data, columns, rows, rows_label)
    terminal_resize(colsp)
    #print(row_format)
    #row_format = row_format_l(colsp)
    #print(row_format)
    #print(row_format.format(*[colsp[ci]['name'] for ci in colsp]))
    for ci in colsp:
        screen_max = colsp[ci]['screen']
    screen = 0
    while screen < screen_max:
        #print(row_format)
        colspart = {}
        if screen > 0:
            colspart[0] = colsp[0]
            print("...")
        for ci in colsp:
            if colsp[ci]['screen'] == screen + 1:
                colspart[ci] = colsp[ci]
        row_format = row_format_l(colspart)
        print(row_format.format(*[colsp[ci]['name'] for ci in colspart]))
        for ri in rowsi:
            #print(row_format.format(profile_rows[i], *[str(col) for col in row if col in colspart]))    # Null to None
            print(row_format.format(str(rows[ri-1]), *[str(col) for ci, col in enumerate(data[ri-1]) if ci+1 in colspart]))    # Null to None
        screen += 1


def show_data(data, columns, show_title = True):
    global variables
    nrows = len(data)
    variables["$all"]["print data"]["value"] = nrows
    ncols = len(columns)
    rows = range(1, nrows + 1)
    colsi = range(1, ncols + 1)
    if nrows <= show_cases*2:
        if show_title: printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing all cases with all columns.")
        rowsi = range(1, nrows + 1)
        print_data(rowsi, colsi, data, columns, rows, rows_label)
    else:
        if show_title: printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing first / last {show_cases} cases with all columns.")
        data_show = list(data[:show_cases])
        #print("Data show",data_show)
        data_show += [["" for c in columns]]
        data_show += data[-show_cases:]
        #print("Data show",data_show)
        rows = list(range(1,show_cases+1))
        rows += ["..."]
        rows += list(range(nrows-show_cases+1, nrows +1))
        #print("Rows:", rows)
        rowsi = range(1, len(data_show) + 1)
        print_data(rowsi, colsi, data_show, columns, rows, rows_label)


def find_columns(colss):
    colsi = []
    for cols in colss:
        is_column = 0
        for i, col in enumerate(columns):
            if col == cols:
                colsi.append(i + 1)
                is_column += 1
        if is_column < 1:
            printRed(f"Column '{cols}' not in columns!")
            print()
        elif is_column > 1:
            printRed(f"Multiple columns '{cols}' are in columns!")
            print()
    return colsi


def data_fill(fill_formats = {}, fill_nones = {}):
    global data

    temp_columns = set()
    if fill_formats is not None:
        for colss in fill_formats:
            temp_columns.add(colss)
    if fill_nones is not None:
        for colss in fill_nones:
            temp_columns.add(colss)

    fill_columns = {}
    for colss in temp_columns:
        fill_columns[colss] = {}
        if fill_formats is not None:
            if colss in fill_formats: fill_columns[colss]["fill_format"] = fill_formats[colss]
        if fill_nones is not None:
            if colss in fill_nones: fill_columns[colss]["fill_none"] = fill_nones[colss]

    print("fill_columns", fill_columns)

    if len(fill_columns) > 0:
        for colss in fill_columns:
            colsi = find_columns([colss])
            fill_format = fill_columns[colss].get("fill_format")
            fill_none = fill_columns[colss].get("fill_none")
            if len(colsi) > 0:
                #print(colss, colsi)
                for ri in range(1, len(data) + 1):
                    for ci in colsi:
                        # do format of columns ci - 1, fill_columns(colss)
                        #print(colss, columns[ci-1], fill_columns[colss])
                        if fill_format == "int" or fill_format == "int." \
                        or fill_format == "int," \
                        or fill_format == "float" or fill_format == "float." \
                        or fill_format == "float,":
                            rsign = 1
                            rstring = ""
                            dstring = ""
                            if fill_format == "int.": dstring = "."
                            if fill_format == "int,": dstring = ","
                            if fill_format == "float" or fill_format == "float.": dstring = "."
                            if fill_format == "float,": dstring = ","
                            value = str(data[ri-1][ci-1])
                            for vi in range(len(value)):
                                v = value[vi]
                                if v in ["-","0","1","2","3","4","5","6","7","8","9",dstring]:
                                    if v == "-" and vi < len(value) and vi > 0:
                                        if value[vi+1] in ["0","1","2","3","4","5","6","7","8","9",dstring] and value[vi-1] not in ["0","1","2","3","4","5","6","7","8","9"]:
                                            rsign = -1
                                    elif v == "-" and vi < len(value)-1:
                                        if value[vi+1] in ["0","1","2","3","4","5","6","7","8","9"]:
                                            rsign = -1
                                    elif v == dstring and vi < len(value)-1:
                                        if value[vi+1] in ["0","1","2","3","4","5","6","7","8","9"]:
                                            rstring += "."
                                    else:
                                        rstring += v
                            try:
                                #print(rstring)
                                if fill_format[:1] == "i":
                                    value = int(float(rstring))*rsign
                                elif fill_format[:1] == "f":
                                    value = float(rstring)*rsign
                                data[ri-1][ci-1] = value
                            except:
                                #print("Error")
                                data[ri-1][ci-1] = None
                        if fill_none is not None:
                            #print(data[ri-1][ci-1])
                            if data[ri-1][ci-1] is None: data[ri-1][ci-1] = fill_none


def data_select():
    global fromm, too, stepp, randd, listt, colss, listi
    nrows = len(data)
    ncols = len(columns)
    colsi = range(1, ncols + 1)
    if len(colss) > 0:
        colsi = find_columns(colss)
    nonesi = []
    if len(noness) > 0:
        nonesi = find_columns(noness)
    #columns_show = [columns[i] for i in colsi] # only existing
    rowsi = []
    listi = []
    if len(listt) > 0:
        if nrows > 0:
            #assert list in range of cases
            for l in listt:
                if l < 0: l += nrows + 1
                if l <= 0: l = 1    # if l was lower than -nrows
                if l > nrows: l = nrows
                if l not in listi: listi.append(l)
        else:
            listi = []
        #print("Listi", listi)
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
    if len(nonesi) > 0:
        rowni = set()
        rowai = set()
        for ri in range(1, len(data) + 1):
            for ci in nonesi:
                if data[ri-1][ci-1] is None:
                    rowni.add(ri)
                else:
                    rowai.add(ri)
        # logika any, all, none
        #print("rowni", rowni)
        #print("rowai", rowai)
        rowsi = []
        if noneso == "all" or noneso == "any":
            for ri in rowni:
                if noneso == "all" and ri not in rowai:
                    rowsi.append(ri)
                elif noneso == "any":
                    rowsi.append(ri)
        elif noneso == "none":
            for ri in range(1, len(data) + 1):
                if ri not in rowni:
                    rowsi.append(ri)
        else:
            printInvRed("Error, none_option not recognized")
    elif randd > 0:
        if too == 0: too = nrows
        if len(listi) > 0:
            # select from listt
            # cannot select 2 same cases in list when 0,1 or >nrows => make set
            #listi = list(set(listi))
            if randd > len(listi): randd = len(listi)
            #print("Randd", randd)
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



def parseText(myText, delimiter, text_qualifiers = ['"', "'", "["], do_strip = True):

    #print("Uvozovky", myText.count('"'), myText.count("'"))

    lst_new = []
    apos = None
    maxs = -1
    for i, chr in enumerate(myText):
        if not apos and (chr == delimiter):
            if do_strip:
                app_text = myText[maxs+1:i].strip()
                if app_text != "": lst_new.append(app_text)
            else:
                app_text = myText[maxs+1:i]
                lst_new.append(app_text)
            maxs = i
        #elif not apos and (chr == '"' or chr == "'" or chr == "["):
        elif not apos and chr in text_qualifiers:
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

    if do_strip:
        app_text = myText[maxs+1:].strip()
        if app_text != "": lst_new.append(app_text)
    else:
        if maxs < len(myText): lst_new.append(myText[maxs+1:])

    #print("lst_new:", lst_new)

    return lst_new


def parseCommand(command_line):
    commands = []
    command = ""
    #options = {}
    #error = 0
    execute = False
    #command_line = command_line.replace(" ", "")
    command_line = command_line[1:].strip() #no slash
    #print (command_line)
    for c in command_options:
        #print(c)
        '''
        if command_line[:len(c)].lower() == c:
            commands.append((c,c))
            #command_line = command_line[len(c):]
            #command_line = "=".join(parseText(command_line, "="))
            #command_line = ",".join(parseText(command_line, " "))
            #print(command_line)
            #command_line_list = parseText(command_line, ",")
            #print(f"Parse command {command} with ',':", command_line_list)
        else:
        '''
        for a in command_options[c]["alternative"]:
            if command_line[:len(a)].lower() == a:
                commands.append((c,a))
                #command_line = command_line[len(a):]
                #command_line = "=".join(parseText(command_line, "="))
                #command_line = ",".join(parseText(command_line, " "))
                #print(command_line)
                #command_line_list = parseText(command_line, ",")
            #if command != "": break
            #print(a)
        #if command != "": break
        #print(c)

    command_line_original = command_line

    for c in commands:
        print(c[0], c[1])
        command = c[0]
        command_line = command_line_original[len(c[1]):]
        command_line = "=".join(parseText(command_line, "="))
        command_line = ",".join(parseText(command_line, " "))
        print("Command line:", command_line)
        command_line_list = parseText(command_line, ",")
        print("Command line list:", command_line_list)

        execute = True
        options = {}

        # this should give key=option together
        #print(f"Parse command {command} with ',':", command_line_list)
        cll_final = []
        i = 0
        while i < len(command_line_list):
            if i < len(command_line_list)-2:
                if command_line_list[i+1] == "=":
                    cll_final.append("".join([command_line_list[i],"=",command_line_list[i+2]]))
                    i += 3
                else:
                    cll_final.append(command_line_list[i])
                    i += 1
            else:
                cll_final.append(command_line_list[i])
                i += 1
        #print(cll_final)

        #print(command)
        for i, cl in enumerate(cll_final):
            #cl = cl.strip()
            #if "=" in cl:
                #cll = cl.split("=")
            cll = parseText(cl, "=", do_strip = False)
            #print("cll:", cll)
            if len(cll) > 1:
                does_exist = 0
                for j, o in enumerate(command_options[command]["name"]):
                    if cll[0].strip().lower() == o:
                        options[o] = cll[1]
                        does_exist = 1
                    else:
                        for a in command_options[command]["altoption"][j]:
                            if cll[0].strip().lower() == a:
                                options[o] = cll[1]
                                does_exist = 1
                            if does_exist: break
                            #print(a)
                if not does_exist:
                    printRed(f'''Unknown option '{cll[0]}'. I will not use your '{cll[1]}' value in any way.''')
                    execute = False
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
                    if len(options[n]) > 0:
                        if options[n][0] == '"' and options[n][-1] == '"':
                            options[n] = options[n].strip('"')
                        elif options[n][0] == "'" and options[n][-1] == "'":
                            options[n] = options[n].strip("'")
                    bCond = options[n] in t
                    #print(options[n], t, bCond)
                    sTxt = f"Value '{options[n]}' is not valid for option '{n}'. Use one of these options: {t}."
                    Assert(bCond, sTxt)
                    if not bCond:
                        execute = False
                        break
                elif t == "str":
                    #options[n] = options[n].strip('"')
                    #print("options[n]", options[n])
                    if len(options[n]) > 0:
                        if options[n][0] == '"' and options[n][-1] == '"':
                            options[n] = options[n].strip('"')
                        elif options[n][0] == "'" and options[n][-1] == "'":
                            options[n] = options[n].strip("'")
                    #print(f"Parse option '{n}' as string:", options[n])
                    #command = "quit"
                elif t == "int":
                    #print(f"I am going to translate '{options[n]}' to 'int'")
                    # check variables first
                    result_message = f"Option '{n}' should be integer but is '{options[n]}'. Probably not doing what expected!"
                    vartest = str(options[n])
                    if vartest[0] not in ["0","1","2","3","5","6","7","8","9","-","+"," "]:
                        if vartest[0] != "$": vartest = "$" + vartest #variable start with "$", user can omit like in print data all
                        variable = None
                        contexts = []
                        if vartest in variables:
                            variable = vartest
                        else:
                            for var in variables:
                                if variables[var].get("shorts"):
                                    if vartest in variables[var]["shorts"]:
                                        variable = var
                                        break
                        if variable:
                            #get context
                            print(f"Getting context for variable '{variable}' in command '{command}' and option '{options[n]}':")
                            for contexttest in variables[variable]:
                                #print(variables[variable][contexttest])
                                if command in variables[variable][contexttest] or contexttest == "user":
                                    contexts.append(contexttest)
                            for context in contexts:
                                print(f"Command '{command}' test passed with context '{context}'!")
                                print(variables[variable][contexttest])
                                print(options)
                                opt = 1
                                if context != "user":
                                    for optiontest in variables[variable][context][command]:
                                        if optiontest in options:
                                            if options[optiontest] in variables[variable][context][command][optiontest]:
                                                print(f"Option '{optiontest}' test passed with value '{options[optiontest]}'!")
                                            else:
                                                opt = 0
                                        else:
                                            opt = 0
                                else:
                                    opt = 1
                                if opt: options[n] = variables[variable][context]["value"]
                        else:
                            result_message = 1
                            result_message = f"Option '{n}' should be integer but is '{options[n]}', which is not a variable. Probably not doing what expected!"

                    try:
                        options[n] = int(options[n])
                    except Exception as e:
                        traceback.print_exc()
                    Assert(isinstance(options[n], int), result_message)
                    if not isinstance(options[n], int):
                        #options[n] = d
                        execute = False
                    #print(f"Parse option '{n}' as integer:", options[n])
                elif t == "intlist":
                    Assert(options[n][0] == "[" and options[n][-1] == "]", "Lists must be enclosed with []. Probably not doing what expected!")
                    options_list_line = options[n][1:-1]
                    options_list_line = ",".join(parseText(options_list_line, " "))
                    lst_old = parseText(options_list_line, ",")
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
                    Assert(options[n][0] == "[" and options[n][-1] == "]", "Lists must be enclosed with []. Probably not doing what expected!")
                    options_list_line = options[n][1:-1]
                    options_list_line = ",".join(parseText(options_list_line, " "))
                    lst_old = parseText(options_list_line, ",")
                    lst_new = []
                    #print("lst_old", lst_old)
                    for l_old in lst_old:
                        if l_old[0] == '"' and l_old[-1] == '"':
                            lst_new.append(l_old.strip('"'))
                        elif l_old[0] == "'" and l_old[-1] == "'":
                            lst_new.append(l_old.strip("'"))
                        else:
                            lst_new.append(l_old)
                    options[n] = lst_new
                elif t == "bool":
                    if options[n] == True or options[n] == "True" or options[n] == "1": options[n] = True
                    if options[n] == False or options[n] == "False" or options[n] == "0": options[n] = False
                elif t == "dictlist":
                    Assert(options[n][0] == "[" and options[n][-1] == "]", "Lists must be enclosed with []. Probably not doing what expected!")
                    options_list_line = options[n][1:-1]
                    options_list_line = ":".join(parseText(options_list_line, ":"))
                    options_list_line = ",".join(parseText(options_list_line, " "))
                    lst_old = parseText(options_list_line, ",")
                    lst_new = {}
                    #print("lst_old", lst_old)
                    for l_old in lst_old:
                        lst = parseText(l_old, ":", do_strip = False)
                        #print("lst:", lst)
                        if len(lst) > 1:
                            lst[0] = lst[0].strip()
                            lst[1] = lst[1].strip()
                            if lst[0][0] == '"' and lst[0][-1] == '"':
                                l = lst[0].strip('"')
                            elif lst[0][0] == "'" and lst[0][-1] == "'":
                                l = lst[0].strip("'")
                            else:
                                l = lst[0]
                            if len(lst[1]) == 0:
                                r = ""
                            elif lst[1][0] == '"' and lst[1][-1] == '"':
                                r = lst[1].strip('"')
                            elif lst[1][0] == "'" and lst[1][-1] == "'":
                                r = lst[1].strip("'")
                            else:
                                r = lst[1]
                            lst_new[l] = r
                        else:
                            printRed(f"Error parsing dictlist option {lst}. Check results carefully!!!")
                    options[n] = lst_new

        print("Command:", command)
        print("Options:", options)
        print("Execute:", execute)

        if execute: break

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
        printYellow(f'''Command '{command}' with options [{', '.join([str(str(op) + "=" + str(printoptions[op])) for op in printoptions])}].''')
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


def do_sql(sql):

    global conn, data, columns, data_old, columns_old, db_filename, folder_exists, folder_name, db_version, db_schema, \
            fromm, too, stepp, randd, listt, colss, noness, noneso, variables, command_history

    #time.sleep(0.1)

    OK = 1
    if sql.startswith("\\"):
        command, options = parseCommand(sql)
        if command == "quit" or command == "q":
            OK = 0

        elif command == "connect sqlite3":
            # , isolation_level=None == autocommit
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
                    #conn = sqlite3.connect(full_filename, isolation_level=None)
                    conn = sqlite3.connect(full_filename)
                    db_version = f"Sqlite3 ({full_filename}): "
                except Exception as e:
                    traceback.print_exc()

        elif command == "connect mysql":
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
                    #conn.autocommit(True)
                    #conn = mysql.connector.connect(host = "localhost", user = "root", password="admin", use_unicode=True,charset="utf8")
                    db_version = f"MySQL (Add schema!): "
                except Exception as e:
                    traceback.print_exc()

            except Exception as e:
                print("No MySQL support. Please run 'pip install mysqlclient'.\n")
                traceback.print_exc()

        elif command == "connect postgre":
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
                    #conn.set_session(autocommit=True)
                    #conn = mysql.connector.connect(host = "localhost", user = "root", password="admin", use_unicode=True,charset="utf8")
                    db_version = f"PostgreSQL (Add schema!): "
                except Exception as e:
                    traceback.print_exc()
            except Exception as e:
                print("No MySQL support. Please run 'pip install mysqlclient'.\n")
                traceback.print_exc()

        elif command == "connect mssql":
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
                    #conn.autocommit = True
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
                printInvGreen(f'''Using folder '{full_foldername}'.''')
                folder_name = full_foldername
            else:
                if folder_exists_old:
                    printInvRed(f'''Folder '{folder_name}' does not exist. Using current folder '{folder_name_old}'.''')
                    folder_exists = folder_exists_old
                    folder_name = folder_name_old
                else:
                    # folder_name_old is None if sql imported file has wrong \folder command
                    printInvRed("Folder '{}' does not exist. Using working directory '{}'.".format(folder_name, os.getcwd()))
                    folder_name = os.getcwd()
                OK = 2

        elif command == "read":
            read_filename = options["filename"]
            read_delimiter = options["delimiter"]
            if options.get("lines"):
                read_lines = options["lines"]
            else:
                read_lines = 0
            if options.get("text_qualifier"):
                read_text_qualifier = options["text_qualifier"]
            else:
                read_text_qualifier = None
            read_columns = options.get("read_columns")
            strip_columns = options.get("strip_columns")
            file_exists, full_filename = check_filename(read_filename)
            #print("Read: '{}'".format(read_filename))
            try:
                with open(full_filename, "r", encoding = "utf-8") as f:
                    data_new = []
                    columns_new = []
                    is_error = False
                    error = 0
                    data_line = f.readline()
                    # line with column names
                    if data_line:
                        if read_columns:
                            if data_line[-1] == "\n": data_line = data_line[:-1]
                            if read_text_qualifier:
                                if strip_columns:
                                    parsed_line = parseText(data_line, read_delimiter, [read_text_qualifier], True)
                                else:
                                    parsed_line = parseText(data_line, read_delimiter, [read_text_qualifier], False)
                                for c in parsed_line:
                                    columns_new.append(c)
                            else:
                                parsed_line = data_line.split(read_delimiter)
                                for c in parsed_line:
                                    if strip_columns:
                                        columns_new.append(c.strip())
                                    else:
                                        columns_new.append(c)
                            data_line = f.readline()
                        else:
                            # just determine number of columns from the first row
                            # column names are created at the end (in case more columns occure)
                            if data_line[-1] == "\n": data_line = data_line[:-1]
                            if read_text_qualifier:
                                parsed_line = parseText(data_line, read_delimiter, [read_text_qualifier], False)
                            else:
                                parsed_line = data_line.split(read_delimiter)
                            cc = 0
                            rest = len(parsed_line)
                            while rest > 0:
                                rest = int(rest/(10**cc))
                                #print(rest)
                                cc += 1
                            for i in range(len(parsed_line)):
                                c = default_columns_name + f"{(i+1):0{(cc-1)}}"
                                columns_new.append(c)
                        row = 1
                        len_columns = len(columns_new)
                        max_columns = len(columns_new)
                        #print("."+data_line+".")
                        while data_line:
                            sys.stdout.write(u"\u001b[1000D" +  "Lines read: " + str(row) + " ")
                            sys.stdout.flush()
                            #print("."+data_line+".")
                            row_new = []
                            if data_line[-1] == "\n": data_line = data_line[:-1]
                            if read_text_qualifier:
                                parsed_line = parseText(data_line, read_delimiter, [read_text_qualifier], False)
                            else:
                                parsed_line = data_line.split(read_delimiter)
                            if len(parsed_line) != max_columns:
                                is_error = True
                                if len(parsed_line) > max_columns: max_columns = len(parsed_line)
                            for c in parsed_line:
                                if len(c) >= 2:
                                    if c[0] == read_text_qualifier and c[-1] == read_text_qualifier: c = c[1:-1]
                                    #print(c)
                                if c != "":
                                    row_new.append(c)
                                else:
                                    row_new.append(None)
                            data_new.append(row_new)
                            if read_lines == row: break
                            #print(row_new)
                            row += 1
                            #time.sleep(1)
                            data_line = f.readline()
                    #print(data_new)
                    print()
                    if is_error:
                        if read_columns:
                            # add new column names only
                            for i in range(len_columns, max_columns):
                                cc = 0
                                rest = max_columns
                                while rest > 0:
                                    rest = int(rest/(10**cc))
                                    #print(rest)
                                    cc += 1
                                c = default_columns_name + f"{(i+1):0{(cc-1)}}"
                                columns_new.append(c)
                        else:
                            # create all column names again
                            columns_new = []
                            for i in range(max_columns):
                                cc = 0
                                rest = max_columns
                                while rest > 0:
                                    rest = int(rest/(10**cc))
                                    #print(rest)
                                    cc += 1
                                c = default_columns_name + f"{(i+1):0{(cc-1)}}"
                                columns_new.append(c)
                        for row, d in enumerate(data_new):
                            if max_columns > len(d):
                                error +=1
                                if error >= 0 and error < 10:
                                    printRed(f"ERROR on row {row+1}. Check carefully!!!")
                                elif error == 10:
                                    printRed(f"Further ERROR messages surpressed!!!")
                                for i in range(max_columns - len(d)):
                                    d.append(None)
                    if error > 0:
                        printInvRed(f"ERRORs in TOTAL {error}. Check carefully!!!")
                        print(max_columns, len_columns)
                    if len(data_new) > 0 or len(columns_new) > 0:
                        data = data_new
                        columns = columns_new
                        data_old = None
                        columns_old = None
                        print()
                        show_data(data, columns)
                    else:
                        printInvRed("! There are no data returned from this file !")
                        OK = 2
            except Exception as e:
                traceback.print_exc()
                printInvRed(str(e))
                OK = 2

        elif command == "export":
            export_filename = options["filename"]
            export_delimiter = options["delimiter"]
            if options.get("none") is not None:
                export_none = options["none"]
            else:
                export_none = None  # never happens, but was before, now is ""
            #print("export_none", export_none)
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
                            if c is None: c = export_none
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
                    start = time.perf_counter()
                    OK_returned = do_sql(sql_load)
                    end = time.perf_counter()
                    print()
                    if OK_returned == 1:
                        print("Elapsed time: " + str(timedelta(seconds=end-start)))
                    elif OK_returned > 1:
                        printRed("Elapsed time: " + str(timedelta(seconds=end-start)))
                        time.sleep(2)
                    else: break

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

            #print()
            #print(db_version + sql)
            print(db_version + sql.format(columns_print))
            #print(columns, data)
            try:
                c = conn.cursor()
                #print(columns_print)
                #print(sql.format(columns_print))
                c.executemany(sql.format(columns_print), data)
                conn.commit()
                print()
                printInvGreen("! There are no data returned from this sql query !")
            except Exception as e:
                traceback.print_exc()
                printInvRed(str(e))
                if OK: OK = 2

        elif command == "print" or command == "print data" or command == "print data easy" or command == "print columns" or command == "print history":
            if command == "print columns": options["what"] = "columns"
            if command == "print" or command == "print data" or command == "print data easy": options["what"] = "data"
            if command == "print history": options["what"] = "history"
            if options["what"] == "c": options["what"] = "columns"
            if options["what"] == "d": options["what"] = "data"
            if options["what"] == "h": options["what"] = "history"

            if options["what"] == "columns":

                #print(", ".join([str(c) for c in columns]))
                print(columns)

            elif options["what"] == "history":

                print(", ".join([str(c) for c in command_history]))

            elif options["what"] == "data":

                fromm = options["from"]
                too = options["to"]
                stepp = options["step"]
                listt = options["list"]
                randd = options["random"]
                colss = options["columns"]
                noness = options.get("nones")
                noneso = options.get("nones_option")
                title = options.get("title")
                note = options.get("note")
                title_color = options.get("title_color")
                note_color = options.get("note_color")
                #print("Title:", title)
                #print(fromm, too, stepp)

                nrows = len(data)
                ncols = len(columns)

                rowsi, colsi = data_select()
                #print(rows_show)

                columns_show = [columns[ci-1] for ci in colsi]

                title_text = ""

                if title is not None:   # include empty string to show no title
                    title_text = title
                    #printInvGreen(title)
                elif len(listt) > 0 and randd == 0:
                    if len(colss) > 0:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with selected columns {columns_show}."
                        #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with selected columns {columns_show}.")
                    else:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with all columns."
                        #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with all columns.")
                elif len(listt) > 0 and randd > 0:
                    if len(colss) > 0:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with selected columns {columns_show}."
                        #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with selected columns {columns_show}.")
                    else:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with all columns."
                        #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with all columns.")
                elif randd > 0:
                    if len(colss) > 0:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with selected columns {columns_show}."
                        #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with selected columns {columns_show}.")
                    else:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with all columns."
                        #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with all columns.")
                else:
                    if len(colss) > 0:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with selected columns {columns_show}."
                        #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with selected columns {columns_show}.")
                    else:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with all columns."
                        #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with all columns.")

                if title_text: # excluse empty string to show title
                    if title_color:
                        cc = colorCode(title_color)
                        printColor(title_text, cc)
                    else:
                        cc = INVGREEN
                        printColor(title_text, cc)

                rows = range(1, nrows + 1)
                #print(rows)
                print_data(rowsi, colsi, data, columns, rows, rows_label)

                if note:
                    print()
                    if note_color:
                        cc = colorCode(note_color)
                        printColor(note, cc)
                    else:
                        print(note)


        elif command == "data fill easy" or command == "data fill":

            if not data_old and not columns_old:
                data_old = data.copy()
                columns_old = columns.copy()

            fill_formats = options.get("formats")
            fill_nones = options.get("nones")
            title = options.get("title")
            note = options.get("note")
            title_color = options.get("title_color")
            note_color = options.get("note_color")
            #print("Title:", title)
            #print(fromm, too, stepp)

            nrows = len(data)
            ncols = len(columns)

            data_fill(fill_formats, fill_nones)
            #print(rows_show)

            title_text = ""

            if title is not None:   # include empty string to show no title
                title_text = title
                #printInvGreen(title)
            else:
                title_text = f"Format data {fill_formats}"

            if title_text: # excluse empty string to show title
                if title_color:
                    cc = colorCode(title_color)
                    printColor(title_text, cc)
                else:
                    cc = INVGREEN
                    printColor(title_text, cc)

            #rows = range(1, nrows + 1)
            #print(rows)
            #print_data(rowsi, colsi, data, columns, rows, rows_label)
            show_data(data, columns, False)

            if note:
                print()
                if note_color:
                    cc = colorCode(note_color)
                    printColor(note, cc)
                else:
                    print(note)

            #print(columns, data)

        elif command == "data reset":
            if data_old and columns_old:
                data = data_old.copy()
                columns = columns_old.copy()
            show_data(data, columns)

        elif command == "data select easy" or command == "data select":

            if not data_old and not columns_old:
                data_old = data.copy()
                columns_old = columns.copy()

            fromm = options["from"]
            too = options["to"]
            stepp = options["step"]
            listt = options["list"]
            randd = options["random"]
            colss = options["columns"]
            noness = options.get("nones")
            noneso = options.get("nones_option")
            title = options.get("title")
            note = options.get("note")
            title_color = options.get("title_color")
            note_color = options.get("note_color")
            #print("Title:", title)
            #print(fromm, too, stepp)

            nrows = len(data)
            ncols = len(columns)

            rowsi, colsi = data_select()
            #print(rows_show)

            columns_selected = [columns[ci-1] for ci in colsi]
            data_selected = [[data[ri-1][ci-1] for ci in colsi] for ri in rowsi]

            title_text = ""

            if title is not None:   # include empty string to show no title
                title_text = title
                #printInvGreen(title)
            elif len(listt) > 0 and randd == 0:
                if len(colss) > 0:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} listed cases {listi} with selected columns {columns_selected}."
                    #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with selected columns {columns_show}.")
                else:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} listed cases {listi} with all columns."
                    #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with all columns.")
            elif len(listt) > 0 and randd > 0:
                if len(colss) > 0:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} random cases from {listi} with selected columns {columns_selected}."
                    #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with selected columns {columns_show}.")
                else:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} random cases from {listi} with all columns."
                    #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with all columns.")
            elif randd > 0:
                if len(colss) > 0:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} random cases from {fromm} to {too} step {stepp} with selected columns {columns_selected}."
                    #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with selected columns {columns_show}.")
                else:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} random cases from {fromm} to {too} step {stepp} with all columns."
                    #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with all columns.")
            else:
                if len(colss) > 0:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} cases from {fromm} to {too} step {stepp} with selected columns {columns_selected}."
                    #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with selected columns {columns_show}.")
                else:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} cases from {fromm} to {too} step {stepp} with all columns."
                    #printInvGreen(f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with all columns.")

            if title_text: # excluse empty string to show title
                if title_color:
                    cc = colorCode(title_color)
                    printColor(title_text, cc)
                else:
                    cc = INVGREEN
                    printColor(title_text, cc)

            #rows = range(1, nrows + 1)
            #print(rows)
            #print_data(rowsi, colsi, data, columns, rows, rows_label)
            show_data(data_selected, columns_selected, False)

            if note:
                print()
                if note_color:
                    cc = colorCode(note_color)
                    printColor(note, cc)
                else:
                    print(note)

            data = data_selected.copy()
            columns = columns_selected.copy()

            #print(columns, data)

        elif command == "data profile easy" or command == "data profile":

            nrows = len(data)
            ncols = len(columns)
            colsi = range(1, ncols + 1)
            rowsi = range(1, nrows + 1)
            rows = range(1, nrows + 1)
            colsp = data_profile(rowsi, colsi, data, columns, rows, rows_label, progress_indicator = True)
            profile_data = []
            profile_columns = columns
            profile_rows = ["Type", "Valids", "Nones", "Valid %", "Sum", "Min", "Max", "Mean", "Q1", "Median", "Q3", "Range", "IQR", "Variance", "STD", "Skew", "Unique", "FirstCat"]
            profile_rows_label = '(Stat)'
            stats = ["t", "v", "n", "v%", "sum", "min", "max", "mean", "q1", "q2", "q3", "ran", "iqr", "var", "std", "skw","uni", "fnq"]

            maxc = 0
            for i, stat in enumerate(stats):
                profile_data.append([])
                for ci in colsp:
                    if ci > 0:  # rows_label
                        if stat == "v%":
                            if (colsp[ci]["v"] + colsp[ci]["n"]) > 0:
                                profile_data[i].append(round(100 * colsp[ci]["v"] / (colsp[ci]["v"] + colsp[ci]["n"]), 2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "ran":
                            if colsp[ci]["max"] and colsp[ci]["max"]:
                                profile_data[i].append(round(colsp[ci]["max"] - colsp[ci]["min"], 2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "iqr":
                            if colsp[ci]["q3"] and colsp[ci]["q1"]:
                                profile_data[i].append(round(colsp[ci]["q3"] - colsp[ci]["q1"], 2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "var":
                            if colsp[ci]["smd2"] and colsp[ci]["v"]:
                                profile_data[i].append(round(colsp[ci]["smd2"] / colsp[ci]["v"], 2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "std":
                            if colsp[ci]["smd2"] and colsp[ci]["v"]:
                                profile_data[i].append(round((colsp[ci]["smd2"] / colsp[ci]["v"])**0.5, 2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "skw":
                            if colsp[ci]["smd3"] and colsp[ci]["smd2"] and colsp[ci]["v"]:
                                profile_data[i].append(round(colsp[ci]["smd3"] / (colsp[ci]["v"] * (colsp[ci]["smd2"] / colsp[ci]["v"])**1.5), 2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "uni":
                            if len(colsp[ci]["c"]) < profile_max_categorical:
                                profile_data[i].append(len(colsp[ci]["c"]))
                                if len(colsp[ci]["c"]) > maxc: maxc = len(colsp[ci]["c"])
                            else:
                                profile_data[i].append("-")
                        elif stat == "fnq":
                            if colsp[ci]["fnq"] is None:
                                profile_data[i].append("-")
                            else:
                                profile_data[i].append(colsp[ci]["fnq"])
                        else:
                            for c in colsp[ci]:
                                #print(c, stat)
                                if c == stat:
                                    if isinstance(colsp[ci][c], float):
                                        profile_data[i].append(round(colsp[ci][c],2))
                                    elif isinstance(colsp[ci][c], str):
                                        profile_data[i].append(colsp[ci][c][:5])    # Quant, Categ
                                    elif colsp[ci][c] is None:
                                        profile_data[i].append("-")
                                    else:
                                        profile_data[i].append(colsp[ci][c])

            if maxc > profile_show_categorical:
                maxc = profile_show_categorical

            minc = len(profile_data)

            for i in range(maxc):
                profile_rows.append("Cat " + str(i + 1) + "_1")
                profile_data.append([])
                for ci in colsp:
                    if ci > 0:  # rows_label
                        if i < len(colsp[ci]["c"]):
                            #profile_data[i + minc].append(str(list(colsp[ci]["c"].keys())[i]) + "(" + str(colsp[ci]["c"][list(colsp[ci]["c"].keys())[i]]) + ")")
                            profile_data[i*3 + minc].append(str(list(colsp[ci]["c"].keys())[i]))
                        else:
                            profile_data[i*3 + minc].append("-")
                profile_rows.append("Cat " + str(i + 1) + "_2")
                profile_data.append([])
                for ci in colsp:
                    if ci > 0:  # rows_label
                        if i < len(colsp[ci]["c"]):
                            #profile_data[i + minc].append(str(list(colsp[ci]["c"].keys())[i]) + "(" + str(colsp[ci]["c"][list(colsp[ci]["c"].keys())[i]]) + ")")
                            profile_data[i*3 + minc + 1].append(str(colsp[ci]["c"][list(colsp[ci]["c"].keys())[i]]))
                        else:
                            profile_data[i*3 + minc + 1].append("-")
                profile_rows.append("Cat " + str(i + 1) + "_3")
                profile_data.append([])
                for ci in colsp:
                    if ci > 0: # rows_label
                        if i < len(colsp[ci]["c"]):
                            #profile_data[i + minc].append(str(list(colsp[ci]["c"].keys())[i]) + "(" + str(colsp[ci]["c"][list(colsp[ci]["c"].keys())[i]]) + ")")
                            profile_data[i*3 + minc + 2].append(str(round(100*colsp[ci]["c"][list(colsp[ci]["c"].keys())[i]]/colsp[ci]["v"],2)) + "%")
                        else:
                            profile_data[i*3 + minc + 2].append("-")


            #print(profile_data)

            nrows = len(profile_data)
            ncols = len(profile_columns)

            colsi = range(1, ncols + 1)
            rowsi = range(1, nrows + 1)

            print()
            print()
            #colsp = data_profile(rowsi, colsi, profile_data, profile_columns, profile_rows, profile_rows_label)
            print_data(rowsi, colsi, profile_data, profile_columns, profile_rows, profile_rows_label)


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
            printInvRed("! Command was not recognized or missing arguments !")

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
            error = 1
        try:
            #conn.commit()
            #print(c.statusmessage)
            data_new = c.fetchall()
            if c.description:
                columns_new = [col[0] for col in c.description]
            #conn.close()
        except Exception as e:
            #traceback.print_exc()
            #error = 1
            pass
        finally:
            if conn: conn.commit()
        if data_new or columns_new:
            data = data_new
            columns = columns_new
            data_old = None
            columns_old = None
            # mysql returns data as tuples, not lists as sqlite3
            # this causes problems in show_data if nrows > show_cases*2
            # (cannoct add anzthing to tuple, probably)
            #if len(data) > 0: print("Data class", data[0].__class__)
            #print("Columns class", columns.__class__)
            show_data(data, columns)
        elif not error:
            printInvGreen("! There are no data returned from this sql query !")
        else:
            printInvRed("! Error exexuting this sql query !")
            if OK: OK = 2

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
    command_history.append(sql)
    variables["$all"]["print history"]["value"] = len(command_history)
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
                        #assert a1 != a2, f"Command '{key1}' has the same alternative as command '{key2}': '{a1}'."
                        pass

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
                start = time.perf_counter()
                OK_returned = do_sql(sql)
                end = time.perf_counter()
                print()
                if OK_returned == 1:
                    print("Elapsed time: " + str(timedelta(seconds=end-start)))
                elif OK_returned > 1:
                    printRed("Elapsed time: " + str(timedelta(seconds=end-start)))
                    time.sleep(2)
                else: break


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

        while OK_returned:

            interactive_pass += 1

            sql_filename = "interactive pass " + str(interactive_pass)
            sqls[sql_filename] = parseText(sql, ";")
            #OK_returned = 1
            for i, sql in enumerate(sqls[sql_filename]):
                printCom(f'''\n\\\\ SQL file '{sql_filename}' command no {str(i+1)} \\\\''')
                #print(sql)
                #print()
                start = time.perf_counter()
                OK_returned = do_sql(sql)
                end = time.perf_counter()
                print()
                if OK_returned == 1:
                    print("Elapsed time: " + str(timedelta(seconds=end-start)))
                elif OK_returned > 1:
                    printRed("Elapsed time: " + str(timedelta(seconds=end-start)))
                    time.sleep(1)
                else: break
            if OK_returned:
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
