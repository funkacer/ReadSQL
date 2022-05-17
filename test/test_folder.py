import unittest
import os, sys
import numpy as np

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
#print(SCRIPT_DIR)
#print(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
#print(os.path.expanduser(__file__))

from src.params import variables
from src.params import command_options

#print(variables)

data = None
columns = None

class TestCase(unittest.TestCase):

    def test_folder_missing_argument(self):
        global variables, command_options, data, columns
        from ReadSQL import do_sql
        sql = r"\f"
        foldername_old = variables["$foldername"]["options"]["value"]
        variables, data, columns = do_sql(sql, variables, command_options, data, columns)
        OK_returned = variables["$command_results"]["options"]["value"][-1]
        foldername = variables["$foldername"]["options"]["value"]
        self.assertEqual(1, OK_returned)
        self.assertEqual(os.path.join(foldername_old, ""), foldername)

    def test_folder_empty_string(self):
        global variables, command_options, data, columns
        from ReadSQL import do_sql
        sql = r"\f ''"
        # getcwd is done in __main__
        variables["$foldername"]["options"]["value"] = os.getcwd()
        foldername_old = variables["$foldername"]["options"]["value"]
        variables, data, columns = do_sql(sql, variables, command_options, data, columns)
        OK_returned = variables["$command_results"]["options"]["value"][-1]
        foldername = variables["$foldername"]["options"]["value"]
        self.assertEqual(1, OK_returned)
        self.assertEqual(os.path.join(foldername_old, ""), foldername)

    def test_folder_exists(self):
        global variables, command_options, data, columns
        from ReadSQL import do_sql
        sql = r"\f test_folder_exists"
        variables, data, columns = do_sql(sql, variables, command_options, data, columns)
        OK_returned = variables["$command_results"]["options"]["value"][-1]
        foldername = variables["$foldername"]["options"]["value"]
        self.assertEqual(1, OK_returned)
        self.assertEqual(os.path.join(os.getcwd(), "test_folder_exists"), foldername)

    def test_folder_not_exists(self):
        global variables, command_options, data, columns
        from ReadSQL import do_sql
        variables["$foldername"]["options"]["value"] = os.getcwd()
        sql = r"\f test_folder_not_exists"
        variables, data, columns = do_sql(sql, variables, command_options, data, columns)
        OK_returned = variables["$command_results"]["options"]["value"][-1]
        foldername = variables["$foldername"]["options"]["value"]
        self.assertEqual(2, OK_returned)
        self.assertEqual(os.getcwd(), foldername)

    def test_folder_parent(self):
        global variables, command_options, data, columns
        from ReadSQL import do_sql
        variables["$foldername"]["options"]["value"] = os.path.join(os.getcwd(), "test_folder_exists")
        sql = r"\f .."
        variables, data, columns = do_sql(sql, variables, command_options, data, columns)
        OK_returned = variables["$command_results"]["options"]["value"][-1]
        foldername = variables["$foldername"]["options"]["value"]
        self.assertEqual(1, OK_returned)
        self.assertEqual(os.getcwd(), foldername)

    def test_folder_complex1(self):
        global variables, command_options, data, columns
        from ReadSQL import do_sql
        variables["$foldername"]["options"]["value"] = os.path.join(os.getcwd(), "test_folder_exists")
        sql = r"\f ..\test_folder_exists"
        variables, data, columns = do_sql(sql, variables, command_options, data, columns)
        OK_returned = variables["$command_results"]["options"]["value"][-1]
        foldername = variables["$foldername"]["options"]["value"]
        self.assertEqual(1, OK_returned)
        self.assertEqual(os.getcwd(), foldername)

    def test_folder_complex1(self):
        global variables, command_options, data, columns
        from ReadSQL import do_sql
        variables["$foldername"]["options"]["value"] = os.path.join(os.getcwd(), "test_folder_exists")
        sql = r"\f ..\test_folder_exists"
        variables, data, columns = do_sql(sql, variables, command_options, data, columns)
        OK_returned = variables["$command_results"]["options"]["value"][-1]
        foldername = variables["$foldername"]["options"]["value"]
        self.assertEqual(1, OK_returned)
        self.assertEqual(variables["$foldername"]["options"]["value"], foldername)

    def test_folder_complex2(self):
        global variables, command_options, data, columns
        from ReadSQL import do_sql
        variables["$foldername"]["options"]["value"] = os.path.join(os.getcwd(), "test_folder_exists")
        sql = r"\f \..\test_folder_exists\..\\"
        variables, data, columns = do_sql(sql, variables, command_options, data, columns)
        OK_returned = variables["$command_results"]["options"]["value"][-1]
        foldername = variables["$foldername"]["options"]["value"]
        self.assertEqual(1, OK_returned)
        self.assertEqual(os.getcwd(), foldername)


