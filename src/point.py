import math

class Point:
    '''
    Kelas point 
    '''
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def equal(self, other):
        '''
        Menghasilkan true jika self == other
        '''
        return self.x == other.x and self.y == other.y

    def less_than(self, other):
        '''
        Menghasilkan True jika self < other
        '''
        if (self.x < other.x):
            return True
        elif (self.x == other.x):
            return self.y < other.y
        return False

    def more_than(self, other):
        '''
        Menghasilkan True jika self > other
        '''
        if (self.x > other.x):
            return True
        elif (self.x == other.x):
            return self.y > other.y
        return False

    def euclid_dist(self, other):
        '''
        Menghitung jarak antara dua titik 
        '''
        return math.sqrt(pow(self.x-other.x, 2) + (pow(self.y-other.y, 2)))

    def farthest_dist_points(self):
        '''
        Mencari dua titik yang memiliki jarak terjauh
        '''
        n = len(self)
        max = float("-inf")
        p1 = None 
        p2 = None
        for i in range(n):
            for j in range(i+1,n):
                temp1 = self[i]
                temp2 = self[j]
                dist = Point.euclid_dist(temp1,temp2)
                if (max < dist):
                    max = dist
                    p1 = temp1
                    p2 = temp2
        if (Point.less_than(p1,p2)):
            return p1, p2
        else:
            return p2, p1
            

    def __repr__(self):
        return f"({self.x}, {self.y})"  