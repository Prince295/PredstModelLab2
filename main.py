import pickle
import time, sys
import numpy as np
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from labels import *
from forms import *
from buttons import *
from enters import *
from PIL import Image,ImageDraw, ImageTk
import json





helpstr = ""

if sys.platform[:3] == 'win':
    HelpFont = ('courier', 9, 'normal')
else:
    HelpFont = ('courier', 12, 'normal')

pickDelays = [0.01, 0.025, 0.05, 0.15, 0.25, 0.0, 0.001, 0.005]
pickUnits = [1,2,4,6,8,10,12]
pickWidths = [1,2,5,10,20]
pickFills = [None, 'while', 'blue', 'red', 'black', 'yellow', 'green', 'purple']

colors = {"Генеративная" : 'black',
        "Негативная" : 'red',
        "Ситуационная" : 'blue',
        "Финитивная" : 'magenta',
        "Инструментальная" : 'yellow',
        "Коммитативная" : 'green',
        "Каузальная" : 'purple',
        "Корелляционая" : 'grey',
        "Потенсивная" : 'brown'}

meanings = {"Генеративная" : "Является частью",
        "Негативная" : 'Отрицает',
        "Ситуационная" : 'Находится в ситуации',
        "Финитивная" : 'Является целью',
        "Инструментальная" : 'Является инструментом',
        "Коммитативная" : 'Сопровождает',
        "Каузальная" : 'Вызывает',
        "Корелляционая" : 'Может увеличить шансы',
        "Потенсивная" : 'Может вызывать'}

pickPens = ['elastic', 'scribble', 'trails']

saving = {}


vals = {"type" : None,
        "x1" : None,
        "y1" : None,
        "x2" : None,
        "y2" : None,
        "value" : None,}

