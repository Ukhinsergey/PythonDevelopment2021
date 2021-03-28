import tkinter as tk
import random
import sys



class TextField(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tag_configure('error', background='red')
        self.bind('<<Modified>>', self.update_text_field)

    def update_text_field(self, args):
        self.tag_remove('error', '1.0', 'end')

        self.master.canvas.delete('all')
        full_text = self.get("1.0", "end").split('\n')[:-1]
        currentline = 1
        for i, line in enumerate(full_text):
            try:
                o = Oval(line)
                self.master.canvas.DrowFromText(o, i + 1)
                currentline += 1
            except:
                self.tag_add('error', '%d.0' % (i+1), '%d.end' % (i+1))
        
        self.edit_modified(False)

    def UpdateStr(self, line, o):
        line = str(line)
        self.delete(line+'.0', line+'.end')
        self.insert(line+'.0', str(o))

    def AddNewLine(self):
        self.insert(tk.END, '\n')



class Oval():
    def __init__(self, str):
        self.str = str
        l = str.split('.')
        if len(l) > 7 :
            raise ValueError
        self.x1 = int(l[0])
        self.y1 = int(l[1])
        self.x2 = int(l[2])
        self.y2 = int(l[3])
        self.width = int(l[4])
        self.fill = l[5]
        self.outline = l[6]

    def __str__(self):
        return self.str


class CanvasField(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Button-1>', self.click)
        self.bind('<ButtonRelease-1>', self.release)
        self.bind('<Motion>', self.CheckMotion)
        self.drawingOval = False
        self.moving = False
        self.width = 3
        self.outline = "#ffffff000"
        self.fill = "#000fff000"
        self.ovals = {}
        self.dx = 0
        self.dy = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.currentlinenumber = 1

    def CheckMotion(self, event):
        if self.drawingOval:
            self.delete(self.current_drawing)
            self.x2 = event.x
            self.y2 = event.y
            self.current_drawing = self.create_oval(self.x1 + self.dx, self.y1 + self.dy, self.x2 + self.dx, self.y2 + self.dy, fill = self.fill, width = self.width, outline = self.outline, tag = self.currentlinenumber)
            o = Oval(self.formOvalString(self.x1 + self.dx, self.y1 + self.dy, self.x2 + self.dx, self.y2 + self.dy, self.width, self.fill, self.outline))
            self.master.text.UpdateStr(self.currentlinenumber, o)
        elif self.moving:
            self.delete(self.current_drawing)
            self.dx = event.x - self.oldx
            self.dy = event.y - self.oldy
            self.current_drawing = self.create_oval(self.x1 + self.dx, self.y1 + self.dy, self.x2 + self.dx, self.y2 + self.dy, fill = self.fill, width = self.width, outline = self.outline, tag = self.currentlinenumber)
            o = Oval(self.formOvalString(self.x1 + self.dx, self.y1 + self.dy, self.x2 + self.dx, self.y2 + self.dy, self.width, self.fill, self.outline))
            self.master.text.UpdateStr(self.currentlinenumber, o)

    def click(self, event):
        l = self.find_overlapping(event.x, event.y, event.x, event.y)
        if len(l) == 0:
            self.beginOval(event)
        else :
            self.moving = True
            self.oldx = event.x
            self.oldy = event.y
            self.current_drawing = l[-1]
            self.currentlinenumber = self.gettags(self.current_drawing)[0]
            self.x1 = self.ovals[self.current_drawing].x1
            self.x2 = self.ovals[self.current_drawing].x2
            self.y1 = self.ovals[self.current_drawing].y1
            self.y2 = self.ovals[self.current_drawing].y2
            self.fill = self.ovals[self.current_drawing].fill
            self.outline  = self.ovals[self.current_drawing].outline
            self.width = self.ovals[self.current_drawing].width
            del self.ovals[self.current_drawing]

    def release(self, event):
        self.endOval(event)


    def beginOval(self, event):
        self.currentlinenumber = max(len(self.master.text.get("1.0", "end").split('\n')) - 1, 1)
        self.dx = 0
        self.dy = 0
        self.x1 = event.x
        self.y1 = event.y
        self.x2 = event.x
        self.y2 = event.y
        self.current_drawing=self.create_oval(self.x1 + self.dx, self.y1 + self.dy, self.x2 + self.dx, self.y2 + self.dy, fill = self.fill, width = self.width, outline = self.outline, tag = self.currentlinenumber)
        o = Oval(self.formOvalString(self.x1 + self.dx, self.y1 + self.dy, self.x2 + self.dx, self.y2 + self.dy, self.width, self.fill, self.outline))
        self.master.text.UpdateStr(self.currentlinenumber, o)
        self.drawingOval = True

    def formOvalString(self, *args):
        s = ""
        for i in args[:-2]:
            s += str(i) + '.'
        s += args[-2] + '.'
        s += args[-1]
        return s

    def endOval(self, event):
        self.delete(self.current_drawing)
        id = self.create_oval(self.x1 + self.dx, self.y1 + self.dy, self.x2 + self.dx, self.y2 + self.dy, fill = self.fill, width = self.width, outline = self.outline, tag = self.currentlinenumber)
        self.ovals[id] = Oval(self.formOvalString(self.x1 + self.dx, self.y1 + self.dy, self.x2 + self.dx, self.y2 + self.dy, self.width, self.fill, self.outline))
        o = Oval(self.formOvalString(self.x1 + self.dx, self.y1 + self.dy, self.x2 + self.dx, self.y2 + self.dy, self.width, self.fill, self.outline))
        self.master.text.UpdateStr(self.currentlinenumber, o)
        if self.drawingOval:
            self.master.text.AddNewLine()
        self.drawingOval = False
        self.moving = False

    def DrowFromText(self, o, currentline):
        id = self.create_oval(o.x1, o.y1, o.x2, o.y2, fill = o.fill, width = o.width, outline = o.outline, tag = currentline)
        self.ovals[id] = o


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.text = TextField(self)
        self.text.grid(row=0, column=0, sticky="news")

        self.canvas = CanvasField(self)
        self.canvas.grid(row=0, column=1, sticky="news")

app = Application()
app.mainloop()