import socket
import pygame

HEADER = 64  # each message will have a header to tell the message size
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # when receiving, close the connection and disconnect client
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
BOARD_SIZE = 10
BOARD_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


def draw_rec_grid(screen, color, left, top, width, height):
    """
    create a single rectangle as a part of the grid
    :param screen: the screen into the rectangle is draw
    :param color: color fill of the rectangle
    :param left: left point of the rectangle on screen
    :param top: top point of the rectangle on screen
    :param width: width of the rectangle
    :param height: height of the rectangle
    :return: void
    """
    pygame.draw.rect(screen, color, [left, top, width, height])


def draw_text(screen, text, color, left, top, font_size):
    """
    draw a text to describe the grid
    :param screen: the screen into the title is draw
    :param text: the text in the title
    :param color: color of the title
    :param left: width of the rectangle in which the title will appear
    :param top: height of the rectangle in which the title will appear
    :param font_size: size of text
    :return: void
    """
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.left = left
    text_rect.top = top
    screen.blit(text, text_rect)


def draw_grids(screen, grid_from_server, no_ship_color, ship_color, margin, width, height, background):
    """
    draw a grid that represent a playing board
    :param screen: the screen into the board is draw
    :param grid_from_server: ships location generated from the server
    :param no_ship_color: color to fill no ship rectangle
    :param ship_color: color to fill ship rectangle
    :param margin: space between rectangles on the board
    :param width: width of each rectangle on the board
    :param height: height of each rectangle on the board
    :param background: background color
    :return:
    """
    for row in range(BOARD_SIZE + 1):
        for column in range(BOARD_SIZE + 1):
            # color
            color = no_ship_color
            if grid_from_server[row][column] == 1:
                color = ship_color
            elif column == 0 or row == 0:
                color = background

            # direction
            left = (margin + width) * column + margin
            top = (margin + height) * row + margin

            draw_rec_grid(screen, color, left, top, width, height)

            # Opponent color
            if column == 0 or row == 0:
                opponent_color = background
            else:
                opponent_color = no_ship_color

            # Opponent direction
            opponent_left = 11 * (margin + width) + left + 100

            draw_rec_grid(screen, opponent_color, opponent_left, top, width, height)

            # draw indicators
            if column == 0 and row != 0:
                draw_text(screen, str(row), no_ship_color, left, top, 22)
                draw_text(screen, str(row), no_ship_color, opponent_left, top, 22)
            if row == 0 and column != 0:
                draw_text(screen, BOARD_LETTERS[column - 1], no_ship_color, left, top, 22)
                draw_text(screen, BOARD_LETTERS[column - 1], no_ship_color, opponent_left, top, 22)

    draw_text(screen, "My Grid", ship_color, left - 6 * width, top + height + 10, 32)
    draw_text(screen, "Opponent Grid", no_ship_color, opponent_left - 7 * width, top + height + 10, 32)


def gui(grid_from_server):
    """
    creates the gui for the game
    :param grid_from_server: ships location generated from the server
    :return: void
    """
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (0, 0, 255)
    WIDTH = 40
    HEIGHT = 40
    MARGIN = 3
    x = (WIDTH + 2 * MARGIN) * 12 * 2
    y = (HEIGHT + MARGIN) * 11 + 100

    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([x, y])
    pygame.display.set_caption("Battleships")

    # Fill the background with white
    screen.fill(black)

    # Draw
    draw_grids(screen, grid_from_server, white, blue, MARGIN, WIDTH, HEIGHT, black)

    # Flip the display
    pygame.display.flip()


def handle_game(current_client):
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    pygame.quit()
    current_client.send(DISCONNECT_MESSAGE)


class Client:
    """
    represents a client connecting to server and created gui
    """

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        grid = self.connect_to_server()
        gui(grid)

    def connect_to_server(self):
        """
        Initialize connection to server and get location of battleships
        :param self: the client
        :return: grid to create the board
        """
        self.socket.connect(ADDRESS)
        # wait for server to give battleships locations
        grid = []
        for row in range(11):
            grid.append([])
            for column in range(11):
                grid[row].append(0)
        grid[1][5] = 1
        grid[1][6] = 1
        return grid

    def send(self, msg):
        """
        sends a message to the server through the socket
        :param msg: a string message to send to the server
        :return: void
        """
        message = msg.encode(FORMAT)
        msg_lenght = len(message)
        send_lenght = str(msg_lenght).encode(FORMAT)
        send_lenght += b' ' * (HEADER - len(send_lenght))  # padd to 64 bytes
        self.socket.send(send_lenght)
        self.socket.send(message)
        print(self.socket.recv(2048).decode(FORMAT))


client = Client()
handle_game(client)
