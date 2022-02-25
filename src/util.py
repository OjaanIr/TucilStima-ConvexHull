from point import Point

def construct_points(list_tuples):
    # Membangun point dari list tuple
    list_points = []
    if list_tuples:
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
    Menghitung determinan yang nantinya nilainya digunakan untuk mengelompokkan titik c,
    terletak di sebelah kiri (atas) atau sebelah kanan (bawah) garis yang dibentuk titik a dan b
    '''
    return (left.x * right.y + right.x * point.y + point.x * left.y) - (left.y * right.x + right.y * point.x + point.y * left.x)

def construct_hull(points, left, right, convex_set):
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
        convex_set.add(extreme_point)
        construct_hull(candidate_points, left, extreme_point, convex_set)
        construct_hull(candidate_points, extreme_point, right, convex_set)