import util

def myConvexHull(points):
    # Menentukan convex hull
    sorted_points = sorted(util.construct_points(points))
    total_points = len(sorted_points)

    leftmost_point = sorted_points[0]
    rightmost_point = sorted_points[total_points-1]

    convex_hull = {leftmost_point, rightmost_point}
    upper_hull = []
    lower_hull = []

    for point in sorted_points:
        distance = util.determinant(leftmost_point, rightmost_point, point)
        if (distance > 0):
            upper_hull.append(point)
        else:
            lower_hull.append(point)

    util.construct_hull(upper_hull, leftmost_point, rightmost_point, convex_hull)
    util.construct_hull(lower_hull, rightmost_point, leftmost_point, convex_hull)

    return sorted(convex_hull)