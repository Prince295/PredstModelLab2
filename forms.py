import tkinter as interface

class Forms(interface.Frame):
    def __init__(self, parent = None, **configs):
        interface.Frame.__init__(self, parent, **configs)
        self.pack()
        self.config( bg = 'white', padx = 0)


class Navs(interface.Frame):
    def __init__(self, parent = None, **configs):
        interface.Frame.__init__(self, parent, **configs)
        self.pack()
        self.config( bg = 'white', padx = 30, pady = 30)




class Container(interface.Frame):
    def __init__(self, parent = None, **configs):
        interface.Frame.__init__(self, parent, **configs)
        self.pack()
        self.config(bg = 'yellow', padx = 30, pady = 30)

class ThemedCanvas(interface.Canvas):
    def __init__(self, parent = None, **configs):
        interface.Canvas.__init__(self, parent, **configs)
        self.pack(expand = True, fill = 'both')
        self.config(width = 525, height = 300, bg = 'grey')

class ThemedText(interface.Text):
    def __init__(self, parent = None, **configs):
        interface.Text.__init__(self, parent, **configs)
        self.pack(expand = True, fill = 'both')
        self.config(bg = '#fce5ff', font = 'verdana 15')


