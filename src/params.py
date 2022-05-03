import os
import datetime
from importlib.metadata import version

#do_mp = True
do_mp = False

is_np = False
try:
    import numpy as np
    is_np = True
except Exception as e:
    traceback.print_exc()

is_mpl = False
try:
    import matplotlib.pyplot as plt
    is_mpl = True
except Exception as e:
    traceback.print_exc()

if is_np: print("Using numpy version:", version("numpy"))
if is_mpl: print("Using matplotlib version:", version("matplotlib"))

#from okno import zobraz

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
folder_exists = False
folder_name = ""
show_cases = 5
print_max_default = 10
profile_max_categorical = 100
profile_show_categorical = 5
rows_label = "(Row)"
command_history = []
default_columns_name = "Column_"
commands = {}
variables = {}
colsp = {}
data_memory = {}
columns_memory = {}
colsp_memory = {}
class_str = type("")
class_int = type(0)
class_float = type(0.0)

functions = set()
functions.add("@(")
functions.add("@int(")

def general_function(vartest):
    ret = None
    opt = None
    print("general_function", vartest)
    return ret, opt

def int_function(vartest):
    ret = None
    opt = None
    print("int_function", vartest)
    try:
        vartest = float(vartest)
        ret = int(vartest)
        opt = 1
    except Exception as e:
        traceback.print_exc()
    return ret, opt

def call_function(vartest, f):
    ret = None
    opt = None
    if f == "@(":
        ret, opt = general_function(vartest)
    if f == "@int(":
        ret, opt = int_function(vartest)
    return ret, opt


variables["$profile_show_categorical"] = {}
variables["$profile_show_categorical"]["shorts"] = []
variables["$profile_show_categorical"]["options"] = {}
variables["$profile_show_categorical"]["options"]["value"] = 5

variables["$do_mp"] = {}
variables["$do_mp"]["shorts"] = []
variables["$do_mp"]["options"] = {}
variables["$do_mp"]["options"]["value"] = False
    
variables["$row_format_l"] = {}
variables["$row_format_l"]["shorts"] = []
variables["$row_format_l"]["options"] = {}
variables["$row_format_l"]["options"]["value"] = lambda columns: "".join([f"{{:>{columns[c]['w']}}}" for c in columns]) if isinstance(columns, dict) else "{:>15}" * (len(columns) + 1)

variables["$rows_label"] = {}
variables["$rows_label"]["shorts"] = []
variables["$rows_label"]["options"] = {}
variables["$rows_label"]["options"]["value"] = "(Row)"

variables["$show_cases"] = {}
variables["$show_cases"]["shorts"] = []
variables["$show_cases"]["options"] = {}
variables["$show_cases"]["options"]["value"] = 5

variables["$command_history"] = {}
variables["$command_history"]["shorts"] = []
variables["$command_history"]["options"] = {}
variables["$command_history"]["options"]["value"] = []

variables["$command_results"] = {}
variables["$command_results"]["shorts"] = []
variables["$command_results"]["options"] = {}
variables["$command_results"]["options"]["value"] = []


RED, YELLOW, GREEN, BLUE, COM, INVGREEN, INVRED, END = '\033[91m', '\033[33m', '\033[92m', '\033[96m', '\033[4m', '\033[97m\033[42m', '\033[97m\033[101m', '\033[0m'

variables["$printRed"] = {}
variables["$printRed"]["shorts"] = []
variables["$printRed"]["options"] = {}
variables["$printRed"]["options"]["value"] = lambda sTxt: print(RED + sTxt + END)

variables["$printGreen"] = {}
variables["$printGreen"]["shorts"] = []
variables["$printGreen"]["options"] = {}
variables["$printGreen"]["options"]["value"] = lambda sTxt: print(GREEN + sTxt + END)

variables["$printYellow"] = {}
variables["$printYellow"]["shorts"] = []
variables["$printYellow"]["options"] = {}
variables["$printYellow"]["options"]["value"] = lambda sTxt: print(YELLOW + sTxt + END)

variables["$printBlue"] = {}
variables["$printBlue"]["shorts"] = []
variables["$printBlue"]["options"] = {}
variables["$printBlue"]["options"]["value"] = lambda sTxt: print(BLUE + sTxt + END)

variables["$printCom"] = {}
variables["$printCom"]["shorts"] = []
variables["$printCom"]["options"] = {}
variables["$printCom"]["options"]["value"] = lambda sTxt: print(COM + sTxt + END)

