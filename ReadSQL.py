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

try:
    print("mysqlclient version:", version("mysqlclient"))
    import MySQLdb
except Exception as e:
    print("No MySQL support. Please run pip install mysqlclient")
    traceback.print_exc()

from okno import zobraz

def parseArgv(argument_list):

    parser = argparse.ArgumentParser()

    parser.add_argument('sql_files', metavar='(SQL_filenames)', type=str, nargs='*',
                    help='Optional list of *.sql filenames (strings) separated by space')
    parser.set_defaults(sql_files="")

    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument('--interactive', dest='interactive', action='store_true')
    feature_parser.add_argument('--no-interactive', dest='interactive', action='store_false')
    parser.set_defaults(interactive='')

    return parser.parse_args(argument_list)

def parseSql(sql_filename, sql):
    global sqls
    sqls[sql_filename] = []
    if sql.count(';') > 0:
        for s in sql.split(';'):
            if s.strip() != '': sqls[sql_filename].append(s.strip())
    else:
        sqls[sql_filename].append(sql.strip())
    return None

def get_sql_queries_dict(lst):
    for sql_filename in lst:
        #print('SQL file:', sql_file)
        file_exists, full_filename = check_filename(sql_filename)
        #print('Check if file exists:', sql_file_exists)
        if file_exists:
            with open(full_filename, mode="r", encoding="utf-8") as f:
                sql = f.read()
                #print('SQL file query:')
                #print(sql.strip(), sql.count(';'))
                parseSql(full_filename, sql)
        else:
            print('! SQL file:', sql_filename, 'does not exist !')
    return None

def check_filename(filename):
    file_exists = False
    if folder and not os.path.isabs(filename):
        full_filename = os.path.realpath(os.path.join(folder_name, os.path.expanduser(filename)))
    else:
        full_filename = filename
    file_exists = os.path.isfile(full_filename)
    #print(full_filename)
    return file_exists, full_filename

