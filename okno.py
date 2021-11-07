import tkinter as tk

##root = tk.Tk()
##root.title('Narozeniny')
##app = Application(master=root)
##app.mainloop()

from tkinter import Frame, Text, Scrollbar, Pack, Grid, Place
from tkinter.constants import RIGHT, LEFT, Y, BOTH

#root = tk.Tk()
#root.title('Narozeniny souhrn:')

class ScrolledText(Text):
    def __init__(self, master=None, **kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)

        kw.update({'yscrollcommand': self.vbar.set})
        Text.__init__(self, self.frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)

def zobraz(AAA):
    from tkinter.constants import END

    #global AAA
    AAA += "\n© Jiří Černý, 2016\n"
    stext = ScrolledText(bg='white', height=10)
    stext.insert(END, AAA)
    stext.pack(fill=BOTH, side=LEFT, expand=True)
    stext.focus_set()
    stext.mainloop()
