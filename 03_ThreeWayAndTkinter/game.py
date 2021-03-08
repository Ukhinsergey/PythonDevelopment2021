import tkinter as tk       
import random

from tkinter import messagebox

new_order = list(range(15))
random.shuffle(new_order)

class Application(tk.Frame):    

                  
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)    
        self.check_order()
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)    
        self.spot = {"row" : 4 , "column" : 3}       
        self.createWidgets()

    def new_game(self):
        random.shuffle(new_order)
        self.check_order()
        self.spot = {"row" : 4 , "column" : 3}  
        for bt in self.bts:
            bt.destroy()
        self.createWidgets()


    def check_order(self):
        count = 0
        for i in range(0, len(new_order)):
            for j in range(i, len(new_order)):
                if new_order[i] > new_order[j]:
                    count += 1
        if count % 2 == 1:
            new_order[0], new_order[1] = new_order[1], new_order[0]

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
                if self.check_win():
                    messagebox.showinfo('15', 'You won!')
                    self.new_game()
            elif (column == self.spot['column'] and (row == self.spot['row'] - 1 or row == self.spot['row'] + 1)) :
                self.bts[number].grid(row = self.spot['row'], column = self.spot['column'])
                self.spot['row'] = row
                if self.check_win():
                    messagebox.showinfo('15', 'You won!')
                    self.new_game()
        return move

    def check_win(self):
        for i, bt in enumerate(self.bts):
            info = bt.grid_info()
            col = info['column']
            row = info['row']
            if col != new_order[i] % 4 or row != new_order[i] // 4 + 1:
                return False
        return True


app = Application()                       
app.master.title('15')    
app.mainloop()        