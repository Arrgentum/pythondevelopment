import tkinter as tk
from tkinter import messagebox
import random

PADDING = 5
CARRY = 4
BUTTON_WIDTH = 6
BUTTON_HEIGHT = 3

class Application(tk.Tk):
    def __init__(self, master=None):
        tk.Tk.__init__(self, master)
        self.buttons = []
        self.game_list = []
        self.game_frame = tk.Frame(self)
        self.buttons_frame = tk.Frame(self)
        self.new_game()

    def win(self):
        for i in range(CARRY * CARRY - 1):
            if self.game_list[i] != i + 1:
                return False
        messagebox.showinfo("tag games", "You won!")
        self.quit()

    def clear(self):
        for button in self.buttons:
            button.destroy()

    def is_game_correct(self):
        list1 = [0 for i in range(CARRY * CARRY)]
        e = 0
        for i in range(CARRY * CARRY):
            if self.game_list[i] == 0:
                e = i // CARRY + 1
            else:
                k = 0
                for j in range(i, CARRY * CARRY):
                    if self.game_list[j] < self.game_list[i] and self.game_list[j] != 0:
                        k += 1
                list1[self.game_list[i]] = k
        N_sum = sum(list1) + e
        return N_sum % 2 == 0

    def new_game(self):
        self.game_list = [i for i in range(CARRY * CARRY)]
        random.shuffle(self.game_list)
        while not self.is_game_correct():
            random.shuffle(self.game_list)
        self.clear()
        self.creat_game()

    def move_button(this, id):
        def new(self=this, idx=id):
            right_button = idx + 1 if idx % CARRY != CARRY - 1 else None
            left_button = idx - 1 if idx % CARRY != 0 else None
            top_button = ((idx // CARRY) - 1) * CARRY + (idx % CARRY) if idx // CARRY != 0 else None
            bot_button = ((idx // CARRY) + 1) * CARRY + (idx % CARRY) if idx // CARRY != CARRY - 1 else None
            sides = [right_button, left_button, top_button, bot_button]
            for side in sides:
                if side is not None and self.game_list[side] == 0:
                    self.game_list[side] = self.game_list[idx]
                    self.game_list[idx] = 0
                    self.clear()
                    self.creat_game()
                    self.win()
                    return
        return new

    def creat_game(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.buttons_frame.grid(row=0, column=0, sticky='NSEW')
        new_button = tk.Button(self.buttons_frame, text='New game', command=self.new_game)
        exit_button = tk.Button(self.buttons_frame, text='Exit game', command=self.quit)

        self.buttons_frame.grid_rowconfigure(0, weight=1, pad=PADDING)
        self.buttons_frame.grid_columnconfigure(0, weight=1, pad=PADDING)
        self.buttons_frame.grid_columnconfigure(1, weight=1, pad=PADDING)
        new_button.grid(column=0, row=0, sticky='NSEW')
        exit_button.grid(column=1, row=0, sticky='NSEW')

        self.game_frame.grid(row=1, column=0, columnspan=4, sticky='NSEW')

        for j in [1,2]:
            for i in range(CARRY):
                self.game_frame.grid_columnconfigure(i, weight=1, pad=PADDING)

        self.buttons = []
        for i in range(CARRY * CARRY):
            if self.game_list[i] != 0:
                self.buttons.append( tk.Button(self.game_frame,text=f'{self.game_list[i]}', width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.move_button(i) ) )
                self.buttons[-1].grid(row=i // CARRY, column=i % CARRY, sticky='NSEW')


app = Application()
app.title('tag games')
app.mainloop()