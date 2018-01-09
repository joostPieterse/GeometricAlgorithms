from Point import Point
import Delaunay
import math

def get_edges(triangle):
    return [(triangle[0], triangle[1]), (triangle[0], triangle[2]), (triangle[1], triangle[2])]


def get_circumcenter(triangle):
    D = 2 * (triangle[0].x * (triangle[1].y - triangle[2].y) +
             triangle[1].x * (triangle[2].y - triangle[0].y) +
             triangle[2].x * (triangle[0].y - triangle[1].y))
    circumcenter_x = 1 / D * ((triangle[0].x ** 2 + triangle[0].y ** 2) * (triangle[1].y - triangle[2].y) +
                              (triangle[1].x ** 2 + triangle[1].y ** 2) * (triangle[2].y - triangle[0].y) +
                              (triangle[2].x ** 2 + triangle[2].y ** 2) * (triangle[0].y - triangle[1].y))
    circumcenter_y = 1 / D * ((triangle[0].x ** 2 + triangle[0].y ** 2) * (triangle[2].x - triangle[1].x) +
                              (triangle[1].x ** 2 + triangle[1].y ** 2) * (triangle[0].x - triangle[2].x) +
                              (triangle[2].x ** 2 + triangle[2].y ** 2) * (triangle[1].x - triangle[0].x))
    return circumcenter_x, circumcenter_y


def get_length(edge):
    return math.sqrt((edge[0].x - edge[1].x) ** 2 + (edge[0].y - edge[1].y) ** 2)

def get_longest_edge(triangle):
    largest_length = get_length((triangle[0], triangle[1]))
    largest_edge = (triangle[0], triangle[1])
    if get_length((triangle[0], triangle[2])) > largest_length:
        largest_edge = (triangle[0], triangle[2])
        largest_length = get_length((triangle[0], triangle[2]))
    if get_length((triangle[1], triangle[2])) > largest_length:
        largest_edge = (triangle[1], triangle[2])
    return largest_edge


