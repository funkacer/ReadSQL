import os
import argparse
import sqlite3
import traceback

def parseArgv():

    parser = argparse.ArgumentParser()

    parser.add_argument('database', metavar='Database_filename', type=str, nargs=1,
                    help='Database filename (string)')
    parser.set_defaults(database="")

    parser.add_argument('sql_files', metavar='(SQL_filenames)', type=str, nargs='*',
                    help='Optional list of *.sql filenames (strings) separated by space')
    parser.set_defaults(sql_files="")

    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument('--interactive', dest='interactive', action='store_true')
    feature_parser.add_argument('--no-interactive', dest='interactive', action='store_false')
    parser.set_defaults(interactive='')

    return parser.parse_args()

def get_sql_queries_dict(lst):
    sqls = {}
    for sql_file in lst:
        #print('SQL file:', sql_file)
        sql_file_exists = os.path.isfile(sql_file)
        #print('Check if file exists:', sql_file_exists)
        if sql_file_exists:
            sqls[sql_file] = []
            with open(sql_file, 'r') as f:
                sql = f.read()
                #print('SQL file query:')
                #print(sql.strip(), sql.count(';'))
                if sql.count(';') > 1:
                    for s in sql.split(';'):
                        if s.strip() != '': sqls[sql_file].append(s.strip())
                else:
                    sqls[sql_file].append(sql.strip())
        else:
            print('WAWNING!!! SQL file:', sql_file, 'does not exist!', '\n')

    return sqls

def do_sql(conn, sql):

    try:
        c = conn.cursor()
        c.execute('''{}'''.format(sql))
        data = c.fetchall()
        if data:
            columns = [col[0] for col in c.description]
            row_format = "{:>15}" * (len(columns) + 1)
            print(row_format.format("", *columns))
            for i, row in enumerate(data):
                #print(row_format.format(str(i), *row)) # not posiible to pass None (Null in db)
                print(row_format.format(str(i), *[str(r) for r in row]))    # Null to None
        print()
        conn.commit()
        #conn.close()

    except Exception as e:
        traceback.print_exc()

def main():

    namespace = parseArgv()
    '''
    for k,v in vars(namespace).items():
        print(k, v)
    '''

    assert len(vars(namespace)['database']) == 1, 'Database_filename error'
    database_filename = vars(namespace)['database'][0]
    print('\n' + 'Database:', database_filename, '\n')
    conn = sqlite3.connect(database_filename)

    if len(vars(namespace)['sql_files']) > 0:
        sqls = get_sql_queries_dict(vars(namespace)['sql_files'])
        #print(sqls, '\n')

        for sqlf in sqls.keys():
            for i, sql in enumerate(sqls[sqlf]):
                print('SQL file {} query no {}:'.format(sqlf, str(i+1)))
                print(sql, '\n')
                do_sql(conn, sql)

    if len(vars(namespace)['sql_files']) == 0 and isinstance(vars(namespace)['interactive'], str) or vars(namespace)['interactive']:
        print("Entering interactive mode. Type 'quit' to quit.", '\n')
        sql = input('Sql: ')
        while sql.lower().strip() != 'quit':
            do_sql(conn, sql)
            sql = input('Sql: ')

    conn.close()

if __name__ == '__main__':
    main()