variables["$printInvGreen"] = {}
variables["$printInvGreen"]["shorts"] = []
variables["$printInvGreen"]["options"] = {}
variables["$printInvGreen"]["options"]["value"] = lambda sTxt: print(INVGREEN + sTxt + END)

variables["$printInvRed"] = {}
variables["$printInvRed"]["shorts"] = []
variables["$printInvRed"]["options"] = {}
variables["$printInvRed"]["options"]["value"] = lambda sTxt: print(INVRED + sTxt + END)

variables["$printColor"] = {}
variables["$printColor"]["shorts"] = []
variables["$printColor"]["options"] = {}
variables["$printColor"]["options"]["value"] = lambda sTxt, mColor: print(mColor + sTxt + END)


variables["$Assert"] = {}
variables["$Assert"]["shorts"] = []
variables["$Assert"]["options"] = {}
variables["$Assert"]["options"]["value"] = lambda bCond=False, sTxt='': variables["$printRed"]["options"]["value"](sTxt) if not bCond else None


variables["$conn"] = {}
variables["$conn"]["shorts"] = []
variables["$conn"]["options"] = {}
variables["$conn"]["options"]["value"] = None

variables["$db_schema"] = {}
variables["$db_schema"]["shorts"] = []
variables["$db_schema"]["options"] = {}
variables["$db_schema"]["options"]["value"] = ""

variables["$db_version"] = {}
variables["$db_version"]["shorts"] = []
variables["$db_version"]["options"] = {}
variables["$db_version"]["options"]["value"] = "None: "
    
variables["$folder_name_old"] = {}
variables["$folder_name_old"]["shorts"] = []
variables["$folder_name_old"]["options"] = {}
variables["$folder_name_old"]["options"]["value"] = ""

variables["$folder_name"] = {}
variables["$folder_name"]["shorts"] = []
variables["$folder_name"]["options"] = {}
variables["$folder_name"]["options"]["value"] = ""

variables["$folder_exists_old"] = {}
variables["$folder_exists_old"]["shorts"] = []
variables["$folder_exists_old"]["options"] = {}
variables["$folder_exists_old"]["options"]["value"] = False

variables["$folder_exists"] = {}
variables["$folder_exists"]["shorts"] = []
variables["$folder_exists"]["options"] = {}
variables["$folder_exists"]["options"]["value"] = False


variables["$parse_value_type"] = {}
variables["$parse_value_type"]["shorts"] = []
variables["$parse_value_type"]["options"] = {}
variables["$parse_value_type"]["options"]["value"] = "auto"

variables["$sleep"] = {}
variables["$sleep"]["shorts"] = []
variables["$sleep"]["options"] = {}
variables["$sleep"]["options"]["value"] = 1

variables["$all"] = {}
variables["$all"]["shorts"] = ["$a","$al"]
variables["$all"]["data"] = {}
variables["$all"]["data"]["value"] = 0
variables["$all"]["data"]["print"] = {}
variables["$all"]["data"]["print data"] = {}
variables["$all"]["data"]["print data all"] = {}
variables["$all"]["data"]["print data easy"] = {}
#variables["$all"]["print data"]["print data easy"]["what"] = []
variables["$all"]["data"]["data"] = {}
variables["$all"]["data"]["data select"] = {}
variables["$all"]["data"]["data select easy"] = {}
variables["$all"]["data"]["data fill"] = {}
variables["$all"]["data"]["data fill easy"] = {}
variables["$all"]["data"]["data profile"] = {}
variables["$all"]["data"]["data profile easy"] = {}

variables["$all"]["print history"] = {}
variables["$all"]["print history"]["value"] = 0
variables["$all"]["print history"]["print history"] = {}
variables["$columns_all"] = {}
variables["$columns_all"]["shorts"] = ["$columns_a","$ca"]
variables["$columns_all"]["data"] = {}
variables["$columns_all"]["data"]["value"] = []
variables["$columns_all"]["data"]["print"] = {}
variables["$columns_all"]["data"]["print data"] = {}
variables["$columns_all"]["data"]["print data easy"] = {}
variables["$columns_all"]["data"]["data"] = {}
variables["$columns_all"]["data"]["data select"] = {}
variables["$columns_all"]["data"]["data select easy"] = {}
variables["$columns_all"]["data"]["data fill"] = {}
variables["$columns_all"]["data"]["data fill easy"] = {}
variables["$columns_all"]["data"]["graph boxplot"] = {}
variables["$columns_all"]["data"]["graph barchart"] = {}
variables["$columns_all"]["data"]["graph linechart"] = {}