'''

    def test_integers_part(self):
        from src.check_input import check_input
        options = [-22,-11,-2,-1,0,1,2,11,22]
        for input in [-2,-1,0,1,2]:
            self.assertEqual(input, check_input(input, options))

    def test_integers_mismach1(self):
        from src.check_input import check_input
        options = [1,2]
        input = 1.0
        #assert input == check_input(input, options)
        self.assertEqual(input, check_input(input, options))
        input = 2.0
        self.assertEqual(input, check_input(input, options))

    def test_integers_mishmash2(self):
        from src.check_input import check_input
        options = [-22,-11,-2,-1,0,1,2,11,22]
        for input in [-22.0,-11.0,-2.0,-1.0,0.0,1.0,2.0,11.0,22.0]:
            self.assertEqual(input, check_input(input, options))

    def test_integers_random(self):
        from src.check_input import check_input
        #options = np.random.choice(np.random.randint(0,1000000,10000),10,replace=False)
        options = [int(a) for a in np.random.randint(0,1000000,1000)]
        options = list(np.random.randint(0,1000000,1000))
        print(options[0].__class__)
        for input in options:
            self.assertEqual(input, check_input(input, options))


    def test_integers_mishmash3(self):
        from src.check_input import check_input
        options = ['-22','-11','-2','-1','0','1','2','11','22']
        options.extend([-22,-11,-2,-1,0,1,2,11,22])
        print(options)
        for input in options:
            with self.assertRaises(TypeError):
                check_input(input, options)


    def test_floats_simple(self):
        from src.check_input import check_input
        options = [-220.9,-22.8,-11.7,-2.6,-1.5,0.4,1.3,2.2,11.1,22.0, 220.99]
        for input in options:
            self.assertEqual(input, check_input(input, options))

    def test_floats_part(self):
        from src.check_input import check_input
        options = [-22.0,-11.0,-2.0,-1.0,0.0,1.0,2.0,11.0,22.0]
        for input in [-2,-1,0,1,2]:
            self.assertEqual(input, check_input(input, options))

    def test_floats_mishmash1(self):
        from src.check_input import check_input
        options = [1.0,2.0]
        input = 1
        #assert input == check_input(input, options)
        self.assertEqual(input, check_input(input, options))
        input = 2
        self.assertEqual(input, check_input(input, options))

    def test_floats_mishmash2(self):
        from src.check_input import check_input
        options = [-22,-11,-2,-1,0,1,2,11,22]
        for input in [-22.0,-11.0,-2.0,-1.0,0.0,1.0,2.0,11.0,22.0]:
            self.assertEqual(input, check_input(input, options))

    def test_floats_random(self):
        from src.check_input import check_input
        options = list(np.random.random(1000)*1000000)
        print(options[0].__class__)
        for input in options:
            self.assertEqual(input, check_input(input, options))


    def test_floats_mishmash3(self):
        from src.check_input import check_input
        options = [-22.0,-11.0,-2.0,-1.0,0.0,1.0,2.0,11.0,22.0]
        for input in options:
            self.assertEqual(input, check_input(int(input), options))


    def test_strings_simple(self):
        from src.check_input import check_input
        options = ["ahoj","alabama"]
        for input in options:
            self.assertEqual(input, check_input(input, options))

    def test_strings_capital_letters(self):
        from src.check_input import check_input
        options = ["Ahoj","ahoj"]
        self.assertEqual("ahoj", check_input("ahoj", options))
        self.assertEqual("Ahoj", check_input("Ahoj", options))
        self.assertEqual("ahoj", check_input("ahoj", options, False))
        self.assertEqual("Ahoj", check_input("Ahoj", options, False))

    def test_strings_parts1(self):
        from src.check_input import check_input
        options = ["Ahoj","ahoj",'A','a']
        #assert input == check_input(input, options)
        for input in options:
            self.assertEqual(input, check_input(input, options))

    def test_strings_parts2(self):
        from src.check_input import check_input
        options = ["Ahoj","ahoj",'Ah','ah']
        #assert input == check_input(input, options)
        for input in options:
            print(input, check_input(input[0], options))
            self.assertEqual(None, check_input(input[0], options))


    def test_strings_mishmash3(self):
        from src.check_input import check_input
        options = ["Ahoj","ahoj"]
        for input in [-2.0,-1.0,0.0,1.0,2.0]:
            with self.assertRaises(TypeError):
                check_input(input, options)
'''
