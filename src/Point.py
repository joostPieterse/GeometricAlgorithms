class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        return "(%s, %s)" % (self.x, self.y)
