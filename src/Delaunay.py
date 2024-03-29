import math
import random

from Point import Point
from Triangle import Triangle

# Used for pointInTriangle()
def sign(q, p1, p2):
    return (q.x - p2.x) * (p1.y - p2.y) - (p1.x - p2.x) * (q.y - p2.y)


# Checks whether or not a point p is in a triangle t
def pointInTriangle(p, t):
    b1 = sign(p, t.p0, t.p1) < 0
    b2 = sign(p, t.p1, t.p2) < 0
    b3 = sign(p, t.p2, t.p0) < 0
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
    t = []
    d = {}

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
    p0 = Point(-100000, -100000, -1)
    p1 = Point(100000, -100000, -1)
    p2 = Point(0, 100000, -1)
    tr = Triangle(p0, p1, p2)
    t.append(tr)

    # Update the dictionary
    d[(p0, p1)] = [tr]
    d[(p1, p2)] = [tr]
    d[(p2, p0)] = [tr]

    # Return T
    return t, d


# Computes the angle at p1 from the x-axis to p2
def computeAngle(p1, p2):
    # Compute the distance between p1 and p2
    d = math.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y))

    # Compute and return the angle at p1
    if d == 0:
        return 0
    v = abs(p2.y - p1.y) / d
    v = max(-1, min(v, 1))
    angle = math.asin(v)
    return angle


# Computes the minimum angle in a triangle (p1, p2, p3)
def minimumAngle(p1, p2, p3):
    # Compute the relative angles at the points
    p12 = math.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y))
    p23 = math.sqrt((p3.x - p2.x) * (p3.x - p2.x) + (p3.y - p2.y) * (p3.y - p2.y))
    p31 = math.sqrt((p1.x - p3.x) * (p1.x - p3.x) + (p1.y - p3.y) * (p1.y - p3.y))
    d1 = 2*p12*p23
    d2 = 2*p23*p31
    d3 = 2*p31*p12
    if d1 == 0 or d2 == 0 or d3 == 0: return math.inf
    v1 = (p12*p12 + p23*p23 - p31*p31) / d1
    v2 = (p23*p23 + p31*p31 - p12*p12) / d2
    v3 = (p31*p31 + p12*p12 - p23*p23) / d3
    v1 = max(-1, min(v1, 1))
    v2 = max(-1, min(v2, 1))
    v3 = max(-1, min(v3, 1))
    angle1 = math.acos(v1)
    angle2 = math.acos(v2)
    angle3 = math.acos(v3)

    # Return the minimum of the three angles
    return min(angle1, angle2, angle3)

# Required by intersect()
def ccw(a, b, c):
    return (c.y-a.y) * (b.x-a.x) > (b.y-a.y) * (c.x-a.x)

# Checks if two line segments intersect
def intersect(p1, p2, q1, q2):
    if ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2):
        return True
    return False

# Removes a triangle from t given its three points
def rem(t, p1, p2, p3):
	# Loop through all triangles
    for tr in t:
		# Check if this triangle is defined by the same three points
        if tr[0] == p1 and tr[1] == p2 and tr[2] == p3:
            t.remove(tr)
            return
        if tr[0] == p1 and tr[1] == p3 and tr[2] == p2:
            t.remove(tr)
            return
        if tr[0] == p2 and tr[1] == p1 and tr[2] == p3:
            t.remove(tr)
            return
        if tr[0] == p2 and tr[1] == p3 and tr[2] == p1:
            t.remove(tr)
            return
        if tr[0] == p3 and tr[1] == p1 and tr[2] == p2:
            t.remove(tr)
            return
        if tr[0] == p3 and tr[1] == p2 and tr[2] == p1:
            t.remove(tr)
            return
    print("---")
    print("Rem: Triangle not found")
    print("---")

# Checks if an edge is incident to a triangle
def edgeOnTriangle(p0, p1, triangle):
    if triangle.p0 == p0 and triangle.p1 == p1: return triangle.p2
    if triangle.p0 == p0 and triangle.p2 == p1: return triangle.p1
    if triangle.p1 == p0 and triangle.p0 == p1: return triangle.p2
    if triangle.p1 == p0 and triangle.p2 == p1: return triangle.p0
    if triangle.p2 == p0 and triangle.p0 == p1: return triangle.p1
    if triangle.p2 == p0 and triangle.p1 == p1: return triangle.p0
    return False