variables["$red"] = {}
variables["$red"]["shorts"] = ["$r"]
variables["$red"]["user"] = {}
variables["$red"]["user"]["value"] = 1
variables["$green"] = {}
variables["$green"]["shorts"] = ["$g"]
variables["$green"]["user"] = {}
variables["$green"]["user"]["value"] = 2
variables["$invGreen"] = {}
variables["$invGreen"]["shorts"] = ["$invgreen","$invg","$ig"]
variables["$invGreen"]["user"] = {}
variables["$invGreen"]["user"]["value"] = 20255
variables["$invRed"] = {}
variables["$invRed"]["shorts"] = ["$invred","$invr","$ir"]
variables["$invRed"]["user"] = {}
variables["$invRed"]["user"]["value"] = 10255
variables["$list"] = {}
variables["$list"]["shorts"] = ["$l"]
variables["$list"]["user"] = {}
#a = "a"
variables["$list"]["user"]["value"] = "[1,2,a]"

variables["$date"] = {}
variables["$date"]["shorts"] = ["$d"]
variables["$date"]["user"] = {}
variables["$date"]["user"]["value"] = "%Y-%m-%d"
variables["$time"] = {}
variables["$time"]["shorts"] = ["$t"]
variables["$time"]["user"] = {}
variables["$time"]["user"]["value"] = "%H:%M:%S"
variables["$mstime"] = {}
variables["$mstime"]["shorts"] = ["$t"]
variables["$mstime"]["user"] = {}
variables["$mstime"]["user"]["value"] = "%H:%M:%S.%f0"
#variables["$time"]["user"]["value"] = "%H:%M:%S.%f0"
#variables["$time"]["user"]["value"] = "%H:%M:%S.%f"
variables["$datetime"] = {}
variables["$datetime"]["shorts"] = ["$dt"]
variables["$datetime"]["user"] = {}
variables["$datetime"]["user"]["value"] = "%Y-%m-%d %H:%M:%S"

variables["$decimal_separator"] = {}
variables["$decimal_separator"]["shorts"] = ["$ds"]
variables["$decimal_separator"]["user"] = {}
variables["$decimal_separator"]["user"]["value"] = "."
variables["$thousands_separator"] = {}
variables["$thousands_separator"]["shorts"] = ["$ts"]
variables["$thousands_separator"]["user"] = {}
variables["$thousands_separator"]["user"]["value"] = ","

variables["$none"] = {}
variables["$none"]["shorts"] = ["$n", "$no"]
variables["$none"]["user"] = {}
variables["$none"]["user"]["value"] = None

variables["$now"] = {}
variables["$now"]["shorts"] = ["$now"]
variables["$now"]["user"] = {}
variables["$now"]["user"]["value"] = lambda x: datetime.datetime.now()

print(variables["$now"]["user"]["value"].__class__)
print(variables["$now"]["user"]["value"](None))

'''
import datetime
datetime.datetime.strptime('24052010', "%d%m%Y").date()
'''


#variables["$a"] = 0

command_options = {}

command_options["#"] = {}
command_options["#"]["name"] = ["title", "note", "title_color", "note_color"]
command_options["#"]["required"] = [False, False, False, False]
command_options["#"]["type"] = ["str", "str", "int", "int"]
command_options["#"]["default"] = [None, None, None, None]
command_options["#"]["help1"] = "Help for command '#'"
command_options["#"]["help2"] = ["Bla1","Bla2","Bla3","Bla4"]
command_options["#"]["alternative"] = ["#"]
command_options["#"]["altoption"] = [["tt"], ["nt"], ["tc"], ["nc"]]

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
command_options["folder"]["altoption"] = [["fn","f"]]


command_options["set variable easy"] = {}
command_options["set variable easy"]["name"] = ["names"]
command_options["set variable easy"]["required"] = [True]
command_options["set variable easy"]["type"] = ["dictlist"]
command_options["set variable easy"]["default"] = [None]
command_options["set variable easy"]["help1"] = "Help for command 'set'"
command_options["set variable easy"]["help2"] = ["Bla1"]
command_options["set variable easy"]["alternative"] = ["set variable", "sv"]
command_options["set variable easy"]["altoption"] = [["n"]]


