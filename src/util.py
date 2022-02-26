from point import Point

def tuples_to_points(list_tuples):
    '''
    Konversi tipe menjadi point
    '''
    list_points = []
    for t in list_tuples:
        if isinstance(t, Point):
            list_points.append(t)
        else:
            try:
                list_points.append(Point(t[0], t[1]))
            except (IndexError, TypeError):
                print("Points must have at least 2 coordinates")
    return list_points

def determinant(left, right, point):
    '''
    Menghitung determinan yang nantinya nilainya digunakan untuk mengelompokkan titik point,
    terletak di sebelah atas atau bawah garis yang dibentuk titik left dan right 
    '''
    return (left.x * right.y + right.x * point.y + point.x * left.y) - (left.y * right.x + right.y * point.x + point.y * left.x)

def convex_hull(points, left, right, convex_set):
    '''
    Mengupdate convex_set apabila terdapat point yang memenuhi syarat untuk dapat
    membentuk convex hull 
    '''
    extreme_point = None
    extreme_distance = float("-inf")
    candidate_points = []
    for point in points:
        if (not (Point.equal(left, point) or Point.equal(right, point))):
            distance = determinant(left, right, point)
            if (distance > 0):
                candidate_points.append(point)
                if (distance > extreme_distance):
                    extreme_distance = distance
                extreme_point = point
    if extreme_point:
        convex_hull(candidate_points, left, extreme_point, convex_set)
        convex_set.add(extreme_point)
        convex_hull(candidate_points, extreme_point, right, convex_set)

def myConvexHull(points):
    '''
    Menentukan convex hull
    '''
    points = tuples_to_points(points)
    total_points = len(points)

    leftmost_point, rightmost_point = Point.farthest_dist_points(points)

    res = {leftmost_point, rightmost_point}
    upper_hull = []
    lower_hull = []

    for point in points:
        distance = determinant(leftmost_point, rightmost_point, point)
        if (distance > 0):
            upper_hull.append(point)
        else:
            lower_hull.append(point)

    # Divide & conquer
    convex_hull(upper_hull, leftmost_point, rightmost_point, res)
    convex_hull(lower_hull, rightmost_point, leftmost_point, res)

    return res