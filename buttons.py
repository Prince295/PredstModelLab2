import tkinter as interface


class ThemedButton(interface.Button):
    def __init__(self, parent = None, **configs):
        interface.Button.__init__(self, parent, **configs)
        self.pack()
        self.config(fg='black', bg = 'white',width = 10,height = 2, font='courier 10', relief='solid', bd=3)

class ThemedMenu(interface.OptionMenu):
    def __init__(self, parent = None, *values, **configs):
        interface.OptionMenu.__init__(self, parent, *values, **configs)
        self.pack
        self.config( fg='black', bg='white', width=10, height=2, font='courier 10', relief='solid', bd=3 )


