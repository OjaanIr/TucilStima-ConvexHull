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

    def __repr__(self):
        return f"({self.x}, {self.y})"  

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
    det = (left.x * right.y + right.x * point.y + point.x * left.y) - (left.y * right.x + right.y * point.x + point.y * left.x)
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
        isClose = np.isclose(distance, 0)
        if (not isClose):
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

def visualization():    
    data = datasets.load_iris()

    #create a DataFrame
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['Target'] = pd.DataFrame(data.target)
    # print(df.shape)
    # df.head()

    #visualisasi hasil myConvexHull
    plt.figure(figsize = (10, 6))
    colors = ['b', 'r', 'g']
    plt.title('Petal Width vs Petal Length')
    plt.xlabel(data.feature_names[0])
    plt.ylabel(data.feature_names[1])
    for i in range(len(data.target_names)):
        bucket = df[df['Target'] == i]
        bucket = bucket.iloc[:,[0,1]].values
        hull = convex_hull(bucket)
        print(hull)
        plt.scatter(bucket[:,0],bucket[:,1], label=data.target_names[i])
        # for simplex in hull.simplices:
        #     plt.plot(bucket[simplex, 0], bucket[simplex,1], colors[i])
    plt.legend()

if __name__ == "__main__":
    visualization()