def do_sql(sql):

    global conn, data, columns, db_filename, folder, folder_name, db_version

    OK = 1
    if sql.startswith('---'):
        if sql.startswith('---quit'):
            OK = 0
        elif sql.startswith('---pause:'):
            if 'ask' in sql:
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
                                print('There are {} rows. Showing first / last {} cases.'.format(str(nrows), str(10)))
                                print(row_format.format("(Row)", *columns))
                                for i, row in enumerate(data[:10]):
                                    print(row_format.format(str(i+1), *[str(r) for r in row]))    # Null to None
                                print('\n','...','\n')
                                for i, row in enumerate(data[-10:]):
                                    print(row_format.format(str(nrows-10+i+1), *[str(r) for r in row]))
                        zobraz(show)
                    elif asked == "q":
                        OK = 0

        elif sql.startswith('---sqlite3::memory:'):
            print('\n' + 'Using database in memory. Save or loose!')
            try:
                conn = sqlite3.connect(':memory:')
                db_version = "Sqlite3: memory: "
            except Exception as e:
                traceback.print_exc()

        elif sql.startswith('---mysql:'):
            db_schema = sql[len('---mysql:'):]
            #connpars = parse_connstring(connstring)
            #print(connpars['server'])
            #print(connpars['user'])
            #print(connpars['password'])
            try:
                conn = MySQLdb.connect("localhost", "root", "admin", use_unicode=True,charset='utf8')
                c = conn.cursor()
                c.execute('''use {}'''.format(db_schema))
                conn.commit()
                db_version = f"MySQL: {db_schema}: "
                #cursor = conn.cursor()
                #conn = sqlite3.connect(full_filename)
            except Exception as e:
                traceback.print_exc()

        elif sql.startswith('---sqlite3:'):
            db_filename = sql[len('---sqlite3:'):]
            file_exists, full_filename = check_filename(db_filename)
            if file_exists:
                print("Using database '{}'.".format(full_filename))
            else:
                print("Creating database '{}'.".format(full_filename))
            try:
                conn = sqlite3.connect(full_filename)
                db_version = f"Sqlite3: {full_filename}: "
            except Exception as e:
                traceback.print_exc()
        elif sql.startswith('---folder:'):
            folder_old = folder
            folder_name_old = folder_name
            folder_name = sql[len('---folder:'):]
            folder = os.path.isdir(folder_name)
            if folder:
                print("Using folder '{}'.".format(folder_name))
            else:
                if folder_old:
                    print("Folder '{}' does not exist. Using current folder '{}'.".format(folder_name, folder_name_old))
                    folder = folder_old
                    folder_name = folder_name_old
                else:
                    # folder_name_old is None if sql imported file has wrong ---folder command
                    print("Folder '{}' does not exist. Using working directory '{}'.".format(folder_name, os.getcwd()))
                    folder_name = os.getcwd()
        elif sql.startswith('---import:'):
            sql_filename = sql[len('---import:'):]
            file_exists, full_filename = check_filename(sql_filename)
            #print('Check if file exists:', sql_file_exists)
            if file_exists:
                with open(full_filename, 'r') as f:
                    sql = f.read()
                    #print('SQL file query:')
                    #print(sql.strip(), sql.count(';'))
                    parseSql(full_filename, sql)
                for i, sql in enumerate(sqls[full_filename]):
                    print("SQL file '{}' command no {}:".format(full_filename, str(i+1)))
                    print(sql)
                    print()
                    do_sql(sql)
            else:
                print("! SQL file '{}' does not exist !".format(full_filename))
        elif sql.startswith('---save:'):
            save_filename = sql[len('---save:'):]
            file_exists, full_filename = check_filename(save_filename)
            print("Save: '{}'".format(save_filename))
            try:
                with open(full_filename, 'w') as f:
                    for c in columns:
                        f.write(str(c) + '\t')
                    f.write('\n')
                    for d in data:
                        for c in d:
                            f.write(str(c) + '\t')
                        f.write('\n')
            except Exception as e:
                traceback.print_exc()
        elif sql.startswith('---insert:'):
            save_tablename = sql.split(':')[1]
            print('\n' + 'Save:', save_tablename)
            part1 = ''
            part2 = ''
            try:
                for i, c in enumerate(columns):
                    if i == 0:
                        part1 += '{{0[{}]}}'.format(str(i))
                        #part2 += '?'.format(str(i))
                        part2 += '%s'.format(str(i))
                    else:
                        part1 += ',{{0[{}]}}'.format(str(i))
                        #part2 += ',?'.format(str(i))
                        part2 += ',%s'.format(str(i))
                sql = '''insert into {} ({}) values ({})'''.format(save_tablename, part1, part2)
                print(sql)
                #print(columns, data)
                c = conn.cursor()
                c.executemany(sql.format(columns), data)
                conn.commit()
            except Exception as e:
                traceback.print_exc()
        elif sql.startswith('---print:columns'):
            print(', '.join([str(c) for c in columns]))
        elif sql.startswith('---print:'):
            fromm_toos = sql[len('---print:'):].split(',')
            #print(fromm_toos)
            for ft in range(len(fromm_toos)):
                fromm_too = fromm_toos[ft].split(':')
                fromm, too, stepp = 1, len(data), 1
                if len(fromm_too) == 1:
                    if fromm_too[0].strip() != '':
                        try:
                            fromm = int(fromm_too[0])
                            too = fromm
                        except Exception as e:
                            traceback.print_exc()
                if len(fromm_too) == 2:
                    if fromm_too[0].strip() != '':
                        try:
                            fromm = int(fromm_too[0])
                        except Exception as e:
                            traceback.print_exc()
                    if fromm_too[1].strip() != '':
                        try:
                            too = int(fromm_too[1])
                        except Exception as e:
                            traceback.print_exc()
                if len(fromm_too) > 2:
                    if fromm_too[0].strip() != '':
                        try:
                            fromm = int(fromm_too[0])
                        except Exception as e:
                            traceback.print_exc()
                    if fromm_too[1].strip() != '':
                        try:
                            too = int(fromm_too[1])
                        except Exception as e:
                            traceback.print_exc()
                    if fromm_too[2].strip() != '':
                        try:
                            stepp = int(fromm_too[2])
                        except Exception as e:
                            traceback.print_exc()
                #print(fromm, too, stepp)
                row_format = "{:>15}" * (len(columns) + 1)
                nrows = len(data)
                if fromm <= 0: fromm = 1
                if too <= 0: too = 1
                if stepp <= 0: stepp = 1
                if too > nrows: too = nrows
                print('There are {} rows. Showing cases {} to {} step {}.'.format(str(nrows), str(fromm), str(too), str(stepp)))
                print(row_format.format("(Row)", *columns))
                for i, row in enumerate(data[fromm-1:too:stepp]):
                    print(row_format.format(str(fromm+i*stepp), *[str(r) for r in row]))    # Null to None
                print('\n')
        else:
            print("! Command was not recognized !")
    else:
        print(db_version + sql + '\n')
        try:
            c = conn.cursor()
            c.execute('''{}'''.format(sql))
            data = c.fetchall()
            if data:
                columns = [col[0] for col in c.description]
                row_format = "{:>15}" * (len(columns) + 1)
                nrows = len(data)
                if nrows < 100:
                    print('There are {} rows. Showing all cases.'.format(str(nrows)))
                    print(row_format.format("(Row)", *columns))
                    for i, row in enumerate(data):
                        #print(row_format.format(str(i), *row)) # not posiible to pass None (Null in db)
                        print(row_format.format(str(i+1), *[str(r) for r in row]))    # Null to None
                else:
                    print('There are {} rows. Showing first / last {} cases.'.format(str(nrows), str(10)))
                    print(row_format.format("(Row)", *columns))
                    for i, row in enumerate(data[:10]):
                        print(row_format.format(str(i+1), *[str(r) for r in row]))    # Null to None
                    print('\n','...','\n')
                    for i, row in enumerate(data[-10:]):
                        print(row_format.format(str(nrows-10+i+1), *[str(r) for r in row]))    # Null to None
            else:
                print('! There are no data returned from this sql query !')
            conn.commit()
            #conn.close()
        except Exception as e:
            traceback.print_exc()
    #print()
    return OK


