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

        # compute which points are closest to the corners of the screen
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

        # add edges to the corner of the screen
        delaunay_edges.add((point_top_left, Point(0,0,"")))
        delaunay_edges.add((point_top_right, Point(width,0,"")))
        delaunay_edges.add((point_bottom_left, Point(0,height,"")))
        delaunay_edges.add((point_bottom_right, Point(width,height,"")))

        for i in range(number_of_points):
            longest_edge_length = -1
            for delaunay_edge in delaunay_edges:
                edge_length = self.get_edge_length(delaunay_edge[0].x, delaunay_edge[0].y, delaunay_edge[1].x, delaunay_edge[1].y)
                if len(delaunay_edges) == 1:
                    newx = uniform(0, width)
                    newy = uniform(0, height)
                elif (edge_length > longest_edge_length):
                    longest_edge_length = edge_length
                    newx, newy, x_point, y_point = self.get_position(delaunay_edge[0].x, delaunay_edge[0].y, delaunay_edge[1].x, delaunay_edge[1].y)
            point_set.append(Point(newx,newy,self.color))
            delaunay_new_edges = delaunay_edges.copy()
            if len(delaunay_edges) > 1:
                for delaunay_edge2 in delaunay_edges:
                    if len(delaunay_new_edges) > 1 and (delaunay_edge2[0].x == x_point or delaunay_edge2[1].x == x_point or delaunay_edge2[0].y == y_point or delaunay_edge2[1].y == y_point):
                        delaunay_new_edges.remove(delaunay_edge2)
                delaunay_edges = delaunay_new_edges.copy()
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
            return newx, newy, x1, y1

        if (x1 > x2):
            newx = 0.001 * xdif + x2 + uniform(0.0000001*xdif,0.001*xdif)
            newy = 0.001 * ydif + y2 + uniform(0.0000001*ydif,0.001*ydif)
            return newx, newy, x2, y2

        points = []

        return points