def computeVoronoi(input_triangles, screen_width, screen_height):
    # for each edge, list all incident triangles
    edge2triangles = {}
    for triangle in input_triangles:
        for edge in get_edges(triangle):
            if edge in edge2triangles:
                edge2triangles[edge].append(triangle)
            elif (edge[1], edge[0]) in edge2triangles:
                edge2triangles[(edge[1], edge[0])].append(triangle)
            else:
                edge2triangles[edge] = [triangle]
    # for each point, list all incident edges
    point2edges = {}
    for edge in edge2triangles:
        if edge[0] in point2edges:
            point2edges[edge[0]].append(edge)
        else:
            point2edges[edge[0]] = [edge]
        if edge[1] in point2edges:
            point2edges[edge[1]].append(edge)
        else:
            point2edges[edge[1]] = [edge]
    point2screen_corners = {}
    screen_corners = [(0,0), (0, screen_height), (screen_width, screen_height), (screen_width, 0)]
    for screen_corner in screen_corners:
        closest_point = min(point2edges, key=lambda p: (p.x - screen_corner[0]) ** 2 + (p.y - screen_corner[1]) ** 2)
        if closest_point in point2screen_corners:
            point2screen_corners[closest_point].append(screen_corner)
        else:
            point2screen_corners[closest_point] = [screen_corner]
    faces = {}
    for point, edges in point2edges.items():
        face = set()
        for corner in point2screen_corners.get(point, []):
            face.add(corner)
        for edge in edges:
            triangles = edge2triangles[edge]
            if len(triangles) == 2:
                center0 = get_circumcenter(triangles[0])
                center1 = get_circumcenter(triangles[1])
                if 0 <= center0[0] <= screen_width and 0 <= center0[1] <= screen_height:
                    face.add(center0)
                if 0 <= center1[0] <= screen_width and 0 <= center1[1] <= screen_height:
                    face.add(center1)
                # add possible intersections
                if (center0[0] < 0) != (center1[0] < 0):
                    screen_intersect_y = center0[1] + (0 - center0[0]) / (center1[0] - center0[0]) * (center1[1] - center0[1])
                    if 0 < screen_intersect_y < screen_height:
                        face.add((0, screen_intersect_y))
                if (center0[0] > screen_width) != (center1[0] > screen_width):
                    screen_intersect_y = center0[1] + (screen_width - center0[0]) / (center1[0] - center0[0]) * (center1[1] - center0[1])
                    if 0 < screen_intersect_y < screen_height:
                        face.add((screen_width, screen_intersect_y))
                if (center0[1] < 0) != (center1[1] < 0):
                    screen_intersect_x = center0[0] + (0 - center0[1]) / (center1[1] - center0[1]) * (center1[0] - center0[0])
                    if 0 < screen_intersect_x < screen_width:
                        face.add((screen_intersect_x, 0))
                if (center0[1] > screen_height) != (center1[1] > screen_height):
                    screen_intersect_x = center0[0] + (screen_height - center0[1]) / (center1[1] - center0[1]) * (center1[0] - center0[0])
                    if 0 < screen_intersect_x < screen_width:
                        face.add((screen_intersect_x, screen_height))
            elif len(triangles) == 1:
                center = get_circumcenter(triangles[0])
                if 0 <= center[0] <= screen_width and 0 <= center[1] <= screen_height:
                    face.add(center)
                # intersection between voronoi edge and delaunay edge
                delaunay_intersect = ((edge[0].x + edge[1].x) / 2, (edge[0].y + edge[1].y) / 2)
                # Change direction of the voronoi edge if it is outside the triangle and the longest edge
                if not Delaunay.pointInTriangle(Point(center[0], center[1], ''), triangles[0]) and edge == get_longest_edge(triangles[0]):
                    delaunay_intersect = (center[0] + 2 * (center[0] - delaunay_intersect[0]), center[1] + 2 * (center[1] - delaunay_intersect[1]))
                if not (0 <= center[0] <= screen_width and 0 <= center[1] <= screen_height):
                    if not (0 <= delaunay_intersect[0] <= screen_width and 0 <= delaunay_intersect[1] <= screen_height):
                        continue
                    if center[1] < 0:
                        screen_intersect_x = center[0] + (center[1]) / (
                        center[1] - delaunay_intersect[1]) * (delaunay_intersect[0] - center[0])
                        if 0 <= screen_intersect_x <= screen_width:
                            face.add((screen_intersect_x, 0))
                    elif center[1] > screen_height:
                        screen_intersect_x = center[0] + (center[1] - screen_height) / (
                        center[1] - delaunay_intersect[1]) * (delaunay_intersect[0] - center[0])
                        if 0 <= screen_intersect_x <= screen_width:
                            face.add((screen_intersect_x, screen_height))
                    if center[0] < 0:
                        screen_intersect_y = center[1] + (center[0]) / (
                        center[0] - delaunay_intersect[0]) * (delaunay_intersect[1] - center[1])
                        if 0 < screen_intersect_y < screen_height:
                            face.add((0, screen_intersect_y))
                    elif center[0] > screen_width:
                        screen_intersect_y = center[1] + (center[0] - screen_width) / (
                        center[0] - delaunay_intersect[0]) * (delaunay_intersect[1] - center[1])
                        if 0 < screen_intersect_y < screen_height:
                            face.add((screen_width, screen_intersect_y))
                # find intersection of voronoi edge going out of the screen
                if center[1] < delaunay_intersect[1]:
                    screen_intersect_x = center[0] + (screen_height - center[1]) / (delaunay_intersect[1] - center[1]) * (delaunay_intersect[0] - center[0])
                    if 0 <= screen_intersect_x <= screen_width:
                        face.add((screen_intersect_x, screen_height))
                elif center[1] > delaunay_intersect[1]:
                    screen_intersect_x = center[0] + (0 - center[1]) / (delaunay_intersect[1] - center[1]) * (delaunay_intersect[0] - center[0])
                    if 0 <= screen_intersect_x <= screen_width:
                        face.add((screen_intersect_x, 0))
                if center[0] < delaunay_intersect[0]:
                    screen_intersect_y = center[1] + (screen_width - center[0]) / (delaunay_intersect[0] - center[0]) * (delaunay_intersect[1] - center[1])
                    if 0 < screen_intersect_y < screen_height:
                        face.add((screen_width, screen_intersect_y))
                elif center[0] > delaunay_intersect[0]:
                    screen_intersect_y = center[1] + (0 - center[0]) / (delaunay_intersect[0] - center[0]) * (delaunay_intersect[1] - center[1])
                    if 0 < screen_intersect_y < screen_height:
                        face.add((0, screen_intersect_y))
        faces[point] = face
    return faces


def get_area_triangle(point1, point2, point3):
    a = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    b = math.sqrt((point1[0] - point3[0]) ** 2 + (point1[1] - point3[1]) ** 2)
    c = math.sqrt((point2[0] - point3[0]) ** 2 + (point2[1] - point3[1]) ** 2)
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def get_area(point, face):
    points = [p for p in face]
    points.sort(key=lambda p: math.atan2(point.y - p[1], point.x - p[0]))
    area = 0
    for i in range(len(points) - 2):
        area += get_area_triangle(points[-1], points[i], points[i + 1])
    return area


def get_area_percentages(faces, screen_width, screen_height):
    areas = {"blue": 0, "red": 0}
    for point, voronoi_points in faces.items():
        areas[point.color] += get_area(point, voronoi_points)
    for color, area in areas.items():
        areas[color] *= 100 / (screen_width * screen_height)
    return areas


