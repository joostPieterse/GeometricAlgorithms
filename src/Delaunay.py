import math
import numpy

from Point import Point


# Used for pointInTriangle()
def sign(q, p1, p2):
    return (q.x - p2.x) * (p1.y - p2.y) - (p1.x - p2.x) * (q.y - p2.y)


# Checks whether or not a point p is in a triangle t
def pointInTriangle(p, t):
    b1 = sign(p, t[0], t[1]) < 0
    b2 = sign(p, t[1], t[2]) < 0
    b3 = sign(p, t[2], t[0]) < 0
    return (b1 == b2) and (b2 == b3)


# Returns an array [minx, maxx, miny, maxy] of a given
# array of points
def getExtremes(points):
    # Initialize extremum variables
    minx = -1
    maxx = -1
    miny = -1
    maxy = -1

    # Loop through all points
    for point in points:
        if minx == -1 or point.x < minx:
            minx = point.x
        if maxx == -1 or point.x > maxx:
            maxx = point.x
        if miny == -1 or point.y < miny:
            miny = point.y
        if maxy == -1 or point.y > maxx:
            maxy = point.y

    # Create and return the result array
    result = []
    result.append(minx)
    result.append(maxx)
    result.append(miny)
    result.append(maxy)
    return result


# Initializes the triangulation with three points far away
# from the extreme coordinates
def initializeT(points):
    # Create array of points T
    p = []
    t = []

    # Find the extreme coordinates in points
    extremes = getExtremes(points)
    minx = extremes[0]
    maxx = extremes[1]
    miny = extremes[2]
    maxy = extremes[3]

    # Add three points for the bounding triangle
    midx = (minx + maxx) / 2
    midy = (miny + maxy) / 2
    dx = maxx - minx
    dy = maxy - miny
    p0 = Point(midx - 3 * dx, midy - 3 * dy, -1)
    p1 = Point(midx + 3 * dx, midy - 3 * dy, -1)
    p2 = Point(midx, midy + 3 * dy, -1)
    p.append(p0)
    p.append(p1)
    p.append(p2)
    t.append((p0, p1, p2))

    # Return T
    return p, t


# Computes the angle at p1 from the x-axis to p2
def computeAngle(p1, p2):
    # Compute the distance between p1 and p2
    d = numpy.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y))

    # Compute and return the angle at p1
    if d == 0:
        return 0
    angle = math.asin((p2.y - p1.y) / d)
    return angle


# Computes the minimum angle in a triangle (p1, p2, p3)
def minimumAngle(p1, p2, p3):
    # Compute the angles of the points with the x-axis
    angle12 = computeAngle(p1, p2)
    angle13 = computeAngle(p1, p3)
    angle23 = computeAngle(p2, p3)

    # Compute the relative angles at the points
    angle1 = abs(angle12 - angle13)
    angle2 = abs(angle23 - angle12)
    angle3 = abs(angle13 - angle23)

    # Return the minimum of the three angles
    return min(angle1, angle2, angle3)


# Legalizes an edge (p1, p2) in a triangulation t, given the third
# point of the triangle including (p1, p2)
def legalizeEdge(p1, p2, t, point):
    # Loop through all triangles
    opposite = -1
    for tr in t:
        if tr[0] == p1 and tr[1] == p2:
            opposite = tr[2]
        if tr[0] == p2 and tr[1] == p1:
            opposite = tr[2]
        if tr[1] == p1 and tr[2] == p2:
            opposite = tr[0]
        if tr[1] == p2 and tr[2] == p1:
            opposite = tr[0]
        if tr[2] == p1 and tr[0] == p2:
            opposite = tr[1]
        if tr[2] == p2 and tr[0] == p1:
            opposite = tr[1]

    # Compute angles
    angle1a = minimumAngle(p1, p2, opposite)
    angle1b = minimumAngle(p1, p2, point)
    angle2a = minimumAngle(p2, opposite, point)
    angle2b = minimumAngle(p1, opposite, point)
    angle1 = min(angle1a, angle1b)
    angle2 = min(angle2a, angle2b)
    if angle1 < angle2:
        # Replace edge (p1, p2) with edge (point, opposite)
        t.remove(tr)
        t.remove((p1, p2, point))
        t.append((p1, point, opposite))
        t.append((p2, point, opposite))

        # Legalize the new triangles
        legalizeEdge(p1, point, t, opposite)
        legalizeEdge(p2, point, t, opposite)


# Adds a point to the triangulation, where the given point is in
# the given triangle
def addToTriangulation(point, triangle, t):
    # Remove old triangle
    t.remove(triangle)

    # Add 3 new triangles
    t.append((triangle[0], triangle[1], point))
    t.append((triangle[1], triangle[2], point))
    t.append((triangle[2], triangle[0], point))


# Legalize triangles
# legalizeEdge(triangle[0], triangle[1], t, point)
# legalizeEdge(triangle[1], triangle[2], t, point)
# legalizeEdge(triangle[2], triangle[0], t, point)

# Computes the Delaunay triangulation of a given array of points
def computeDelaunay(points):
    # Initialize triangle T with p0, p1, p2 containing P
    p, t = initializeT(points)

    # Loop through all points
    for point in points:
        # Add point to T
        p.append(point)

        # Add delaunay edges to point
        # tt = t[:]
        for triangle in t:
            # global k
            # k = -1
            # for k in range(len(t)):
            # while k < len(t)-1:
            #	k = k + 1
            if pointInTriangle(point, triangle):
                addToTriangulation(point, triangle, t)
                break
            # t = tt[:]

    # Discard p0, p1, p2 in T and its edges
    extremes = getExtremes(points)
    minx = extremes[0]
    maxx = extremes[1]
    miny = extremes[2]
    maxy = extremes[3]
    newt = []
    for triangle in t:
        b = True
        for i in range(0, 2):
            if triangle[i].x < minx:
                b = False
            if triangle[i].x > maxx:
                b = False
            if triangle[i].y > maxy:
                b = False
        if b:
            newt.append(triangle)

    # Return T
    return t
