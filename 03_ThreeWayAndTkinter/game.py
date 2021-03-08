import tkinter as tk       
import random

new_order = list(range(15))
random.shuffle(new_order)

class Application(tk.Frame):              
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)    
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)    
        self.spot = {"row" : 4 , "column" : 3}       
        self.createWidgets()

    def new_game(self):
        random.shuffle(new_order)
        self.spot = {"row" : 4 , "column" : 3}  
        for bt in self.bts:
            bt.destroy()
        self.createWidgets()

    def createWidgets(self):
        top=self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)
        self.rowconfigure(4, weight=2)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(1, weight=1)
        self.newButton = tk.Button(self, text = "New", command = self.new_game)
        self.quitButton = tk.Button(self, text='Exit', command = self.quit)      
        self.quitButton.grid(row = 0, column = 2, sticky="NEWS", columnspan = 2)    
        self.newButton.grid(row = 0, column = 0, sticky="NEWS",  columnspan = 2)
        self.bts = [tk.Button(self, text = str(p), command = self.make_move(i)) for i, p in enumerate(new_order)]
        for i, bt in enumerate(self.bts):
            bt.grid(row = i // 4 + 1, column = i % 4, sticky = "NEWS")
    
    def make_move(self, number):
        def move():
            grid_info = self.bts[number].grid_info()
            column = grid_info['column']
            row = grid_info['row']
            if (row == self.spot['row'] and (column == self.spot['column'] - 1 or column == self.spot['column'] + 1)) :
                self.bts[number].grid(row = self.spot['row'], column = self.spot['column'])
                self.spot['column'] = column
            elif (column == self.spot['column'] and (row == self.spot['row'] - 1 or row == self.spot['row'] + 1)) :
                self.bts[number].grid(row = self.spot['row'], column = self.spot['column'])
                self.spot['row'] = row
        return move
    

app = Application()                       
app.master.title('Sample application')    
app.mainloop()        