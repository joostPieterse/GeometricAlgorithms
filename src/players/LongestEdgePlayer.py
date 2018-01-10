from Point import Point
from math import sqrt

class LongestEdgePlayer:

    def __init__(self, delaunay_triangulation):
        self.delaunay_triangulation = delaunay_triangulation

    def get_points(self, number_of_points, settings, points):
        self.color = "red"
        if points is not None:
            self.color = "blue"
        delaunay_edges = set()
        for delaunay_triangle in self.delaunay_triangulation:
            if (delaunay_triangle[1], delaunay_triangle[0]) not in delaunay_edges:
                delaunay_edges.add((delaunay_triangle[0], delaunay_triangle[1]))
            if (delaunay_triangle[2], delaunay_triangle[0]) not in delaunay_edges:
                delaunay_edges.add((delaunay_triangle[0], delaunay_triangle[2]))
            if (delaunay_triangle[2], delaunay_triangle[1]) not in delaunay_edges:
                delaunay_edges.add((delaunay_triangle[1], delaunay_triangle[2]))
        delaunay_points = set()
        for delaunay_triangle in self.delaunay_triangulation:
            delaunay_points.add(delaunay_triangle[0])
            delaunay_points.add(delaunay_triangle[1])
            delaunay_points.add(delaunay_triangle[2])

        # Add edges to the corner of the screen
        points = []

        return points
