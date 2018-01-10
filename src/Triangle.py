from Point import Point

class Triangle:
	def __init__(self, p0, p1, p2):
		self.p0 = p0
		self.p1 = p1
		self.p2 = p2
	
	def __repr__(self):
		return "(%s, %s, %s)" % (self.p0, self.p1, self.p2)