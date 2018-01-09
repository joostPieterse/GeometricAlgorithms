class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        return "(%s, %s)" % (self.x, self.y)

    def isAbove(self, point1, point2):
        result = self.y > (self.x - point1[0]) / (point2[0] - point1[0]) * (point2[1] - point1[1]) + point1[1]
        print("isAbove", point1, point2, self, result)
        return result

    def isRightOf(self, point1, point2):
        result = self.x > (self.y - point1[1]) / (point2[1] - point1[1]) * (point2[0] - point1[0]) + point1[0]
        return result
