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
                return rectangle_row_index, rectangle_col_index
    return None, None
