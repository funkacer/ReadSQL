import sys
import os
import argparse
import sqlite3
import traceback

def parseArgv(argument_list):

    parser = argparse.ArgumentParser()

    parser.add_argument('database', metavar='Database_filename', type=str, nargs='?',
                    help='Database filename (string)')
    parser.set_defaults(database="")

    parser.add_argument('sql_files', metavar='(SQL_filenames)', type=str, nargs='*',
                    help='Optional list of *.sql filenames (strings) separated by space')
    parser.set_defaults(sql_files="")

    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument('--interactive', dest='interactive', action='store_true')
    feature_parser.add_argument('--no-interactive', dest='interactive', action='store_false')
    parser.set_defaults(interactive='')

    return parser.parse_args(argument_list)

def parseSql(sql_file, sql):
    global sqls
    sqls[sql_file] = []
    if sql.count(';') > 0:
        for s in sql.split(';'):
            if s.strip() != '': sqls[sql_file].append(s.strip())
    else:
        sqls[sql_file].append(sql.strip())
    return None

def get_sql_queries_dict(lst):
    global sqls
    for sql_file in lst:
        #print('SQL file:', sql_file)
        sql_file_exists = os.path.isfile(sql_file)
        #print('Check if file exists:', sql_file_exists)
        if sql_file_exists:
            with open(sql_file, 'r') as f:
                sql = f.read()
                #print('SQL file query:')
                #print(sql.strip(), sql.count(';'))
                parseSql(sql_file, sql)
        else:
            print('WAWNING!!! SQL file:', sql_file, 'does not exist!', '\n')

    return None

def do_sql(sql):

    global conn, data, columns

    if sql.startswith('---'):
        if sql.startswith('---sqlite3:') or sql.startswith('---use:'):
            database_filename = sql.split(':')[1]
            print('\n' + 'Database:', database_filename, '\n')
            conn = sqlite3.connect(database_filename)
        elif sql.startswith('---save:'):
            save_filename = sql.split(':')[1]
            print('\n' + 'Save:', save_filename, '\n')
            with open(save_filename, 'w') as f:
                for c in columns:
                    f.write(str(c) + '\t')
                f.write('\n')
                for d in data:
                    for c in d:
                        f.write(str(c) + '\t')
                    f.write('\n')
        elif sql.startswith('---insert:'):
            save_tablename = sql.split(':')[1]
            print('\n' + 'Save:', save_tablename, '\n')
            part1 = ''
            part2 = ''
            for i, c in enumerate(columns):
                if i == 0:
                    part1 += '{{0[{}]}}'.format(str(i))
                    part2 += '?'.format(str(i))
                else:
                    part1 += ',{{0[{}]}}'.format(str(i))
                    part2 += ',?'.format(str(i))
            sql = '''insert into {} ({}) values ({})'''.format(save_tablename, part1, part2)
            print(sql)
            #print(columns, data)
            c = conn.cursor()
            c.executemany(sql.format(columns), data)
            conn.commit()
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
                print('There are {} rows. Showing cases {} to {} step {}.'.format(str(nrows), str(fromm), str(too), str(stepp)), '\n')
                print(row_format.format("(Row)", *columns))
                for i, row in enumerate(data[fromm-1:too:stepp]):
                    print(row_format.format(str(fromm+i*stepp), *[str(r) for r in row]))    # Null to None
                print('\n')

    else:
        try:
            c = conn.cursor()
            c.execute('''{}'''.format(sql))
            data = c.fetchall()
            if data:
                columns = [col[0] for col in c.description]
                row_format = "{:>15}" * (len(columns) + 1)
                nrows = len(data)
                if nrows < 100:
                    print('There are {} rows. Showing all cases.'.format(str(nrows)), '\n')
                    print(row_format.format("(Row)", *columns))
                    for i, row in enumerate(data):
                        #print(row_format.format(str(i), *row)) # not posiible to pass None (Null in db)
                        print(row_format.format(str(i+1), *[str(r) for r in row]))    # Null to None
                else:
                    print('There are {} rows. Showing first / last {} cases.'.format(str(nrows), str(10)), '\n')
                    print(row_format.format("(Row)", *columns))
                    for i, row in enumerate(data[:10]):
                        print(row_format.format(str(i+1), *[str(r) for r in row]))    # Null to None
                    print('\n','...','\n')
                    for i, row in enumerate(data[-10:]):
                        print(row_format.format(str(nrows-10+i+1), *[str(r) for r in row]))    # Null to None
            conn.commit()
            #conn.close()
        except Exception as e:
            traceback.print_exc()

    print()


def main(argv):

    global conn, sqls, data, columns

    conn = None
    sqls = {}
    data = None
    columns = None

    namespace = parseArgv(argv)

    for k,v in vars(namespace).items():
        print(k, v)

    #assert len(vars(namespace)['database']) == 1, 'Database_filename error'
    database_filename = vars(namespace)['database']
    if database_filename != '':
        print('\n' + 'Database:', database_filename, '\n')
        conn = sqlite3.connect(database_filename)
    else:
        print('Database is not specified. Please use ---sqlite:filename for example.')

    if len(vars(namespace)['sql_files']) > 0:
        get_sql_queries_dict(vars(namespace)['sql_files'])
        #print(sqls, '\n')

        for sqlf in sqls.keys():
            for i, sql in enumerate(sqls[sqlf]):
                print('SQL file {} query no {}:'.format(sqlf, str(i+1)))
                print(sql, '\n')
                do_sql(sql)

    if len(vars(namespace)['sql_files']) == 0 and isinstance(vars(namespace)['interactive'], str) or vars(namespace)['interactive']:
        print("Entering interactive mode. Type 'quit' to quit.", '\n')

        interactive_pass = 0
        sql = input('Sql: ')

        while sql.lower().strip() != 'quit':

            interactive_pass += 1

            sql_file = 'interactive pass ' + str(interactive_pass)
            parseSql(sql_file, sql)
            for i, sql in enumerate(sqls[sql_file]):
                print('SQL {} query no {}:'.format(sql_file, str(i+1)))
                print(sql, '\n')
                #tady men conn
                do_sql(sql)
            sql = input('Sql: ')

    conn.close()

if __name__ == '__main__':
    main(sys.argv[1:])