class MovingPics():
    def __init__(self, parent = None):
        canvas = Canvas(parent, width=800, height=600, bg = 'white')
        menu_form = Navs(parent)
        menu_form.pack(side = 'left', expand = True, fill = 'both')
        canvas.pack(side = 'right', expand = True, fill = 'both')
        button =[None, None, None, None, None, None,None]

        button[0]=ThemedButton(menu_form, text = 'Открыть файл')
        button[1]=ThemedButton(menu_form, text = 'Добавить сущность')
        button[2]=ThemedButton(menu_form, text = 'Посмотреть текстовое описание сети')
        button[3]=ThemedButton(menu_form, text = 'Сохранить связь')
        button[5]=ThemedButton(menu_form, text = 'Сохранить файл')
        button[4]=ThemedButton(menu_form, text = 'Удалить связь')
        button[6]=ThemedButton(menu_form, text = 'Показать/скрыть связи')

        for i in range(len(button)):
            button[i].pack(in_ = menu_form, side = 'top', padx = 10, pady = 10, expand = True, fill = 'both')

        var1 = StringVar()
        opt1 = ThemedMenu(menu_form, var1, "Генеративная", "Негативная", "Ситуационная", "Финитивная",
                                            "Инструментальная", "Коммитативная", "Каузальная", "Корелляционая", "Потенсивная" )
        opt1.pack(in_ = menu_form, side = 'top', padx = 10, pady = 10, expand = True, fill = 'both')

        button[0].config(command = self.loadObject)
        button[1].config(command = self.addWidget)
        button[2].config(command = self.add_text_widget)
        button[3].config(command = self.saveObject)
        button[4].config(command = self.deleteNet)
        button[5].config(command = self.savePostscript)
        button[6].config(command = self.show_hide_text)



        canvas.bind('<Button-1>',   self.onStart)
        canvas.bind('<Button1-Motion>',       self.onGrow)
        canvas.bind('<ButtonPress-3>',       self.onSelect)
        canvas.bind('<Button3-Motion>',      self.onDrag)
        parent.bind('<Shift-F2>',       self.onOptions)
        parent.bind('<Return>', self.changeObject)
        parent.bind('<Delete>', self.deleteObject)
        self.createMethod = Canvas.create_line
        self.canvas = canvas
        self.menu_form = menu_form
        self.opt1 = opt1
        self.moving = []
        self.objects = {}
        self.variables={}
        self.seq = {}
        self.var1 = var1
        self.flag = 0
        self.line ={}
        self.uniq = []

        self.id1 = 0
        self.id2 = 0
        self.id3 = 0

        self.object = None
        self.prev_object = None
        self.where = None
        self.scribbleMode = 0
        parent.title('Семантические сети')
        parent.protocol('WM_DELETE_WINDOW', self.onQuit)
        self.realquit = parent.quit
        # self.textInfo = self.canvas.create_text(5,5, anchor = 'nw', font = HelpFont, text='Press ? for help')


    def add_text_widget(self):
        toplevel = Toplevel()
        text_widget = ThemedText(toplevel)
        text_widget.pack()

        hights = {}
        value = []
        for v in self.variables.values():
            value.append(v)
        for i in range(len(value)):
            value1 = []
            for k in value[i].keys():
                value1.append(k)
            hights[value1[0]] = []
            for j in range(len(value)):
                value2 = []
                for k in value[j].keys():
                    value2.append( k )
                if value1[0] == value2[0]:
                    hights[value1[0]].append(value2[2])
                    hights[value1[0]] = list(set(hights[value1[0]]))

        if self.canvas.type(self.object) == 'window' and self.canvas.type(self.prev_object)=='window':
            begin = self.prev_object
            target = self.object

            path = []
            path1 = []
            previos_targets = []

            def find(dic, target, begin, path, previos_targets):
                stack = []
                for i in range( len( target ) ):
                    for k, v in dic.items():
                        if target[i] in v:
                            if target[i] not in previos_targets:
                                stack.append( k )
                    previos_targets.append( target[i] )
                    if begin in stack:
                        previos_targets = list( set( previos_targets ) )

                        path.append( target[i] )
                        path.append( begin )
                        return path
                path1 = find( dic, stack, begin, path, previos_targets )
                if path1 != None:
                    return path1

            arr = find( hights, [target], begin, path, previos_targets )
            true_path = [arr[1]]
            true_path.append( arr[0] )
            while True:
                if arr[0] in hights[1]:
                    break
                path = []
                path1 = []
                previos_targets = []
                arr = find( hights, [target], arr[0], path, previos_targets )
                true_path.append( arr[0] )

            true_path.append( target )


            for k, v in self.variables.items():
                string = ''
                f = True
                a = 1
                arr1 = []
                index = k
                for key, val in v.items():
                    arr1.append(key)
                    if a % 2 != 0:
                        string += " - {} - ".format( self.objects[key].get() )
                    else:
                        string += " - {} - ".format( self.seq[key] )
                    a += 1
                for i in range(len(true_path)-1):
                    if true_path[i] == arr1[0] and true_path[i+1] == arr1[2]:
                        text_widget.insert( '{}.0'.format( k + 1 ), string + '\n' )
            string ='Путь : '
            for i in range(len(true_path)):
                string += " - {} - ".format( self.objects[true_path[i]].get() )
            text_widget.insert( '{}.0'.format( index + 2 ), string + '\n' )

    def loadObject(self):
        self.canvas.delete('all')
        self.uniq = []
        self.variables={}
        self.objects={}
        # self.canvas.create_text( 5, 5, anchor='nw', font=HelpFont, text='Press ? for help' )
        f1 = open( 'temp', 'rb' )
        saving = pickle.load( f1 )
        f1.close()

        for key, val in saving.items():

                    if val['type'] == 'window':
                        var = StringVar()
                        text = ThemedMessage( self.canvas, bd=1, bg='yellow', width=10 )
                        text.config( state='disabled', textvariable=var )
                        var.set(val['value'])
                        self.object = self.canvas.create_window( val['x1'],
                                                                 val['y1'],
                                                                 window=text
                                                                 )
                        self.objects[self.object] = text
        for key, val in saving.items():
            if val['type'] == 'line':
                self.canvas.create_line( int( val['x1'] ),
                                         int( val['y1'] ), int( val['x2'] ),
                                         int( val['y2'] ), fill=colors[val['value']], width=pickWidths[0], arrow='last' )
                self.id1 = self.canvas.find_overlapping( val['x1'] - 10, val['y1'] - 10, val['x1'] + 10,
                                                         val['y1'] + 10 )[0]
                self.id2 = self.canvas.find_overlapping( val['x2'] - 2, val['y2'] - 2, val['x2'] + 2, val['y2'] + 2 )[0]
                self.id3 = self.canvas.find_overlapping( val['x2'] - 2, val['y2'] - 2, val['x2'] + 2, val['y2'] + 2 )[1]
                self.objects[self.canvas.find_all()[len( self.canvas.find_all() ) - 1]] = self.object
                self.line[self.id3] = val['value']
                self.seq[self.id3] = meanings[val['value']]
                if val['net']:
                    self.variables[val['net']] = {self.id1: self.objects[self.id1].get(),
                                                  self.id3: self.seq[self.id3],
                                                  self.id2: self.objects[self.id2].get()
                                                  }
                    x1, y1, x2, y2 = self.canvas.coords( self.id3 )
                    self.canvas.create_text( (x1 + x2) / 2, (y1 + y2) / 2, text=self.seq[self.id3] )

                if val['net'] > self.flag:
                    self.flag = val['net']

        self.flag+=1
        saving.clear()


    def show_hide_text(self):
        arr = self.canvas.find_all()
        for i in range(len(arr)):
            if self.canvas.type(arr[i]) == 'text':
                config=self.canvas.itemconfig(arr[i])['fill']
                if config[len(config)-1] == 'black':
                     self.canvas.itemconfig(arr[i], fill = 'white')
                else:
                     self.canvas.itemconfig( arr[i],fill ='black')


    def deleteNet(self):
        temp = None
        if self.object:
            if self.canvas.type(self.object) == 'line':
                self.canvas.delete(self.object)
                self.objects.pop(self.object)
                for key, val in self.variables.items():
                    for k in val.keys():
                        if k == self.object:
                            temp = key
                self.variables.pop(temp)

    def saveObject(self):
        if self.id1 and self.id2 and self.id3:
            self.uniq.append( "{}:{}:{}".format( self.id1, self.id2, self.id3 ) )
            setuniq = set( self.uniq )
            if len( setuniq ) == len( self.uniq ):
                self.variables[self.flag] = {self.id1 : self.objects[self.id1].get(),
                                    self.id3 : self.seq[self.id3],
                                    self.id2 : self.objects[self.id2].get()}
                x1,y1,x2,y2 = self.canvas.coords(self.id3)
                self.canvas.create_text( (x1+x2)/2, (y1+y2)/2, text = self.seq[self.id3])

                self.flag += 1

    def onStart(self,event):
        self.where = event
        self.object = None

    def onGrow(self,event):
        canvas = event.widget


        if self.object and pickPens[0] == 'elastic':
            canvas.delete(self.object)

        self.id1 = self.canvas.find_overlapping( self.where.x-10, self.where.y-10, self.where.x + 10, self.where.y + 10 )[0]
        self.object = self.createMethod(canvas, self.where.x,
                                        self.where.y, event.x,
                                        event.y, fill=colors[self.var1.get()], width=pickWidths[0],arrow = 'last')
        self.objects[self.object] = self.canvas.type( self.object )
        self.id2 = self.canvas.find_overlapping(event.x-2, event.y-2,event.x+2, event.y+2)[0]
        self.id3 = self.canvas.find_overlapping(event.x-2, event.y-2,event.x+2, event.y+2)[1]
        self.objects[self.canvas.find_all()[len( self.canvas.find_all() ) - 1]] = self.object

        self.line[self.id3] = self.var1.get()
        self.seq[self.id3] = meanings[self.var1.get()]


        if pickPens[0] == 'scribble':
            self.where = event

    def onClear(self, event):
        if self.moving:
            return
        event.widget.delete('all')
        self.objects = []
        self.variables = []
        self.textInfo = self.canvas.create_text(5, 5, anchor = 'nw',
                                                font = HelpFont,
                                                text='Press ? for help')

    def plotMoves(self, event):
        diffX = event.x - self.where.x
        diffY = event.y - self.where.y
        reptX = np.abs(diffX) // pickUnits[0]
        reptY = np.abs(diffY) // pickUnits[0]
        incrX = pickUnits[0]*((diffX > 0) or -1)
        incrY = pickUnits[0]*((diffY > 0) or -1)
        return incrX, reptX, incrY, reptY



    def onSelect(self, event):
        self.where = event
        self.prev_object = self.object
        self.object = self.canvas.find_closest(event.x, event.y)[0]


    def onDrag(self, event):
        diffX = event.x - self.where.x
        diffY = event.y - self.where.y
        self.canvas.move(self.object, diffX, diffY)
        self.where = event

    def onOptions(self, event):
        keymap = {


            'd' : MovingPics.deleteObject,
            '1' : MovingPics.raiseObject,
            '2' : MovingPics.lowerObject,
            'f' : MovingPics.changeObject,
            'b' : MovingPics.fillBackground,
            'p' : MovingPics.addWidget

        }
        try:
            keymap[event.char](self)
        except KeyError:
            self.setTextInfo('Press ? for help')



    def changeOption(self, list, name):
        list.append(list[0])
        del list[0]
        self.setTextInfo('{}={}'.format(name, list[0]))

    def deleteObject(self,event):
        canvas = event.widget
        self.canvas.delete(self.object)
        self.objects.pop(self.object)
        self.object = None


    def changeObject(self, event):
        canvas = event.widget
        if self.object:

            type = self.canvas.type(self.object)
            x, y = self.canvas.coords(self.object)


            if self.objects[self.object]['state'] == 'normal':
                prev = self.object
                self.objects[self.object].config( state='disabled', bg='yellow' )
                self.objects[self.canvas.find_all()[len( self.canvas.find_all() ) - 1] + 1 ] = self.objects[self.object]

                self.canvas.create_window( int( x ), int( y ), window=self.objects[self.object] )
                self.canvas.delete( prev )
                self.object = self.canvas.find_all()[len(self.canvas.find_all())- 1]
                return
            if self.objects[self.object]['state'] == 'disabled':
                prev = self.object
                self.objects[self.object].config(state = 'normal', bg ='white')
                self.objects[self.canvas.find_all()[len( self.canvas.find_all() ) - 1] + 1] = self.objects[self.object]

                self.canvas.create_window( int( x ), int( y ), window=self.objects[self.object] )
                self.canvas.delete( prev )
                self.object = self.canvas.find_all() [len( self.canvas.find_all() ) - 1 ]
                return






    def fillBackground(self):
        self.canvas.config(bg=pickFills[0])

    def addWidget(self):
        if self.where:
            var = StringVar()
            text = ThemedMessage(self.canvas, bd = 1, bg = 'yellow', width = 10)
            text.config(state = 'disabled', textvariable = var)

            var.set('Enter here')
            self.object = self.canvas.create_window(self.where.x,
                                                       self.where.y,
                                                    window = text
                                                       )
            self.objects[self.object] = text

    def savePostscript(self):
        hui = self.canvas.find_all()
        for i in hui:
            get_flag = None
            type = self.canvas.type(i)
            if type == 'line':
                x1,y1,x2,y2 = self.canvas.coords(i)
                value = self.line[i]
                for key, val in self.variables.items():
                    if i in val.keys():
                        get_flag = key
                saving[i] = {"type": type,
                             "x1": x1,
                             "y1": y1,
                             "x2": x2,
                             "y2": y2,
                             "value": value,
                             "net" : get_flag
                             }
            if type == 'window':
                for key, val in self.variables.items():
                    if i in val.keys():
                        get_flag = key
                x1, y1 = self.canvas.coords(i)
                x2, y2 = (None, None)
                value = self.objects[i].get()
                saving[i] = {"type" : type,
                            "x1" : x1,
                            "y1" : y1,
                            "x2" : x2,
                            "y2" : y2,
                            "value" : value,
                            "net" : get_flag
                             }
        f1 = open('temp','wb')
        pickle.dump(saving, f1 )
        f1.close()
        saving.clear()



    def help(self):
        self.setTextInfo(helpstr)

    def setTextInfo(self, text):
        self.canvas.dchars(self.textInfo, 0, END)
        self.canvas.insert(self.textInfo, 0 , text)
        self.canvas.tkraise(self.textInfo)

    def onQuit(self):
        if self.moving:
            self.setTextInfo("Cannot quit while move in progress")
        else:
            self.realquit()



    def traceEvent(label, event, fullTrace=True):
        print( label )
        if fullTrace:
            for attr in dir( event ):
                if attr[:2] != '__':
                    print( attr, '=>', getattr( event, attr ) )


if __name__ == '__main__':
    from sys import argv

    root = Tk()
    root.geometry( "1100x600+200+100" )
    MovingPics( root )

    root.mainloop()





