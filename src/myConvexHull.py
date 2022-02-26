from point import Point
import numpy as np

def tuples_to_points(list_tuples):
    '''
    Konversi tipe menjadi point
    '''
    points: list[Point] = []
    for p in list_tuples:
        if isinstance(p, Point):
            points.append(p)
        else:
            try:
                points.append(Point(p[0], p[1]))
            except (IndexError, TypeError):
                print("Points must have at least 2 coordinates")
    return points

def determinant(a, b, c):
    '''
    Menghitung determinan yang nantinya nilainya digunakan untuk mengelompokkan titik point,
    terletak di sebelah atas atau bawah garis yang dibentuk titik left dan right 
    '''
    det = (a.x * b.y + b.x * c.y + c.x * a.y) - (a.y * b.x + b.y * c.x + c.y * a.x)
    return det

def construct_convex_hull(points, left, right, convex_set):
    '''
    Mengupdate convex_set apabila terdapat point yang memenuhi syarat untuk dapat
    membentuk convex hull 
    '''
    extreme_point = None
    extreme_distance = float("-inf")
    candidate_points = []
    for point in points:
        distance = determinant(left, right, point)
        if (distance > 0):
            candidate_points.append(point)
            if (distance > extreme_distance):
                extreme_distance = distance
                extreme_point = point
    if extreme_point:
        construct_convex_hull(candidate_points, left, extreme_point, convex_set)
        convex_set.add(extreme_point)
        construct_convex_hull(candidate_points, extreme_point, right, convex_set)

def convex_hull(points):
    '''
    Menentukan convex hull
    '''
    points = sorted(tuples_to_points(points))
    total_points = len(points)

    leftmost_point = points[0]
    rightmost_point = points[total_points-1]

    res = {leftmost_point, rightmost_point}
    upper_hull = []
    lower_hull = []

    for i in range(1, total_points-1):
        distance = determinant(leftmost_point, rightmost_point, points[i])
        if (distance > 0):
            upper_hull.append(points[i])
        else:
            lower_hull.append(points[i])

    # Divide & conquer
    construct_convex_hull(upper_hull, leftmost_point, rightmost_point, res)
    construct_convex_hull(lower_hull, rightmost_point, leftmost_point, res)

    return sorted(res)