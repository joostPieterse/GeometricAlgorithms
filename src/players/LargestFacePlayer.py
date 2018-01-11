from random import uniform

import Voronoi
import math

import sys

from Point import Point


class LargestFacePlayer:

    def __init__(self, voronoi_diagram):
        self.voronoi_diagram = voronoi_diagram

    def ccw(self, point1, point2, point3):
        return (point3[1] - point1[1]) * (point2[0] - point1[0]) > (point2[1] - point1[1]) * (point3[0] - point1[0])

    def is_intersecting(self, edge1, edge2):
        return self.ccw(edge1[0], edge2[0], edge2[1]) != self.ccw(edge1[1], edge2[0], edge2[1]) and \
               self.ccw(edge1[0], edge1[1], edge2[0]) != self.ccw(edge1[0], edge1[1], edge2[1])

    def get_intersection(self, edge1, edge2):
        if math.isclose(edge1[1][0], edge1[0][0]):
            return (edge1[0][0], edge2[0][1] + (edge2[1][1] - edge2[0][1])/(edge2[1][0] - edge2[0][0]) * (edge1[0][0] - edge2[0][0]))
        t = ((edge2[1][1] - edge2[0][1]) * (edge2[0][0] - edge1[0][0]) - (edge2[1][0] - edge2[0][0]) *
             (edge2[0][1] - edge1[0][1])) / ((edge1[1][0] - edge1[0][0]) * (edge2[1][1] - edge2[0][1]) - (edge2[1][0] - edge2[0][0]) * (edge1[1][1] - edge1[0][1]))
        return (edge1[0][0] + (edge1[1][0] - edge1[0][0]) * t, edge1[0][1] + (edge1[1][1] - edge1[0][1]) * t)

    def get_length(self, voronoi_edge):
        return math.sqrt((voronoi_edge[1][0]-voronoi_edge[0][0])**2 + (voronoi_edge[1][1]-voronoi_edge[0][1])**2)


    def get_points(self, number_of_points, settings, points):
        self.color = "red"
        if points is not None:
            self.color = "blue"
        result = []
        # Sort existing points by face area
        print(self.voronoi_diagram)
        points.sort(reverse=True, key=lambda p: Voronoi.get_area(p, self.voronoi_diagram[p]))
        for point in points:
            if len(result) >= number_of_points:
                break
            face = [p for p in self.voronoi_diagram[point]]
            face.sort(key=lambda p: math.atan2(point.y - p[1], point.x - p[0]))
            # Candidate line that are perpendicular to a Voronoi edge and that go through the Delaunay point
            candidates = {}
            for i in range(len(face)):
                # Voronoi edge
                e = (face[i], face[(i + 1) % len(face)])
                # Find the edge that the perpendicular line through point intersects
                normal = ((-(e[1][1] - e[0][1]), e[1][0] - e[0][0]), (e[1][1] - e[0][1], -(e[1][0] - e[0][0])))
                multiplier = self.get_length(((0, 0), (settings['width'], settings['height']))) / self.get_length(normal)
                normal = ((normal[0][0] * multiplier, normal[0][1] * multiplier), (normal[1][0] * multiplier, normal[1][1] * multiplier))
                perp_edge = ((point.x, point.y), (point.x + normal[0][0] - normal[1][0], point.x + normal[0][1] - normal[1][1]))
                for j in range(len(face)):
                    intersect_edge = (face[j], face[(j + 1) % len(face)])
                    if self.is_intersecting(perp_edge, intersect_edge):
                        break
                #print("intersect_edge", intersect_edge)
                #print("e", e)
                #print("perp_edge", perp_edge)
                intersect1 = self.get_intersection(e, perp_edge)
                intersect2 = self.get_intersection(intersect_edge, perp_edge)
                candidates[e] = (intersect1, intersect2)
            # Best candidate
            e = None
            best_candidate_perp = None
            best_candidate_length = sys.float_info.max
            # Find the shortest perpendicular edge
            for voronoi_edge, perp_edge in candidates.items():
                if self.get_length(perp_edge) < best_candidate_length:
                    best_candidate_length = self.get_length(perp_edge)
                    e = voronoi_edge
                    best_candidate_perp = perp_edge
            # Find the voronoi edges that intersect with the line parallel to best_candidate through point
            multiplier = self.get_length(((0, 0), (settings['width'], settings['height']))) / self.get_length(e)
            # Check both directions from the point
            result_line1 = ((point.x, point.y), (point.x + multiplier * (e[1][0]-e[0][0]), point.y + multiplier * (e[1][1]-e[0][1])))
            result_line2 = ((point.x, point.y), (point.x - multiplier * (e[1][0]-e[0][0]), point.y - multiplier * (e[1][1]-e[0][1])))
            for voronoi_edge in candidates:
                if self.is_intersecting(result_line1, voronoi_edge):
                    intersect_voronoi1 = self.get_intersection(result_line1, voronoi_edge)
                if self.is_intersecting(result_line2, voronoi_edge):
                    intersect_voronoi2 = self.get_intersection(result_line2, voronoi_edge)
            best_intersect = intersect_voronoi1
            if self.get_length(((point.x, point.y), intersect_voronoi2)) > self.get_length(((point.x, point.y), intersect_voronoi1)):
                best_intersect = intersect_voronoi2
            xdiff = best_intersect[0] - point.x
            ydiff = best_intersect[1] - point.y
            print("xdiff", xdiff, "ydiff", ydiff)
            result.append(Point(point.x + .01 * xdiff + uniform(0.0001*xdiff, 0.001*xdiff), point.y + .01 * ydiff + uniform(0.0001*ydiff,0.001*ydiff), self.color))
        return result
