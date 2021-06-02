import util


class Block:
    def __init__(self, sprite, col, row):
        self.sprite = util.load_image(sprite, transparent=True)
        self.rect = self.sprite.get_rect()
        self.type_ = sprite.split(".")[0]
        self.col = col
        self.row = row

    def draw(self, window):
        self.rect.x = self.rect.width * self.col
        self.rect.y = self.rect.height * self.row
        window.blit(self.sprite, self.rect)

    def up(self):
        self.row -= 1

    def down(self):
        self.row += 1

    def right(self):
        self.col += 1

    def left(self):
        self.col -= 1

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
