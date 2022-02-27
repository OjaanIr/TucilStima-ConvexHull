import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets

class Point:
    '''
    Kelas point 
    '''
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if self.x > other.x:
            return True
        elif self.x == other.x:
            return self.y > other.y
        return False

    def __lt__(self, other):
        return not self > other

    def __ge__(self, other):
        if self.x > other.x:
            return True
        elif self.x == other.x:
            return self.y >= other.y
        return False

    def __le__(self, other):
        if self.x < other.x:
            return True
        elif self.x == other.x:
            return self.y <= other.y
        return False

    def __hash__(self):
        return hash(self.x) 

def tuples_to_points(list_tuples):
    '''
    Konversi tipe menjadi point
    '''
    list_points = []
    for tuple in list_tuples:
        if isinstance(tuple, Point):
            list_points.append(tuple)
        else:
            try:
                list_points.append(Point(tuple[0], tuple[1]))
            except (IndexError, TypeError):
                print("Points must have at least 2 coordinates")
    return list_points

def determinant(left, right, point):
    '''
    Menghitung determinan yang nantinya nilainya digunakan untuk mengelompokkan titik point,
    terletak di sebelah atas atau bawah garis yang dibentuk titik left dan right 
    '''
    return (left.x * right.y + right.x * point.y + point.x * left.y) - (left.y * right.x + right.y * point.x + point.y * left.x)

def construct_convex_hull(points, left, right, hull):
    '''
    Mengupdate hull apabila terdapat point yang memenuhi syarat untuk dapat
    membentuk convex hull 
    '''
    extreme_point = None
    extreme_distance = float("-inf")
    candidate_points = []
    for point in points:
        distance = determinant(left, right, point)
        isClose = np.isclose(distance, 0)
        if (not isClose):
            if (distance > 0):
                candidate_points.append(point)
                if (distance > extreme_distance):
                    extreme_distance = distance
                    extreme_point = point
    if extreme_point:
        construct_convex_hull(candidate_points, left, extreme_point, hull)
        hull.append(extreme_point)
        construct_convex_hull(candidate_points, extreme_point, right, hull)

def convex_hull(points):
    '''
    Menentukan convex hull
    '''
    sorted_points = sorted(tuples_to_points(points))
    total_points = len(points)

    # Mengambil titik yang terletak di absis paling kiri dan kanan
    leftmost_point = sorted_points[0]
    rightmost_point = sorted_points[total_points-1]

    # List convex hull
    upper_res = [leftmost_point, rightmost_point]
    lower_res = [leftmost_point, rightmost_point]
    # Menginisialisasi list untuk menyimpan titik-titik yang berada di atas dan di bawah
    # garis yang dibentuk titik leftmost_point dan rightmost_point
    upper_area = []
    lower_area = []

    # Menyimpan titik yang memenuhi syarat ke list upper _area atau lower_area
    for i in range(1, total_points-1):
        distance = determinant(leftmost_point, rightmost_point, sorted_points[i])
        # Append point ke list upper_area apabila nilai distance > 0
        if (distance > 0):
            upper_area.append(sorted_points[i])
        # Append point ke list lower_area apabila nilai distance <= 0
        else:
            lower_area.append(sorted_points[i])

    # Divide & conquer (mengonstruksi convex hull untuk upper_area dan lower_area)
    construct_convex_hull(upper_area, leftmost_point, rightmost_point, upper_res)
    construct_convex_hull(lower_area, rightmost_point, leftmost_point, lower_res)

    return sorted(upper_res), sorted(lower_res)

def construct_indices(points, points_convex_hull):
    '''
    Menyimpan indeks dan koordinat x points, jika elemen point di points sama dengan point di points_convex_hull
    '''
    points = tuples_to_points(points)
    indices = []

    for point in points_convex_hull:
        for i in range (len(points)):
            if point == points[i]:
                indices.append(i)
    
    return indices

def construct_simplices(upper, lower, points):
    '''
    Mengonstruksi simplices (pasangan indeks) dengan tujuan visualisasi nanti
    '''
    upper_indices = construct_indices(points, upper)
    lower_indices = construct_indices(points, lower)
    simplices = []

    # upper
    for i in range (len(upper_indices)-1):
        simplices.append([upper_indices[i],upper_indices[i+1]])
    simplices.append([upper_indices[i],upper_indices[i+1]])

    #lower
    for i in range (len(lower_indices)-1):
        simplices.append([lower_indices[i],lower_indices[i+1]])
    simplices.append([lower_indices[i],lower_indices[i+1]])

    return simplices    
    
def visualization():    
    data = datasets.load_iris()

    #create a DataFrame
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['Target'] = pd.DataFrame(data.target)

    #visualisasi hasil myConvexHull
    plt.figure(figsize = (10, 6))
    colors = ['b', 'r', 'g']
    plt.title('Petal Width vs Petal Length')
    plt.xlabel(data.feature_names[0])
    plt.ylabel(data.feature_names[1])
    for i in range(len(data.target_names)):
        bucket = df[df['Target'] == i]
        bucket = bucket.iloc[:,[0,1]].values
        upper, lower = convex_hull(bucket)
        simplices = construct_simplices(upper, lower, bucket)
        plt.scatter(bucket[:,0],bucket[:,1], label=data.target_names[i])
        for simplex in simplices:
            plt.plot(bucket[simplex, 0], bucket[simplex,1], colors[i])
    plt.legend()

if __name__ == "__main__":
    visualization()