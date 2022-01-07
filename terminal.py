import os
  
# Get the size
# of the terminal
size = os.get_terminal_size()
  
  
# Print the size
# of the terminal
print(size)

columns, rows = os.get_terminal_size()
print(columns, rows)

os.system('color')
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

#from timeit import default_timer as timer
import time
from datetime import timedelta

#start = timer()
start = time.perf_counter()

# ....
# (your code runs here)
# ...
time.sleep(0.1)

#end = timer()
end = time.perf_counter()
print("Elapsed time:", timedelta(seconds=end-start))
