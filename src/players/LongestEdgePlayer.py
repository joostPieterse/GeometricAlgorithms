from Point import Point
from math import sqrt
from random import uniform

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

        width = settings['width']
        height = settings['height']
        point_set = []
        top_left = max(width,height) * 2
        top_right = max(width,height) * 2
        bottom_right = max(width,height) * 2
        bottom_left = max(width,height) * 2

        for delaunay_point in delaunay_points:
            if self.get_edge_length(delaunay_point.x, delaunay_point.y, 0, 0) < top_left:
                top_left = self.get_edge_length(delaunay_point.x, delaunay_point.y, 0, 0)
                point_top_left = delaunay_point

            if self.get_edge_length(delaunay_point.x, delaunay_point.y, width, 0) < top_right:
                top_right = self.get_edge_length(delaunay_point.x, delaunay_point.y, width, 0)
                point_top_right = delaunay_point

            if self.get_edge_length(delaunay_point.x, delaunay_point.y, 0, height) < bottom_left:
                bottom_left = self.get_edge_length(delaunay_point.x, delaunay_point.y, 0, height)
                point_bottom_left = delaunay_point

            if self.get_edge_length(delaunay_point.x, delaunay_point.y, width, height) < bottom_right:
                bottom_right = self.get_edge_length(delaunay_point.x, delaunay_point.y, width, height)
                point_bottom_right = delaunay_point

        delaunay_edges.add((point_top_left, Point(0,0,"")))
        delaunay_edges.add((point_top_right, Point(width,0,"")))
        delaunay_edges.add((point_bottom_left, Point(0,height,"")))
        delaunay_edges.add((point_bottom_right, Point(width,height,"")))

        for i in range(number_of_points):
            longest_edge_length = -1
            for delaunay_edge in delaunay_edges:
                edge_length = self.get_edge_length(delaunay_edge[0].x, delaunay_edge[0].y, delaunay_edge[1].x, delaunay_edge[1].y)
                if (edge_length > longest_edge_length):
                    longest_edge_length = edge_length
                    longest_edge = delaunay_edge
                    newx, newy = self.get_position(delaunay_edge[0].x, delaunay_edge[0].y, delaunay_edge[1].x, delaunay_edge[1].y)
            print("Appended: ", newx, newy)
            point_set.append(Point(newx,newy,self.color))
            print("Removed: ", longest_edge)
            delaunay_edges.remove(longest_edge)
        return [point_set[i] for i in range(number_of_points)]

    def get_edge_length(self, x1, y1, x2, y2):
        xdif = abs(x1-x2)
        ydif = abs(y1-y2)
        return sqrt(xdif*xdif + ydif*ydif)

    def get_position(self, x1, y1, x2, y2):
        xdif = abs(x1 - x2)
        ydif = abs(y1 - y2)
        if(x1 <= x2):
            newx = 0.001 * xdif + x1 + uniform(0.0000001*xdif,0.001*xdif)
            newy = 0.001 * ydif + y1 + uniform(0.0000001*ydif,0.001*ydif)
        if (x1 > x2):
            newx = 0.001 * xdif + x2 + uniform(0.0000001*xdif,0.001*xdif)
            newy = 0.001 * ydif + y2 + uniform(0.0000001*ydif,0.001*ydif)
        return newx, newy

        # Add edges to the corner of the screen
        points = []

        return points