command_options["set variable"] = {}
command_options["set variable"]["name"] = ["what", "names"]
command_options["set variable"]["required"] = [True, True]
command_options["set variable"]["type"] = [["variable", "v"], "dictlist"]
command_options["set variable"]["default"] = [None, None]
command_options["set variable"]["help1"] = "Help for command 'set'"
command_options["set variable"]["help2"] = ["Bla1", "Bla2"]
command_options["set variable"]["alternative"] = ["set", "s"]
command_options["set variable"]["altoption"] = [["w"], ["n"]]

command_options["connect sqlite3"] = {}
command_options["connect sqlite3"]["name"] = ["what", "filename", "parse_formats"]
command_options["connect sqlite3"]["required"] = [True, False, False]
command_options["connect sqlite3"]["type"] = [["sqlite3", "sqlite", "sql3", "sql", "s"], "str", "bool"]
command_options["connect sqlite3"]["default"] = [None, ":memory:", True]
command_options["connect sqlite3"]["help1"] = "Help for command 'connect'"
command_options["connect sqlite3"]["help2"] = ["Blabla1","Blabla2","Blabla3"]
command_options["connect sqlite3"]["alternative"] = ["connect", "c"]
command_options["connect sqlite3"]["altoption"] = [["w"], ["fn","f"], ["pf","p"]]

command_options["connect sqlite3 easy"] = {}
command_options["connect sqlite3 easy"]["name"] = ["filename", "parse_formats"]
command_options["connect sqlite3 easy"]["required"] = [False, False]
command_options["connect sqlite3 easy"]["type"] = ["str", "bool"]
command_options["connect sqlite3 easy"]["default"] = [":memory:", True]
command_options["connect sqlite3 easy"]["help1"] = "Help for command 'connect'"
command_options["connect sqlite3 easy"]["help2"] = ["Blabla1","Blabla2"]
command_options["connect sqlite3 easy"]["alternative"] = ["connect sqlite3", "connect sqlite", "connect sql3", "connect sql", "connect s", "c sqlite3", "c sqlite", "c sql3", "c sql", "c s",  "csqlite3", "csqlite", "csql3", "csql", "cs"]
command_options["connect sqlite3 easy"]["altoption"] = [["fn","f"], ["pf","p"]]

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
command_options["connect mssql"]["name"] = ["database", "user", "password", "host", "port", "driver", "option"]
command_options["connect mssql"]["required"] = [False, False, False, False, False, False, False]
command_options["connect mssql"]["type"] = ["str", "str", "str", "str", "int", "str", "str"]
command_options["connect mssql"]["default"] = ["", "root", "admin", "localhost", 3306, "SQL Server", "trustedconn=true"]
command_options["connect mssql"]["help1"] = "Help for command 'folder'"
command_options["connect mssql"]["help2"] = ["Bla1", "Bla2", "Bla3", "Bla4", "Bla5", "Bla6", "Bla7"]
command_options["connect mssql"]["alternative"] = ["c mssql", "c ms", "cmssql", "cms"]
command_options["connect mssql"]["altoption"] = [["d"],["u"],["p"],["h"],["po"],["dr"],["o", "do"]]

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
command_options["export"]["altoption"] = [["fn","f"],["d"],["null","n"]]

command_options["load"] = {}
command_options["load"]["name"] = ["filename"]
command_options["load"]["required"] = [True]
command_options["load"]["type"] = ["str"]
command_options["load"]["default"] = [None]
command_options["load"]["help1"] = "Help for command 'folder'"
command_options["load"]["help2"] = ["Blabla1"]
command_options["load"]["alternative"] = ["l"]
command_options["load"]["altoption"] = [["fn","f"]]


command_options["table"] = {}
command_options["table"]["name"] = ["tablename", "drop_if_exists", "id"]
command_options["table"]["required"] = [True, False, False]
command_options["table"]["type"] = ["str", "bool", "str"]
command_options["table"]["default"] = [None, False, None]
command_options["table"]["help1"] = "Help for command 'folder'"
command_options["table"]["help2"] = ["Blabla1", "Blabla2", "Blabla3"]
command_options["table"]["alternative"] = ["table", "t"]
command_options["table"]["altoption"] = [["tn","t"], ["die","de","dt","d"], ["i"]]


command_options["insert"] = {}
command_options["insert"]["name"] = ["tablename"]
command_options["insert"]["required"] = [True]
command_options["insert"]["type"] = ["str"]
command_options["insert"]["default"] = [None]
command_options["insert"]["help1"] = "Help for command 'folder'"
command_options["insert"]["help2"] = ["Blabla1"]
command_options["insert"]["alternative"] = ["insert", "i"]
command_options["insert"]["altoption"] = [["tn","t"]]

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

