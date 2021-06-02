import util


class Player:
    def __init__(self):
        self.sprite = util.load_image("player.png")
        self.rect = self.sprite.get_rect()
        self.col = 0
        self.row = 0

    def update(self):
        pass

    def up(self):
        self.row -= 1

    def down(self):
        self.row += 1

    def right(self):
        self.col += 1

    def left(self):
        self.col -= 1

    def draw(self, window):
        self.rect.x = self.rect.width * self.col
        self.rect.y = self.rect.height * self.row
        window.blit(self.sprite, self.rect)

    def set_position(self, col, row):
        self.col = col
        self.row = row

    def get_position(self, to=""):
        positions = {
            "up": lambda col, row: (col, row - 1),
            "down": lambda col, row: (col, row + 1),
            "right": lambda col, row: (col + 1, row),
            "left": lambda col, row: (col - 1, row),
        }
        try:
            return positions[to](self.col, self.row)
        except KeyError:
            return self.col, self.row
