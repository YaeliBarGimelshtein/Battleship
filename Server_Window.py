import tkinter as tk
from tkinter import ttk


def check_and_pass(player_one_entry, player_two_entry):
    print("finished adding names")
    player_one_name = player_one_entry.get()
    player_two_name = player_two_entry.get()
    if len(player_one_name) != 0 and len(player_two_name) != 0:
        app.destroy()


class first_window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("240x100")
        self.title('Start Game')
        self.resizable(0, 0)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.create_widgets()

    def create_widgets(self):
        # Player One
        Player_One_label = ttk.Label(self, text="Player One:")
        Player_One_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        Player_One_entry = ttk.Entry(self)
        Player_One_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        # Player Two
        Player_Two_label = ttk.Label(self, text="Player Two:")
        Player_Two_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        Player_Two_entry = ttk.Entry(self)
        Player_Two_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # start button
        login_button = ttk.Button(self, text="Start",
                                  command=lambda: check_and_pass(Player_One_entry, Player_Two_entry))
        login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)


app = first_window()
app.mainloop()
