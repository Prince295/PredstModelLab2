import tkinter as interface

class ThemedMessage(interface.Entry):
    def __init__(self, parent = None, **configs):
        interface.Entry.__init__(self, parent, **configs)
        self.pack()
        self.config(fg='black', bg = 'white', font = 'times 10', relief='solid', justify = 'center', width = 15, disabledbackground='#fce5ff' , disabledforeground='black')
