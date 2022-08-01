def check_rectangle_pressed(rectangles, position):
    """
    checks if the mouse was pressed in a allowed position on board and returns it
    :param rectangles: the 2d array of rectangles on the board
    :param position: position the mouse was pressed
    :return: row and column if allowed, else None
    """
    for rectangle_row_index in range(1, 11):
        for rectangle_col_index in range(1, 11):
            if rectangles[rectangle_row_index][rectangle_col_index].collidepoint(position):
                return rectangle_row_index - 1, rectangle_col_index - 1
    return None, None


def check_is_hit(rectangles, row, column):
    """
    check if a single rectangle has a ship on it
    :param rectangles: list of rectangles on the board
    :param row: row number
    :param column: column number
    :return: True if there is a ship at that row and column, otherwise False
    """
    if rectangles[row][column] == 1:
        return True
    else:
        return False


def check_is_ship_drown(ship):
    """
    checks if the ship had drown
    :param ship: a wanted ship to check
    :return: True if the ship had drown, else False
    """
    return ship.lives == 0