def main(argv):

    global conn, sqls, data, columns, folder, folder_name, db_version

    conn = None
    sqls = {}
    data = None
    columns = None
    folder = None
    folder_name = None
    db_version = None

    namespace = parseArgv(argv)
    '''
    for k,v in vars(namespace).items():
        print(k, v)
    '''

    if len(vars(namespace)['sql_files']) > 0:
        get_sql_queries_dict(vars(namespace)['sql_files'])
        #print(sqls)

        for sql_filename in sqls.keys():
            #OK_returned = 1
            for i, sql in enumerate(sqls[sql_filename]):
                print("\n------------" + " SQL file '{}' command no {} ".format(sql_filename, str(i+1)) + "------------")
                #print(sql)
                #print()
                OK_returned = do_sql(sql)
                if OK_returned == 0: break

    if len(vars(namespace)['sql_files']) == 0 and isinstance(vars(namespace)['interactive'], str) or vars(namespace)['interactive']:
        print("\nEntering interactive mode. Type '---quit' to quit.")

        if conn:
            print("Using database '{}'. Use '---sqlite3:filename' for change.".format(db_filename))
        else:
            print("Database is not specified. Please use '---sqlite3:filename' for example.")

        if folder:
            print("Using folder '{}'.".format(folder_name))
        else:
            folder_name = os.getcwd()
            print("Folder is not specified. Using working directory '{}'.".format(folder_name))
        print()

        interactive_pass = 0
        sql = input('Sql: ')

        while sql.lower().strip() != '---quit':

            interactive_pass += 1

            sql_file = 'interactive pass ' + str(interactive_pass)
            parseSql(sql_file, sql)
            #OK_returned = 1
            for i, sql in enumerate(sqls[sql_file]):
                print("\n------------" + " SQL file '{}' command no {} ".format(sql_file, str(i+1)) + "------------")
                #print(sql)
                #print()
                OK_returned = do_sql(sql)
                if OK_returned == 0: break
            if OK_returned == 1: sql = input(db_version)

    try:
        conn.close()
    except Exception as e:
        #traceback.print_exc()
        pass
    print()

if __name__ == '__main__':
    main(sys.argv[1:])
