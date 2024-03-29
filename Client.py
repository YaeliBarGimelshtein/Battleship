import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import json
import Ship
import socket
import sys
import os
from datetime import datetime
from Constants import ADDRESS, GET_BOARD_MESSAGE, GET_TURN_MESSAGE, PID_MESSAGE, FORMAT, HEADER, TRY_HIT_MESSAGE, \
    WAIT_TURN_MESSAGE, RESULT_HIT_MESSAGE, GAME_OVER, DISCONNECT_MESSAGE


class client_window(tk.Tk):
    """
    client_window represents a client with it's screen and data
    """

    def __init__(self):
        """
        init of a client
        """
        super().__init__()

        # client information
        self.args = sys.argv
        if len(self.args) == 1:
            print("No names given, can't run client")
            raise SystemExit
        self.my_name = self.args[1]
        self.opponent_name = self.args[2]
        self.log = open(self.my_name + "_log.txt", "a")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ships = []
        self.game_over = False
        self.ships_indexes, self.turn = self.connect_to_server()
        self.ships = self.create_ships()
        self.send_pid()

        # client gui
        self.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.attributes("-topmost", True)

        self.title('Battleship')
        self.resizable(True, True)
        self.window_size = self.set_geometry()
        self.geometry('%dx%d+%d+%d' % self.window_size)
        self.font = Font(family='Arial', size=14, weight='normal')
        self.configure(bg='black')
        self.instructions = StringVar()
        self.instructions.set("make a move by selecting a ship location")
        self.create_columns_rows()
        self.instructions_label = self.create_Labels(self.my_name, self.opponent_name)
        self.opponent_buttons, self.my_buttons = self.create_buttons()
        self.wait_visibility(self)
        if not self.turn:
            self.withdraw()
            self.wait_for_move()

    def set_geometry(self):
        """
        gets screen size and set location of window in the screen
        :return: width, height of screen and where the window needs to start
        """
        width = 1000
        height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        return width, height, x, y

    def create_columns_rows(self):
        """
        configures rows and columns into the client's window
        :return: void
        """
        for column in range(35):
            self.columnconfigure(column, weight=2)
        for row in range(20):
            self.rowconfigure(row, weight=1)

    def create_Labels(self, player_1, player_2):
        """
        creates and grids players names and instruction onto the screen
        :param player_1: first player name
        :param player_2: second player name
        :return: instructions label
        """
        # Player One
        Player_One_label = ttk.Label(self, text="Your Grid (" + player_1 + ")", font=self.font,
                                     foreground="white", background="black")
        Player_One_label.grid(column=7, row=16, sticky=tk.W, padx=5, pady=5, columnspan=10)

        # Player Two
        Player_Two_label = ttk.Label(self, text=player_2 + "'s Grid", font=self.font,
                                     foreground="white", background="black")
        Player_Two_label.grid(column=23, row=16, sticky=tk.W, padx=5, pady=5, columnspan=10)

        # instructions
        instructions = ttk.Label(self, textvariable=self.instructions, font=self.font, foreground="black",
                                 background="white")
        instructions.grid(column=1, row=18, sticky=tk.W, padx=5, pady=5, columnspan=30)
        return instructions

    def get_button_color(self, row, column):
        """
        calculates the color the square grid should be, blue if there's a ship in that location
        :param row: row of square in the grid
        :param column: column of square in the grid
        :return:
        """
        for ship in self.ships:
            if (row, column) in ship.indexes:
                return "blue"
        return "white"

    def create_buttons(self):
        """
        creates and grids buttons as player's board
        :return: 2 arrays of buttons that represent players grids
        """
        opponent_buttons = []
        my_buttons = []
        for row in range(5, 15, 1):
            my_buttons.append([])
            for column in range(5, 15, 1):
                color = self.get_button_color(row - 5, column - 5)
                button = Button(self, width=2, height=1, bg=color, state="disable")
                button.grid(column=column, row=row)
                my_buttons[row - 5].append(button)

        for row in range(5, 15, 1):
            opponent_buttons.append([])
            for column in range(20, 30, 1):
                button = Button(self, width=2, height=1,
                                command=lambda x=row - 5, y=column - 20: self.make_move(x, y),
                                bg="white")
                button.grid(column=column, row=row)
                opponent_buttons[row - 5].append(button)

        return opponent_buttons, my_buttons

    def connect_to_server(self):
        """
        Initialize connection to server, get location of battleships and turn
        :return: battleships locations, turn
        """
        try:
            self.socket.connect(ADDRESS)
            return self.send_and_receive(GET_BOARD_MESSAGE), self.send_and_receive(GET_TURN_MESSAGE)
        except ConnectionRefusedError:
            print("No server, can't run client without a server")
            raise SystemExit

    def send_pid(self):
        """
        sends the process id to server
        :return: void
        """
        pid = os.getpid()
        self.send_and_receive(PID_MESSAGE)
        self.send_and_receive(pid)

    def send_and_receive(self, obj):
        """
        sends a message to the server through the socket and waits for a return object
        :param obj: an object message to send to the server
        :return: the object received from the server
        """
        try:
            obj_json = json.dumps(obj)
            msg_lenght = len(obj_json)
            obj_json = obj_json.encode(FORMAT)
            send_lenght = str(msg_lenght).encode(FORMAT)
            send_lenght += b' ' * (HEADER - len(send_lenght))  # pad to 64 bytes
            self.write_to_log("sent " + str(obj))
            self.socket.send(send_lenght)
            self.socket.send(obj_json)
            msg_lenght = self.socket.recv(HEADER).decode(FORMAT)
            if msg_lenght:  # check not none
                msg_lenght = int(msg_lenght)
                msg = self.socket.recv(msg_lenght).decode(FORMAT)
                object_from_server = json.loads(msg)
                self.write_to_log("got message: " + str(object_from_server))
                return object_from_server
        except ConnectionResetError:
            self.write_to_log("got ConnectionResetError")
            self.log.close()
            self.destroy()

    def update_colors_for_opponent_grid(self, indexes, row, column):
        """
        fills squares of the opponent grid with black if missed or red if hit
        :param indexes: list of tuples that represent hit places [(x,y),..]
        :param row: row  hit
        :param column: column  hit
        :return: void
        """
        if len(indexes) != 0:
            for index in indexes:
                self.opponent_buttons[index[0]][index[1]].configure(bg='red', state="disable")
        else:
            self.opponent_buttons[row][column].configure(bg='black', state="disable")

    def update_colors_for_my_grid(self, indexes, row, column):
        """
        fills squares of the my grid with x if missed or red if hit
        :param indexes: list of tuples that represent hit places [(x,y),..]
        :param row: row opponent hit
        :param column: column opponent hit
        :return: void
        """
        if len(indexes) != 0:
            for index in indexes:
                self.my_buttons[index[0]][index[1]].configure(bg='red')
        else:
            self.my_buttons[row][column].configure(text="X")

    def update_instructions(self, txt):
        """
        updates instruction label with given message
        :param txt: message to update
        :return: void
        """
        self.instructions.set(txt)

    def make_move(self, row, column):
        """
        tries to hit a ship. shows the result on screen.
        :return: void
        """
        self.send_and_receive(TRY_HIT_MESSAGE)
        hit_successful_indexes = self.send_and_receive((row, column))
        self.update_colors_for_opponent_grid(hit_successful_indexes[0], row, column)
        self.update_instructions("wait for your turn")
        self.update()
        time.sleep(1)
        self.game_over = hit_successful_indexes[1]
        if self.game_over:
            self.send_game_over()
            return
        self.turn = False
        self.withdraw()
        self.wait_for_move()

    def check_did_any_ship_hit(self, row, column):
        """
        checks if any ship got hit
        :param row: row hit
        :param column: column hit
        :return: ship if was hit, else None
        """
        for ship in self.ships:
            if ship.is_hit(row, column):
                self.write_to_log("found a ship")
                return ship
        return None

    def wait_for_move(self):
        """
        checks opponent move. shows the result on screen.
        :return: void
        """
        row, column = self.send_and_receive(WAIT_TURN_MESSAGE)
        indexes = self.check_opponent_move(row, column)
        self.write_to_log(str(indexes))
        self.send_and_receive(RESULT_HIT_MESSAGE)
        self.send_and_receive(indexes)
        if self.game_over:
            self.log.close()
            self.destroy()
            return
        self.turn = True
        self.update_instructions("Your turn, select opponent battleship location")
        self.update()
        time.sleep(1)
        self.deiconify()

    def check_opponent_move(self, row, column):
        """
        checks if opponent hit a ship, drown a ship or didn't hit at all
        :param row: row hit
        :param column: column hit
        :return: array of hit indexes [(x,y)..] that could be empty, true of false for game over
        """
        self.write_to_log("started checking the move")
        hit_indexes = []
        ship = self.check_did_any_ship_hit(row, column)
        if ship is not None:
            self.write_to_log("found the ship that was hit")
            ship.hit(row, column)
            is_ship_drown = ship.drown()
            if is_ship_drown:  # dead ship
                self.write_to_log("ship drown")
                self.ships.remove(ship)
                self.write_to_log(str(self.ships))
                if len(self.ships) == 0:
                    self.game_over = True
                    self.write_to_log("no more ships left, game over")
                self.update_colors_for_my_grid(ship.hit_indexes, row, column)
                return ship.hit_indexes, self.game_over
            else:
                self.write_to_log("whole ship did not drown, part was hit")
                hit_indexes.append((row, column))
                self.update_colors_for_my_grid(hit_indexes, row, column)
                return hit_indexes, self.game_over
        else:
            self.update_colors_for_my_grid(hit_indexes, row, column)
            return hit_indexes, self.game_over

    def send_game_over(self):
        """
        sends to server that the game is over and destroys the window
        :return: void
        """
        self.update_instructions("You win!!!")
        self.update()
        self.send_and_receive(GAME_OVER)
        self.destroy()

    def create_ships(self):
        """
        creates ships objects from the indexes array
        :return: array of ships indexes
        """
        ships = []
        for ship_indexes in self.ships_indexes:
            ship = Ship.Ship(ship_indexes[0], ship_indexes[1])
            ships.append(ship)
        return ships

    def write_to_log(self, msg):
        """
        writes to log file
        :param msg: string message to write to log
        :return: void
        """
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        name = "[" + self.my_name + "]"
        self.log.write(dt_string + " " + name + " " + " " + msg + "\n")

    def disable_event(self):
        """
        sends a disconnect message and destroys the window
        :return: void
        """
        if not self.game_over:
            self.write_to_log("disable")
            self.send_and_receive(DISCONNECT_MESSAGE)
            self.log.close()
            self.destroy()


app = client_window()
app.mainloop()
