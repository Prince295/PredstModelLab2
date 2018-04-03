import tkinter as interface

class ThemedLabel(interface.Label):
    def __init__(self, parent = None, **configs):
        interface.Label.__init__(self, parent, **configs)
        self.pack()
        self.config(fg='black', bg = 'white', font = 'times 30', relief='solid', justify = 'center', bd=3)

class OutLabel(interface.Label):
    def __init__(self,parent = None, **configs):
        interface.Label.__init__(self, parent, **configs)
        self.pack()
        self.config(fg='black', bg = 'yellow', font = 'verdana 13', relief = 'solid', justify = 'center', bd = 2)

class HeaderLabel(interface.Label):
    def __init__(self,parent = None, **configs):
        interface.Label.__init__(self, parent, **configs)
        self.pack()
        self.config( fg='black', bg='white', font='verdana 20', relief='solid', justify='center', bd=3, width=100 )