# Legalizes an edge (p0, p1) in a triangulation t, given the third
# point of the triangle including (p0, p1)
def legalizeEdge(p0, p1, p2, t, d):
    # Find two triangles connected to edge (p0, p1)
    triangles = d[(p0, p1)] if (p0, p1) in d else d[(p1, p0)]
    q1 = -1
    q2 = -1
    t1 = -1
    t2 = -1
    for tr in triangles:
        pp2 = edgeOnTriangle(p0, p1, tr)
        if pp2 != False and q1 == -1:
            q1 = pp2
            t1 = tr
            continue
        if pp2 != False and q1 != -1:
            q2 = pp2
            t2 = tr

    # Do nothing if the edge does not have a second triangle
    if q1 == -1 or q2 == -1:
        return

    # Compute angles
    angleoriga = minimumAngle(p0, p1, q1)
    angleorigb = minimumAngle(p0, p1, q2)
    angleflipa = minimumAngle(p0, q1, q2)
    angleflipb = minimumAngle(p1, q1, q2)
    angleorig = min(angleoriga, angleorigb)
    angleflip = min(angleflipa, angleflipb)
    if angleorig < angleflip and intersect(p0, p1, q1, q2):
        # Replace edge (p1, p2) with edge (point, opposite)
        removeTriangle(t1, t, d)
        removeTriangle(t2, t, d)
        addTriangle(p0, q1, q2, t, d)
        addTriangle(p1, q1, q2, t, d)

        # Legalize the new triangles
        if p2 == q1:
            legalizeEdge(p0, q2, q1, t, d)
            legalizeEdge(p1, q2, q1, t, d)
        else:
            legalizeEdge(p0, q1, q2, t, d)
            legalizeEdge(p1, q1, q2, t, d)

# Checks if two triangles are equal in terms of their three points
def isTriangle(t0, t1):
    if t1 == None: return False
    if t0.p0 == t1.p0 and t0.p1 == t1.p1 and t0.p2 == t1.p2: return True
    if t0.p0 == t1.p0 and t0.p1 == t1.p2 and t0.p2 == t1.p1: return True
    if t0.p0 == t1.p1 and t0.p1 == t1.p0 and t0.p2 == t1.p2: return True
    if t0.p0 == t1.p1 and t0.p1 == t1.p2 and t0.p2 == t1.p0: return True
    if t0.p0 == t1.p2 and t0.p1 == t1.p0 and t0.p2 == t1.p1: return True
    if t0.p0 == t1.p2 and t0.p1 == t1.p1 and t0.p2 == t1.p0: return True
    return False

# Gets the point of a triangle not equal to the two given other points,
# assuming that p0 and p1 are on triangle.
def getPoint(triangle, p0, p1):
    if triangle.p0 == p0 and triangle.p1 == p1: return triangle.p2
    if triangle.p0 == p0 and triangle.p2 == p1: return triangle.p1
    if triangle.p1 == p0 and triangle.p0 == p1: return triangle.p2
    if triangle.p1 == p0 and triangle.p2 == p1: return triangle.p0
    if triangle.p2 == p0 and triangle.p0 == p1: return triangle.p1
    if triangle.p2 == p0 and triangle.p1 == p1: return triangle.p0

# Returns whether or not a given point is above a given line, or
# to the right of it should it be vertical.
def pointAboveLine(line0, line1, point):
    # Verify that the line is not vertical
    if line0.x == line1.x:
        return point.x > line1.x

    # Compute the slope of the line
    m = (line1.y - line0.y) / (line1.x - line0.x)
    k = line1.y - m*line1.x

    # Check if the point is above or below the line
    if m * point.x + k < point.y:
        # Point is above the line
        return True
    else:
        # Point is below the line
        return False

# Returns the triangle in which a given point is located
def pointLocation(point, p0, p1, p2, triangle, t, d, pointLocationMethod):
    if pointLocationMethod == "O(n)":
        for tr in t:
            if pointInTriangle(point, tr):
                return tr
    #print("---")
    #print("PointLocation: Point does not lie in any triangle")
    #print("---")

	# The code below is an implementation of Point Location by walking
	# through the triangulation, which is more efficient than the above
	# code, which simply loops through all triangles and checks if the
	# point is inside. However, the more efficient code below is prone
	# to errors when three or more points are near colinear, because of
	# rounding errors.

    # Find an edge that separates point from the triangle
    else:
        if pointAboveLine(p1, p2, point) != pointAboveLine(p1, p2, p0):
            # Find the other triangle connected to edge (p1, p2)
            triangles = d[(p1, p2)] if (p1, p2) in d else d[(p2, p1)]
            for tr in triangles:
                if not isTriangle(triangle, tr):
                    q = getPoint(tr, p1, p2)
                    return pointLocation(point, p1, p2, q, tr, t, d, pointLocationMethod)
        if pointAboveLine(p0, p2, point) != pointAboveLine(p0, p2, p1):
            # Find the other triangle connected to edge (p0, p2)
            triangles = d[(p0, p2)] if (p0, p2) in d else d[(p2, p0)]
            for tr in triangles:
                if not isTriangle(triangle, tr):
                    q = getPoint(tr, p0, p2)
                    return pointLocation(point, p0, p2, q, tr, t, d, pointLocationMethod)

        # No edge separates point from the triangle, so point is in this triangle
        return triangle

