import time
import argparse
parser = argparse.ArgumentParser(description='A test')
parser.add_argument("ahoj=", metavar='N', help="Test variable", type=str)

args = parser.parse_args()

def foo():
    command_line_argument = args['ahoj=']
    bar = 2*int(args.args['ahoj='])
    print(bar)
    return


if  __name__ == "__main__":
    try:
        while True:
            foo()
            time.sleep(1)
    except KeyboardInterrupt:
        print('User has exited the program')
