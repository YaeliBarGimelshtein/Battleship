import subprocess
import tkinter as tk
from tkinter import ttk


class first_window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("300x100")
        self.title('Start Game')
        self.resizable(0, 0)
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.disable_event)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # names
        self.player_1_name = tk.StringVar()
        self.player_2_name = tk.StringVar()

        # Error label
        self.error = tk.StringVar()
        self.error_label = ttk.Label(self, textvariable=self.error, foreground="red",)
        self.error_label.grid(column=0, row=3, sticky=tk.E, padx=5, pady=5)
        self.create_widgets()

    def create_widgets(self):
        """
        creates all widgets of the window
        :return: void
        """
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
                                  command=lambda: self.check_and_pass(Player_One_entry, Player_Two_entry))
        login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

    def check_and_pass(self, player_one_entry, player_two_entry):
        """
        checks if names are not empty
        :param player_one_entry: entry of first name
        :param player_two_entry: entry of second name
        :return: names of players, if names not empty
        """
        player_one_name = player_one_entry.get()
        player_two_name = player_two_entry.get()
        if len(player_one_name) == 0 or len(player_two_name) == 0:
            self.error.set("At least one character needed")
            self.update()
        elif player_one_name == player_two_name:
            self.error.set("Cant have same name")
            self.update()
        else:
            self.player_1_name = player_one_name
            self.player_2_name = player_two_name
            self.destroy()

    def get_player_1_name(self):
        """
        get name of first player
        :return: name
        """
        return self.player_1_name

    def get_player_2_name(self):
        """
        get name of second player
        :return: name
        """
        return self.player_2_name

    def disable_event(self):
        raise SystemExit


class Last_window(tk.Tk):
    def __init__(self, winner_name, server,port):
        super().__init__()

        self.geometry("240x100")
        self.title('Game Ended')
        self.resizable(0, 0)
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.disable_event)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.winner_name = winner_name
        self.server = server
        self.port_to_send = port
        self.create_widgets(self.winner_name)
        self.deiconify()

    def create_widgets(self, winner_name):
        """
        creates all widgets of the window
        :return: void
        """
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
        self.server.restart(self.port_to_send)

    def disable_event(self):
        raise SystemExit