# Removes a triangle, both from the triangle list and the dictionary
def removeTriangle(triangle, t, d):
    # Get the three points of the triangle to remove
    p0 = triangle.p0
    p1 = triangle.p1
    p2 = triangle.p2

    # Remove the old triangle from the dictionary
    if (p0, p1) in d:
        if triangle in d[(p0, p1)]: d[(p0, p1)].remove(triangle)
    if (p1, p0) in d:
        if triangle in d[(p1, p0)]: d[(p1, p0)].remove(triangle)
    if (p1, p2) in d:
        if triangle in d[(p1, p2)]: d[(p1, p2)].remove(triangle)
    if (p2, p1) in d:
        if triangle in d[(p2, p1)]: d[(p2, p1)].remove(triangle)
    if (p2, p0) in d:
        if triangle in d[(p2, p0)]: d[(p2, p0)].remove(triangle)
    if (p0, p2) in d:
        if triangle in d[(p0, p2)]: d[(p0, p2)].remove(triangle)

    # Remove the old triangle from the triangulation
    if triangle in t: t.remove(triangle)

# Adds a triangle to the dictionary given an edge
def addToDictionary(p0, p1, triangle, d):
    if (p0, p1) in d:
        d[(p0, p1)].append(triangle)
        return
    if (p1, p0) in d:
        d[(p1, p0)].append(triangle)
        return
    d[(p0, p1)] = [triangle]

# Adds a triangle, both to the triangle list and the dictionary
def addTriangle(p0, p1, p2, t, d):
    # Create a new triangle
    triangle = Triangle(p0, p1, p2)

    # Add the triangle to t
    t.append(triangle)

    # Add the three edges to the dictionary
    addToDictionary(p0, p1, triangle, d)
    addToDictionary(p1, p2, triangle, d)
    addToDictionary(p2, p0, triangle, d)

# Adds a point to the triangulation, where the given point is in
# the given triangle
def addToTriangulation(point, t, d, pointLocationMethod):
    # Search in which triangle point lies
    triangle = pointLocation(point, t[0].p0, t[0].p1, t[0].p2, t[0], t, d, pointLocationMethod)

    # Remove old triangle
    removeTriangle(triangle, t, d)

    # Add 3 new triangles
    addTriangle(triangle.p0, triangle.p1, point, t, d)
    addTriangle(triangle.p1, triangle.p2, point, t, d)
    addTriangle(triangle.p2, triangle.p0, point, t, d)

    # Legalize triangles
    legalizeEdge(triangle.p0, triangle.p1, point, t, d)
    legalizeEdge(triangle.p1, triangle.p2, point, t, d)
    legalizeEdge(triangle.p2, triangle.p0, point, t, d)

# Returns whether or not the given triangle is a "main" triangle.
# Every triangle is a main triangle, except for the initial outer triangle.
def isMainTriangle(triangle):
    if triangle.p0.x < -90000: return False
    if triangle.p0.x >  90000: return False
    if triangle.p0.y >  90000: return False
    if triangle.p1.x < -90000: return False
    if triangle.p1.x >  90000: return False
    if triangle.p1.y >  90000: return False
    if triangle.p2.x < -90000: return False
    if triangle.p2.x >  90000: return False
    if triangle.p2.y >  90000: return False
    return True

# Computes the Delaunay triangulation of a given array of points
def computeDelaunay(points, pointLocationMethod):
    # Initialize triangle T with p0, p1, p2 containing P
    t, d = initializeT(points)

    # Loop through all points
    for point in points:
        # Add point to the triangulation
        addToTriangulation(point, t, d, pointLocationMethod)

    # Discard p0, p1, p2 in T and its edges
    extremes = getExtremes(points)
    minx = extremes[0]
    maxx = extremes[1]
    miny = extremes[2]
    maxy = extremes[3]
    newt = []
    for triangle in t:
        if isMainTriangle(triangle):
            newt.append((triangle.p0, triangle.p1, triangle.p2))

    # Return T
    return newt
