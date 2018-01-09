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
    faces = {}
    for point, edges in point2edges.items():
        face = []
        screen_intersections = []
        for edge in edges:
            triangles = edge2triangles[edge]
            print("longest edge", triangles[0], get_longest_edge(triangles[0]))
            if len(triangles) == 2:
                face.append((get_circumcenter(triangles[0]), get_circumcenter(triangles[1])))
                print("No screen intersection", (get_circumcenter(triangles[0]), get_circumcenter(triangles[1])))
            # if there is only one triangle, the voronoi edge will intersect with the screen edge
            elif len(triangles) == 1:
                center = get_circumcenter(triangles[0])
                # intersection between voronoi edge and delaunay edge
                delaunay_intersect = ((edge[0].x + edge[1].x) / 2, (edge[0].y + edge[1].y) / 2)
                # Change direction of the voronoi edge if it is outside the triangle and the longest edge
                if not Delaunay.pointInTriangle(Point(center[0], center[1], ''), triangles[0]) and edge == get_longest_edge(triangles[0]):
                    print("changing", edge)
                    delaunay_intersect = (center[0] + 2 * (center[0] - delaunay_intersect[0]), center[1] + 2 * (center[1] - delaunay_intersect[1]))
                # find intersection between voronoi edge and screen
                if center[1] < delaunay_intersect[1]:
                    screen_intersect_x = center[0] + (screen_height - delaunay_intersect[1]) / (delaunay_intersect[1] - center[1]) * (delaunay_intersect[0] - center[0])
                    if 0 <= screen_intersect_x <= screen_width:
                        face.append((center, (screen_intersect_x, screen_height)))
                        screen_intersections.append((screen_intersect_x, screen_height))
                        print("Point", point, "center", center, "delaunay intersect", delaunay_intersect, "x intersect", (center, (screen_intersect_x, screen_height)))
                elif center[1] > delaunay_intersect[1]:
                    screen_intersect_x = center[0] + (0 - center[1]) / (delaunay_intersect[1] - center[1]) * (delaunay_intersect[0] - center[0])
                    if 0 <= screen_intersect_x <= screen_width:
                        face.append((center, (screen_intersect_x, 0)))
                        screen_intersections.append((screen_intersect_x, 0))
                        print("Point", point, "center", center, "delaunay intersect", delaunay_intersect, "x intersect", (center, (screen_intersect_x, 0)))
                if center[0] < delaunay_intersect[0]:
                    screen_intersect_y = center[1] + (screen_width - delaunay_intersect[0]) / (delaunay_intersect[0] - center[0]) * (delaunay_intersect[1] - center[1])
                    if 0 < screen_intersect_y < screen_height:
                        face.append((center, (screen_width, screen_intersect_y)))
                        screen_intersections.append( (screen_width, screen_intersect_y))
                        print("Point", point, "center", center, "delaunay intersect", delaunay_intersect, "y intersect", (center, (screen_width, screen_intersect_y)))
                elif center[0] > delaunay_intersect[0]:
                    screen_intersect_y = center[1] + (0 - center[0]) / (delaunay_intersect[0] - center[0]) * (delaunay_intersect[1] - center[1])
                    if 0 < screen_intersect_y < screen_height:
                        face.append((center, (0, screen_intersect_y)))
                        screen_intersections.append((0, screen_intersect_y))
                        print("Point", point, "center", center, "delaunay intersect", delaunay_intersect, "y intersect", (center, (0, screen_intersect_y)))
        if len(screen_intersections) == 2:
            a = screen_intersections[0]
            b = screen_intersections[1]
            # intersections are on the same screen edge
            if (a[0] == 0 and b[0] == 0) or (a[1] == 0 and b[1] == 0) or (a[0] == screen_width and b[0] == screen_width) or (a[1] == screen_height and b[1] == screen_height):
                face.append((a, b))
            # intersections are on opposite screen edges
            elif a[0] == 0 and b[0] == screen_width:
                if point.isAbove(a, b):
                    face.append((a, (0, 0)))
                    face.append(((0,0), (screen_width, 0)))
                    face.append(((screen_width, 0), b))
                else:
                    face.append((a, (0, screen_height)))
                    face.append(((0,0), (screen_width, 0)))
                    face.append(((screen_width, screen_height), b))
            elif (a[0] == screen_width and b[0] == 0):
                if point.isAbove(a, b):
                    face.append((b, (0, 0)))
                    face.append(((0,0), (screen_width, 0)))
                    face.append(((screen_width, 0), a))
                else:
                    face.append((b, (0, screen_height)))
                    face.append(((0,0), (screen_width, 0)))
                    face.append(((screen_width, screen_height), a))
            elif a[1] == 0 and b[1] == screen_height:
                if point.isRightOf(a, b):
                    face.append((a, (screen_width, 0)))
                    face.append(((screen_width,0), (screen_width, screen_height)))
                    face.append(((screen_width, screen_height), b))
                else:
                    face.append((a, (0, 0)))
                    face.append(((0,0), (0, screen_height)))
                    face.append(((0, screen_height), b))
            elif a[1] == screen_height and b[1] == 0:
                if point.isRightOf(a, b):
                    face.append((b, (screen_width, 0)))
                    face.append(((screen_width,0), (screen_width, screen_height)))
                    face.append(((screen_width, screen_height), a))
                else:
                    face.append((b, (0, 0)))
                    face.append(((0,0), (0, screen_height)))
                    face.append(((0, screen_height), a))
            # one horizontal screen edge and one vertical is intersected otherwise
            else:
                corner_x = screen_width
                if a[0] == 0 or b[0] == 0:
                    corner_x = 0
                corner_y = screen_height
                if a[1] == 0 or b[1] == 0:
                    corner_y = 0
                face.append(((corner_x, corner_y), a))
                face.append(((corner_x, corner_y), b))


        faces[point] = face
    print("Faces", faces)
    return faces

