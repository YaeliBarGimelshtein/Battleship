class Ship:
    def __init__(self, start, end):
        self.start_x = start[0]
        self.start_y = start[1]
        self.end_x = end[0]
        self.end_y = end[1]
        self.lives = self.calc_size()
        self.indexes = self.calc_all_indexes()
        self.hit_indexes = []

    def __eq__(self, other):
        """
        check if two ships are equal
        :param other: ship to compare to
        :return: True if equal, else False
        """
        if isinstance(other, Ship):
            return self.start_x == other.start_x and self.start_y == other.start_y and self.end_x == other.end_x and \
                   self.end_y == other.end_y and self.lives == other.lives and self.indexes.__eq__(other.indexes)

    def hit(self, row, column):
        """
        decreases the life of the ship and remove location to hit array
        :param row: row on grid
        :param column: column on grid
        :return: void
        """
        self.lives -= 1
        self.indexes.remove((row, column))
        self.hit_indexes.append((row, column))

    def is_hit(self, row, column):
        """
        checks if the ship was hit
        :param row: row on grid
        :param column: column on grid
        :return: True if ship was hot, else False
        """
        if (row, column) in self.indexes:
            return True
        else:
            return False

    def drown(self):
        """
        checks if the ship drown
        :return: True if ship drown, else False
        """
        return self.lives == 0

    def calc_size(self):
        """
        calculates size of ship
        :return: size of ship (int)
        """
        if self.start_x == self.end_x:
            return self.end_y - self.start_y
        else:
            return self.end_x - self.start_x

    def calc_all_indexes(self):
        """
        calculates all indexes of the ship
        :return: array [(x,y)..] indexes of the ship
        """
        indexes = [(self.start_x + 1, self.start_y + 1)]
        if self.start_x == self.end_x:
            for counter in range(1, self.lives):
                indexes.append((self.start_x + 1, self.start_y + 1 + counter))
        else:
            for counter in range(1, self.lives):
                indexes.append((self.start_x + 1 + counter, self.start_y + 1))
        return indexes
