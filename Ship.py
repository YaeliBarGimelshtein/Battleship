class Ship:
    def __init__(self, start, end):
        self.start_x = start[0]
        self.start_y = start[1]
        self.end_x = end[0]
        self.end_y = end[1]
        self.lives = self.calc_size()
        self.indexes = self.calc_all_indexes()

    def hit(self):
        self.lives -= 1

    def calc_size(self):
        if self.start_x == self.end_x:
            return self.end_y - self.start_y
        else:
            return self.end_x - self.start_x

    def calc_all_indexes(self):
        indexes = [(self.start_x + 1, self.start_y + 1)]
        if self.start_x == self.end_x:
            for counter in range(1, self.lives):
                indexes.append((self.start_x + 1, self.start_y + 1 + counter))
        else:
            for counter in range(1, self.lives):
                indexes.append((self.start_x + 1 + counter, self.start_y + 1))
        return indexes
