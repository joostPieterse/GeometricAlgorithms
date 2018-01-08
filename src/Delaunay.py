import math

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
    p0 = Point(-100000, -100000, -1)
    p1 = Point(100000, -100000, -1)
    p2 = Point(0, 100000, -1)
    p.append(p0)
    p.append(p1)
    p.append(p2)
    t.append((p0, p1, p2))

    # Return T
    return p, t


# Computes the angle at p1 from the x-axis to p2
def computeAngle(p1, p2):
    # Compute the distance between p1 and p2
    d = math.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y))

    # Compute and return the angle at p1
    if d == 0:
        return 0
    angle = math.asin(abs(p2.y - p1.y) / d)
    return angle


# Computes the minimum angle in a triangle (p1, p2, p3)
def minimumAngle(p1, p2, p3):
    # Compute the relative angles at the points
    p12 = math.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y))
    p23 = math.sqrt((p3.x - p2.x) * (p3.x - p2.x) + (p3.y - p2.y) * (p3.y - p2.y))
    p31 = math.sqrt((p1.x - p3.x) * (p1.x - p3.x) + (p1.y - p3.y) * (p1.y - p3.y))
    angle1 = math.acos((p12*p12 + p23*p23 - p31*p31) / (2*p12*p23))
    angle2 = math.acos((p23*p23 + p31*p31 - p12*p12) / (2*p23*p31))
    angle3 = math.acos((p31*p31 + p12*p12 - p23*p23) / (2*p31*p12))

    # Return the minimum of the three angles
    return min(angle1, angle2, angle3)

def ccw(a, b, c):
    return (c.y-a.y) * (b.x-a.x) > (b.y-a.y) * (c.x-a.x)

def intersect(p1, p2, t, f1, f2):
    if ccw(p1, f1, f2) != ccw(p2, f1, f2) and ccw(p1, p2, f1) != ccw(p1, p2, f2):
        print("Intersection: ", p1, p2, f1, f2)
        return True
    return False
    
    for tr in t:
        for i in range(0, 2):
            q1 = tr[i]
            q2 = tr[(i+1) % 3]
            if p1 == q1 or p1 == q2 or p2 == q1 or p2 == q2:
                continue
            if q1 == f1 or q1 == f2 or q2 == f1 or q2 == f2:
                continue
            if ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2):
                print("Intersection: ", p1, p2, q1, q2)
                return True
    return False

def rem(t, p1, p2, p3):
    for tr in t:
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

# Legalizes an edge (p1, p2) in a triangulation t, given the third
# point of the triangle including (p1, p2)
def legalizeEdge(p1, p2, t, point):
    q1 = -1
    for tr in t:
        if tr[0] == p1 and tr[1] == p2:
            q1 = tr[2]
        if tr[0] == p2 and tr[1] == p1:
            q1 = tr[2]
        if tr[1] == p1 and tr[2] == p2:
            q1 = tr[0]
        if tr[1] == p2 and tr[2] == p1:
            q1 = tr[0]
        if tr[2] == p1 and tr[0] == p2:
            q1 = tr[1]
        if tr[2] == p2 and tr[0] == p1:
            q1 = tr[1]
    
    if q1 == -1:
        return
    
    q2 = -1
    for tr in t:
        if tr[0] == p1 and tr[1] == p2 and tr[2] != q1:
            q2 = tr[2]
        if tr[0] == p2 and tr[1] == p1 and tr[2] != q1:
            q2 = tr[2]
        if tr[1] == p1 and tr[2] == p2 and tr[0] != q1:
            q2 = tr[0]
        if tr[1] == p2 and tr[2] == p1 and tr[0] != q1:
            q2 = tr[0]
        if tr[2] == p1 and tr[0] == p2 and tr[1] != q1:
            q2 = tr[1]
        if tr[2] == p2 and tr[0] == p1 and tr[1] != q1:
            q2 = tr[1]
    
    if q2 == -1:
        return
    
    # Compute angles
    angle1a = minimumAngle(p1, p2, q1)
    angle1b = minimumAngle(p1, p2, q2)
    angle2a = minimumAngle(p1, q1, q2)
    angle2b = minimumAngle(p2, q1, q2)
    angle1 = min(angle1a, angle1b)
    angle2 = min(angle2a, angle2b)
    print(p1, p2, q1, q2, angle1, angle2)
    if angle1 < angle2 and intersect(q2, q1, t, p1, p2):
        # Replace edge (p1, p2) with edge (point, opposite)
        print("Replace ", p1, p2, q2, "and", p1, p2, q1, " with ", q2, q1, p1, " and ", q2, q1, p2)
        rem(t, p1, p2, q1)
        rem(t, p1, p2, q2)
        t.append((p1, q2, q1))
        t.append((p2, q2, q1))

        # Legalize the new triangles
        if point == q1:
            legalizeEdge(p1, q2, t, point)
            legalizeEdge(p2, q2, t, point)
        else:
            legalizeEdge(p1, q1, t, point)
            legalizeEdge(p2, q1, t, point)

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
    legalizeEdge(triangle[0], triangle[1], t, point)
    legalizeEdge(triangle[1], triangle[2], t, point)
    legalizeEdge(triangle[2], triangle[0], t, point)

# Computes the Delaunay triangulation of a given array of points
def computeDelaunay(points):
    # Initialize triangle T with p0, p1, p2 containing P
    p, t = initializeT(points)

    # Loop through all points
    for point in points:
        # Add point to T
        p.append(point)

        # Add delaunay edges to point
        for triangle in t:
            if pointInTriangle(point, triangle):
                addToTriangulation(point, triangle, t)
                break
    
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
            if triangle[i].x < -90000:
                b = False
            if triangle[i].x > 90000:
                b = False
            if triangle[i].y > 90000:
                b = False
        if b:
            newt.append(triangle)

    # Return T
    return newt
