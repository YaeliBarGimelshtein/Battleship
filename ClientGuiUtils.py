from itertools import cycle

import pygame

BOARD_SIZE = 10
BOARD_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
SPACE_BETWEEN_BOARDS = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RECTANGLE_WIDTH = 40
RECTANGLE_HEIGHT = 40
RECTANGLE_MARGIN = 3
FONT_SIZE = 22
HEADLINE_SIZE = 32
BLINK_EVENT = pygame.USEREVENT + 0


def draw_rec_grid(screen, color, left, top):
    """
    create a single rectangle as a part of the board
    :param screen: the screen into the rectangle is draw
    :param color: color fill of the rectangle
    :param left: left point of the rectangle on screen
    :param top: top point of the rectangle on screen
    :return: a rectangle bounding the changed pixels
    """
    return pygame.draw.rect(screen, color, [left, top, RECTANGLE_WIDTH, RECTANGLE_HEIGHT])


def draw_blink_rect(screen, color, left, top, text):
    font = pygame.font.Font('freesansbold.ttf', HEADLINE_SIZE)
    text = font.render(text, True, color)
    text_rect_size_height = text.get_rect().height
    text_rect_size_width = text.get_rect().width
    return pygame.draw.rect(screen, color,  [left, top, text_rect_size_width, text_rect_size_height])


def draw_text(screen, text, color, left, top, font_size):
    """
    add text to screen
    :param screen: the screen into the text is draw
    :param text: the text
    :param color: color of the text
    :param left: left point of the rectangle in which the text will appear
    :param top: top point of the rectangle in which the text will appear
    :param font_size: size of font of the text
    :return: void
    """
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.left = left
    text_rect.top = top
    screen.blit(text, text_rect)


def draw_number_column(screen, row, column, left, opponent_left, top):
    if column == 0 and row != 0:
        draw_text(screen, str(row), WHITE, left, top, FONT_SIZE)
        draw_text(screen, str(row), WHITE, opponent_left, top, FONT_SIZE)


def draw_letter_row(screen, row, column, left, opponent_left, top):
    if row == 0 and column != 0:
        draw_text(screen, BOARD_LETTERS[column - 1], WHITE, left, top, FONT_SIZE)
        draw_text(screen, BOARD_LETTERS[column - 1], WHITE, opponent_left, top, FONT_SIZE)


def draw_headlines(screen, left, opponent_left, top):
    draw_text(screen, "My Grid", WHITE, left - 6 * RECTANGLE_WIDTH, top + RECTANGLE_HEIGHT + 10, 32)
    draw_text(screen, "Opponent Grid", WHITE, opponent_left - 7 * RECTANGLE_WIDTH, top + RECTANGLE_HEIGHT + 10, 32)


def calc_fill_rectangle(grid_array, row, column):
    """
    calculates the RGB color of rectangle filling
    :param grid_array: ships location generated from the server
    :param row: row of rectangle in the grid
    :param column: column of rectangle in the grid
    :return: RGB color of rectangle filling
    """
    if grid_array is not None and grid_array[row][column] == 1:
        return BLUE
    elif column == 0 or row == 0:
        return BLACK
    else:
        return WHITE


def calc_left_point_rectangle(column):
    """
    calculates the left point of the rectangle in client grid
    :param column: column of rectangle in the grid
    :return: left point of rectangle
    """
    return (RECTANGLE_MARGIN + RECTANGLE_WIDTH) * column + RECTANGLE_MARGIN


def calc_left_point_opponent_rectangle(column, left):
    """
    calculates the left point of the rectangle in opponent grid
    :param column: column of rectangle in the grid
    :param left: left point of twin rectangle in client board
    :return: left point of rectangle
    """
    return (BOARD_SIZE + 1) * (RECTANGLE_MARGIN + RECTANGLE_WIDTH) + left + SPACE_BETWEEN_BOARDS


def calc_top_point_rectangle(row):
    """
    calculates the top point of the rectangle
    :param row: row of rectangle in the grid
    :return: top point of rectangle
    """
    return (RECTANGLE_MARGIN + RECTANGLE_HEIGHT) * row + RECTANGLE_MARGIN


def draw_grids(screen, grid_from_server, my_rectangles, opponent_rectangles):
    """
    draw a grid that represent a playing board
    :param screen: the screen into the board is draw
    :param grid_from_server: ships location generated from the server
    :param opponent_rectangles: empty list of all rectangles of opponent board
    :param my_rectangles: empty list of all rectangles of my board
    :return:
    """
    for row in range(BOARD_SIZE + 1):
        my_rectangles.append([])
        opponent_rectangles.append([])
        for column in range(BOARD_SIZE + 1):
            # my board
            color = calc_fill_rectangle(grid_from_server, row, column)
            left = calc_left_point_rectangle(column)
            top = calc_top_point_rectangle(row)
            my_rectangles[row].append(draw_rec_grid(screen, color, left, top))

            # opponent board
            opponent_color = calc_fill_rectangle(None, row, column)
            opponent_left = calc_left_point_opponent_rectangle(column, left)
            opponent_rectangles[row].append(draw_rec_grid(screen, opponent_color, opponent_left, top))

            # draw indicators
            draw_letter_row(screen, row, column, left, opponent_left, top)
            draw_number_column(screen, row, column, left, opponent_left, top)

    draw_headlines(screen, left, opponent_left, top)


def create_gui(grid_from_server, my_rectangles, opponent_rectangles):
    x = (RECTANGLE_WIDTH + 2 * RECTANGLE_MARGIN) * (BOARD_SIZE + 2) * 2
    y = (RECTANGLE_HEIGHT + RECTANGLE_MARGIN) * (BOARD_SIZE + 1) + SPACE_BETWEEN_BOARDS

    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([x, y])
    pygame.display.set_caption("Battleships")

    # Fill the background with white
    screen.fill(BLACK)

    # Draw
    draw_grids(screen, grid_from_server, my_rectangles, opponent_rectangles)

    # Flip the display
    pygame.display.flip()
    return screen
