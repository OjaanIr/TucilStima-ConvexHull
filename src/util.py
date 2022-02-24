from point import Point

def construct_points(list_tuples):
    # Membangun point dari list tuple
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

def validate_inputs(points):
    # Memvalidasi input
    if not hasattr(points, "__iter__"):
        raise ValueError(f"Expecting an iterable object but got an non-iterable type {points}")
    
    if not points:
        raise ValueError(f"Expecting a list of points but got {points}")

    return construct_points(points)

def determinant(a, b, c):
    '''
    Menghitung determinan yang nantinya nilainya digunakan untuk mengelompokkan titik c,
    terletak di sebelah kiri (atas) atau sebelah kanan (bawah) garis yang dibentuk titik a dan b
    '''
    return (a.x * b.y + b.x * c.y + c.x * a.y) - (a.y * b.x + b.y * c.x + c.y * a.x)