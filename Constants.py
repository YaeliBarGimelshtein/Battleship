"""
Header file --> constants used by both server and client
"""
import socket
HEADER = 64  # each message will have a header to tell the message size
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # when receiving, close the connection and disconnect client
GET_BOARD_MESSAGE = "GET_BOARD"
GET_TURN_MESSAGE = "GET_TURN"
WAIT_TURN_MESSAGE = "WAIT_TURN"
TRY_HIT_MESSAGE = "TRY_HIT"
RESULT_HIT_MESSAGE = "RESULT_HIT"
PID_MESSAGE = "PID"
GAME_OVER = "GAME_OVER"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
YOUR_TURN = "Your turn, Select opponent battleship location"
OPPONENT_TURN = "Opponent Turn, please wait"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
XL_SHIP = 4
L_SHIP = 3
M_SHIP = 2
S_SHIP = 1