command_options["print data all"] = {}
command_options["print data all"]["name"] = ["from", "to", "step", "random", "list", "columns", "nones", "nones_option", "title", "note", "title_color", "note_color"]
command_options["print data all"]["required"] = [False, False, False, False, False, False, False, False, False, False, False, False]
command_options["print data all"]["type"] = ["int", "int", "int", "int", "intlist", "strlist", "strlist", ["any","all","none"], "str", "str", "int", "int"]
command_options["print data all"]["default"] = [0, "$all", 1, 0, "[]", "[]", "[]", "any", None, None, None, None]
command_options["print data all"]["help1"] = "Help for command 'folder'"
command_options["print data all"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11","Bla12"]
command_options["print data all"]["alternative"] = ["print data all", "pda"]
command_options["print data all"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["nulls", "ns", "n"], ["no"], ["tt"], ["nt"], ["tc"], ["nc"]]

command_options["print data easy"] = {}
command_options["print data easy"]["name"] = ["from", "to", "step", "random", "list", "columns", "nones", "nones_option", "title", "note", "title_color", "note_color"]
command_options["print data easy"]["required"] = [False, False, False, False, False, False, False, False, False, False, False, False]
command_options["print data easy"]["type"] = ["int", "int", "int", "int", "intlist", "strlist", "strlist", ["any","all","none"], "str", "str", "int", "int"]
command_options["print data easy"]["default"] = [0, 0, 1, 0, "[]", "[]", "[]", "any", None, None, None, None]
command_options["print data easy"]["help1"] = "Help for command 'folder'"
command_options["print data easy"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11","Bla12"]
command_options["print data easy"]["alternative"] = ["print data", "pd"]
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
command_options["print columns"]["default"] = [None]
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


command_options["print variables"] = {}
command_options["print variables"]["name"] = ["what"]
command_options["print variables"]["required"] = [True]
command_options["print variables"]["type"] = [["variables", "v"]]
command_options["print variables"]["default"] = [None]
command_options["print variables"]["help1"] = "Help for command 'folder'"
command_options["print variables"]["help2"] = ["Bla1"]
command_options["print variables"]["alternative"] = ["print", "p"]
command_options["print variables"]["altoption"] = [["w"]]

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
command_options["data profile easy"]["name"] = ["from", "to", "step", "random", "list", "columns", "nones", "nones_option", "title", "note", "title_color", "note_color", "print_all", "purge"]
command_options["data profile easy"]["required"] = [False, False, False, False, False, False, False, False, False, False, False, False, False, False]
command_options["data profile easy"]["type"] = ["int", "int", "int", "int", "intlist", "strlist", "strlist", ["any","all","none"], "str", "str", "int", "int", "bool", "bool"]
command_options["data profile easy"]["default"] = [0, 0, 1, 0, "[]", "[]", "[]", "all", None, None, None, None, False, False]
command_options["data profile easy"]["help1"] = "Help for command 'folder'"
command_options["data profile easy"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11","Bla12","Bla13","Bla14"]
command_options["data profile easy"]["alternative"] = ["data profile", "d profile", "d pr", "d p", "dpr", "dp"]
command_options["data profile easy"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["nulls", "ns", "n"], ["no"], ["tt"], ["nt"], ["tc"], ["nc"], ["pa"], ["pu"]]

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

command_options["graph boxplot"] = {}
command_options["graph boxplot"]["name"] = ["what", "columns", "title", "show_fliers"]
command_options["graph boxplot"]["required"] = [True, False, False, False]
command_options["graph boxplot"]["type"] = [["boxplot","bo"], "strlist", "str", "bool"]
command_options["graph boxplot"]["default"] = ["boxplot", None, None, True]
command_options["graph boxplot"]["help1"] = "Help for command 'folder'"
command_options["graph boxplot"]["help2"] = ["Bla1","Bla2","Bla3","Bla4"]
command_options["graph boxplot"]["alternative"] = ["graph", "g"]
command_options["graph boxplot"]["altoption"] = [["w"],["c"],["tt"],["sf"]]

command_options["graph barchart"] = {}
command_options["graph barchart"]["name"] = ["what", "columns", "title"]
command_options["graph barchart"]["required"] = [True, False, False]
command_options["graph barchart"]["type"] = [["barchart","ba"], "strlist", "str"]
command_options["graph barchart"]["default"] = ["barchart", None, None]
command_options["graph barchart"]["help1"] = "Help for command 'folder'"
command_options["graph barchart"]["help2"] = ["Bla1","Bla2","Bla3"]
command_options["graph barchart"]["alternative"] = ["graph", "g"]
command_options["graph barchart"]["altoption"] = [["w"],["c"],["tt"]]

command_options["graph linechart"] = {}
command_options["graph linechart"]["name"] = ["what", "columns", "title"]
command_options["graph linechart"]["required"] = [True, False, False]
command_options["graph linechart"]["type"] = [["linechart","li"], "strlist", "str"]
command_options["graph linechart"]["default"] = ["linechart", None, None]
command_options["graph linechart"]["help1"] = "Help for command 'folder'"
command_options["graph linechart"]["help2"] = ["Bla1","Bla2","Bla3"]
command_options["graph linechart"]["alternative"] = ["graph", "g"]
command_options["graph linechart"]["altoption"] = [["w"],["c"],["tt"]]

command_options["graph histogram"] = {}
command_options["graph histogram"]["name"] = ["what", "columns", "split", "title"]
command_options["graph histogram"]["required"] = [True, False, False, False]
command_options["graph histogram"]["type"] = [["histogram","hi"], "strlist", "strlist", "str"]
command_options["graph histogram"]["default"] = ["histogram", None, None, None]
command_options["graph histogram"]["help1"] = "Help for command 'folder'"
command_options["graph histogram"]["help2"] = ["Bla1","Bla2","Bla3","Bla4"]
command_options["graph histogram"]["alternative"] = ["graph", "g"]
command_options["graph histogram"]["altoption"] = [["w"],["c"],["s"],["tt"]]

command_options["data memory easy"] = {}
command_options["data memory easy"]["name"] = ["name"]
command_options["data memory easy"]["required"] = [False]
command_options["data memory easy"]["type"] = ["str"]
command_options["data memory easy"]["default"] = ["1"]
command_options["data memory easy"]["help1"] = "Help for command 'folder'"
command_options["data memory easy"]["help2"] = ["Bla1"]
command_options["data memory easy"]["alternative"] = ["data memory", "data mem", "dm"]
command_options["data memory easy"]["altoption"] = [["n"]]

command_options["data memory"] = {}
command_options["data memory"]["name"] = ["what", "name"]
command_options["data memory"]["required"] = [True, False]
command_options["data memory"]["type"] = [["memory","mem","m"],"str"]
command_options["data memory"]["default"] = ["memory", "1"]
command_options["data memory"]["help1"] = "Help for command 'folder'"
command_options["data memory"]["help2"] = ["Bla1","Bla2"]
command_options["data memory"]["alternative"] = ["data", "d"]
command_options["data memory"]["altoption"] = [["w"],["n"]]

command_options["data activate easy"] = {}
command_options["data activate easy"]["name"] = ["name"]
command_options["data activate easy"]["required"] = [False]
command_options["data activate easy"]["type"] = ["str"]
command_options["data activate easy"]["default"] = ["1"]
command_options["data activate easy"]["help1"] = "Help for command 'folder'"
command_options["data activate easy"]["help2"] = ["Bla1"]
command_options["data activate easy"]["alternative"] = ["data activate", "data act", "da"]
command_options["data activate easy"]["altoption"] = [["n"]]

command_options["data activate"] = {}
command_options["data activate"]["name"] = ["what", "name"]
command_options["data activate"]["required"] = [True, False]
command_options["data activate"]["type"] = [["activate","act","a"],"str"]
command_options["data activate"]["default"] = ["memory", "1"]
command_options["data activate"]["help1"] = "Help for command 'folder'"
command_options["data activate"]["help2"] = ["Bla1","Bla2"]
command_options["data activate"]["alternative"] = ["data", "d"]
command_options["data activate"]["altoption"] = [["w"],["n"]]

command_options["split"] = {}
command_options["split"]["name"] = ["columns", "split"]
command_options["split"]["required"] = [True, True]
command_options["split"]["type"] = ["strlist", "strlist"]
command_options["split"]["default"] = [None, None]
command_options["split"]["help1"] = "Help for command 'folder'"
command_options["split"]["help2"] = ["Bla1","Bla2"]
command_options["split"]["alternative"] = ["split", "s"]
command_options["split"]["altoption"] = [["c"],["s"]]


