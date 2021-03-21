import tkinter as tk
from tkinter.messagebox import showinfo

def add_member(self, attr):
    def add_widget(widgetType, geometry, **kwargs):
        l = geometry.split('/')
        grav = "NEWS" if len(l) == 1 else l[1]
        l = l[0].split(':')
        rowl = l[0].split('+')
        coll = l[1].split('+')
        rowspan = 0 if len(rowl) == 1 else int(rowl[1])
        columnspan = 0 if len(coll) == 1 else int(coll[1])
        rowl = rowl[0].split('.')
        coll = coll[0].split('.')
        row = rowl[0]
        rowweight = 1 if len(rowl) == 1 else int(rowl[1])
        col = coll[0]
        colweight = 1 if len(coll) == 1 else int(coll[1])
        widget = type(widgetType.__name__, tuple([widgetType]), {"__getattr__": add_member})
        setattr(self, attr, widget(self, **kwargs))
        getattr(self, attr).master.rowconfigure(row, weight = rowweight)
        getattr(self, attr).master.columnconfigure(col, weight = colweight)
        getattr(self, attr).grid(row = row, column = col, rowspan = rowspan + 1, columnspan = columnspan + 1, sticky = grav)
    return add_widget

class Application(tk.Frame):
  def __init__(self, master=None, title="<application>"):
    super().__init__(master)
    self.master.title(title)
    self.master.columnconfigure(0, weight=1)
    self.master.rowconfigure(0, weight=1)
    self.grid(sticky="NEWS")
    Application.__getattr__ = add_member
    self.createWidgets()




class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))

app = App(title="Sample application")
app.mainloop()