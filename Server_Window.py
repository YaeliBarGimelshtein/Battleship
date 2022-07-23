import tkinter as tk
from tkinter import ttk


def check_and_pass(player_one_entry, player_two_entry, application):
    print("finished adding names")
    player_one_name = player_one_entry.get()
    player_two_name = player_two_entry.get()
    if len(player_one_name) != 0 and len(player_two_name) != 0:
        application.destroy()


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
                                  command=lambda: check_and_pass(Player_One_entry, Player_Two_entry, self))
        login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)


class Last_window(tk.Tk):
    def __init__(self, winner_name):
        super().__init__()

        self.geometry("240x100")
        self.title('Game Ended')
        self.resizable(0, 0)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.winner_name = winner_name
        self.create_widgets(self.winner_name)

    def create_widgets(self, winner_name):
        # Winner is
        winner_is_label = ttk.Label(self, text="The winner is:")
        winner_is_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # Winner name
        winner_name_label = ttk.Label(self, text=winner_name)
        winner_name_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        # play again button
        replay_button = ttk.Button(self, text="Play Again", command=lambda: self.replay())
        replay_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

    def replay(self):
        self.destroy()
        app_2 = first_window()
        app_2.mainloop()


# app = first_window()
# app.mainloop()
app = Last_window("Ran Sasson")
app.mainloop()
