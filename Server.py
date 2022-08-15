import json
import socket
import threading
import random
import os
from Server_Window import first_window
from Server_Window import Last_window
import subprocess
from datetime import datetime

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
HEADER = 64  # each message will have a header to tell the message size
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # when receiving, close the connection and disconnect client
GET_BOARD_MESSAGE = "GET_BOARD"
GET_TURN_MESSAGE = "GET_TURN"
TRY_HIT_MESSAGE = "TRY_HIT"
PID_MESSAGE = "PID"
RESULT_HIT_MESSAGE = "RESULT_HIT"
GAME_OVER = "GAME_OVER"
XL_SHIP = 4
L_SHIP = 3
M_SHIP = 2
S_SHIP = 1


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class Server:

    def __init__(self):
        self.log = open("Server_log.txt", "w")
        self.write_to_log("[STARTING] server is starting...")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDRESS)
        self.board_size = 10
        self.player1_board = [[]]
        self.player1_ships = []
        self.ships_sizes = [XL_SHIP, L_SHIP, L_SHIP, M_SHIP, M_SHIP, M_SHIP, S_SHIP, S_SHIP, S_SHIP, S_SHIP]
        self.client = "Client.py"
        self.player_1_name = ""
        self.player_2_name = ""
        self.player_1_turn = True
        self.player_2_turn = False
        self.asked_for_turn_first_time = False
        self.player1_pid = 0
        self.player2_pid = 0

    def handle_client(self, port, ip):
        """
        handle individual connection between one client and the server
        :param port: client's port number of the connection
        :param ip: client's ip address
        :return: void
        """
        try:
            self.write_to_log(f"[NEW CONNECTION] {ip} connected.")
            connected = True
            while connected:
                msg_lenght = port.recv(HEADER).decode(
                    FORMAT)  # blocks until receiving a message and convert it from bytes
                if msg_lenght:  # check not none
                    connected = self.receive_massage(msg_lenght, port)

            port.close()
            self.log.close()
        except ConnectionAbortedError:
            # self.write_to_log("connection was canceled")
            self.log.close()
            raise SystemExit

    def receive_massage(self, size, port):
        msg_lenght = int(size)
        msg = port.recv(msg_lenght).decode(FORMAT)
        msg = json.loads(msg)
        if msg == DISCONNECT_MESSAGE:
            send_Massage("ACK", port)
            self.disconnect_and_quit(port)
            return False
        elif msg == GET_BOARD_MESSAGE:
            self.generate_and_send_board_for_client(port)
        elif msg == GET_TURN_MESSAGE:
            self.generate_and_send_turn_for_client(port)
        elif msg == TRY_HIT_MESSAGE or msg == RESULT_HIT_MESSAGE:
            send_Massage("ACK", port)
            self.pass_msg(port, msg)
        elif msg == GAME_OVER:
            send_Massage("ACK", port)
            self.game_over()
        elif msg == PID_MESSAGE:
            send_Massage("ACK", port)
            self.get_process_id(port)
        return True

    def start(self):
        get_names_window = first_window()
        get_names_window.mainloop()
        self.player_1_name = get_names_window.get_player_1_name()
        self.player_2_name = get_names_window.get_player_2_name()

        self.server.listen()
        self.write_to_log(f"[LISTENING] Server is listening on {SERVER}")

        client_1_thread = threading.Thread(target=self.start_client, args=(self.player_1_name, self.player_2_name))
        client_1_thread.start()
        self.player1_port, ip = self.server.accept()  # blocks. waits for new connection to the server
        thread = threading.Thread(target=self.handle_client, args=(self.player1_port, ip))
        thread.start()

        client_2_thread = threading.Thread(target=self.start_client, args=(self.player_2_name, self.player_1_name))
        client_2_thread.start()
        self.player2_port, ip = self.server.accept()  # blocks. waits for new connection to the server
        thread = threading.Thread(target=self.handle_client, args=(self.player2_port, ip))
        thread.start()
        self.write_to_log(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 3}")

    def create_battleground(self):
        self.player1_board = None
        self.player1_ships.clear()
        self.player1_board = self.init_board()
        for size in self.ships_sizes:
            self.add_ship_to_board(size, self.player1_board, self.player1_ships)
        self.write_to_log(str(self.player1_ships))
        self.write_to_log(str(len(self.player1_ships)))
        return self.player1_ships

    def get_random_location(self):
        x = random.randint(0, self.board_size - 1)
        y = random.randint(0, self.board_size - 1)
        return x, y

    def add_ship_to_board(self, size, board, ships):
        done = False
        while not done:
            location = self.get_random_location()
            done = self.try_place_ship(location, size, board, ships)
        return

    def init_board(self):
        board = [[0 for x in range(self.board_size)] for y in range(self.board_size)]
        return board

    def try_place_ship(self, location, size, board, ships):
        start_x, end_x, start_y, end_y = location[0], location[0], location[1], location[1]
        direction = random.randint(0, 3)
        i = 0
        while i < XL_SHIP + 1:
            if direction == 0:  # check for left direction
                if location[0] - size < 0:
                    direction = i
                    i += 1
                    continue
                start_x = location[0] - size
                if self.is_valid_location(start_x, end_x, start_y, end_y, board, ships):
                    return True
                else:
                    direction = i
                    i += 1
                    continue
            elif direction == 1:  # check for right direction
                if location[0] + size >= self.board_size:
                    direction = i
                    i += 1
                    continue
                end_x = location[0] + size
                if self.is_valid_location(start_x, end_x, start_y, end_y, board, ships):
                    return True
                else:
                    direction = i
                    i += 1
                    continue
            elif direction == 2:  # check for up direction
                if location[1] - size < 0:
                    direction = i
                    i += 1
                    continue
                start_y = location[1] - size
                if self.is_valid_location(start_x, end_x, start_y, end_y, board, ships):
                    return True
                else:
                    direction = i
                    i += 1
                    continue
            elif direction == 3:
                if location[1] + size >= self.board_size:
                    direction = i
                    i += 1
                    continue
                end_y = location[1] + size
                if self.is_valid_location(start_x, end_x, start_y, end_y, board, ships):
                    return True
                else:
                    direction = i
                    i += 1
                    continue

        return False

    def is_valid_location(self, start_x, end_x, start_y, end_y, board, ships):
        for x in range(start_x, end_x + 1):  # run over the location and check if has ships
            for y in range(start_y, end_y + 1):
                if board[x][y] == 1:
                    return False
        for x in range(start_x, end_x + 1):  # assign ship at the location
            for y in range(start_y, end_y + 1):
                self.player1_board[x][y] = 1
        ship = [(start_x, start_y), (end_x, end_y)]
        ships.append(ship)
        return True

    def start_client(self, player_name, opponent_name):
        path = os.path.abspath(self.client)
        os.system(f'python {path} {player_name} {opponent_name}')

    def pass_msg(self, port, msg):
        if msg == TRY_HIT_MESSAGE:
            if self.player_1_turn:
                player_port_to_send = self.player2_port
            else:
                player_port_to_send = self.player1_port
        elif msg == RESULT_HIT_MESSAGE:
            send_Massage("ACK", port)
            if not self.player_1_turn:
                player_port_to_send = self.player2_port
            else:
                player_port_to_send = self.player1_port
            self.swap_turns()
        pass_msg_to_other_player(port, player_port_to_send)

    def swap_turns(self):
        self.player_1_turn = not self.player_1_turn
        self.player_2_turn = not self.player_2_turn

    def game_over(self):
        if self.player_1_turn:  # player 2 is the winner!
            winner = self.player_2_name
        else:
            winner = self.player_1_name
        self.write_to_log("Server got game over! winner is:" + winner)
        last_window = Last_window(winner, self)
        last_window.mainloop()

    def generate_and_send_board_for_client(self, port):
        ships_positions = self.create_battleground()
        self.write_to_log("board created!")
        send_Massage(ships_positions, port)

    def generate_and_send_turn_for_client(self, port):
        if self.asked_for_turn_first_time:
            turn = self.player_2_turn
        else:
            turn = self.player_1_turn
            self.asked_for_turn_first_time = True
            self.write_to_log("turn decided!")
        send_Massage(turn, port)

    def get_process_id(self, port):
        size = port.recv(HEADER).decode(FORMAT)
        msg_lenght = int(size)
        msg = port.recv(msg_lenght).decode(FORMAT)
        msg = json.loads(msg)

        if port == self.player1_port:
            self.player1_pid = msg
        else:
            self.player2_pid = msg
        send_Massage("ACK", port)

    def disconnect_and_quit(self, port):
        self.write_to_log("got disconnect message")
        if port == self.player1_port:
            subprocess.Popen('taskkill /F /PID {0}'.format(self.player2_pid), shell=True)
        else:
            subprocess.Popen('taskkill /F /PID {0}'.format(self.player1_pid), shell=True)
        self.player1_port.close()
        self.player2_port.close()

    def write_to_log(self, msg):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        name = "[Server]"
        self.log.write(dt_string + " " + name + " " + " " + msg + "\n")


def pass_msg_to_other_player(port, player_port_to_send):
    size = port.recv(HEADER).decode(FORMAT)
    msg_lenght = int(size)
    msg = port.recv(msg_lenght).decode(FORMAT)
    msg = json.loads(msg)
    send_Massage(msg, player_port_to_send)


def send_Massage(msg, port):
    msg_json = json.dumps(msg)
    msg_lenght = len(msg_json)
    msg_json = msg_json.encode(FORMAT)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))  # pad to 64 bytes
    port.send(send_lenght)
    port.send(msg_json)


server = Server()
server.start()
