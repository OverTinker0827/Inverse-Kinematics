import numpy as np
class Vector:

    def __init__(self, start, end):
        self.start = np.array(start, dtype=float)
        self.end = np.array(end, dtype=float)
    def length(self):
        return np.linalg.norm(self.end - self.start)
    
    def direction(self,start_point,end_point):
        return np.array(end_point, dtype=float) - np.array(start_point, dtype=float)
    def magnitude(self,v):
        return np.linalg.norm(v)

    def move(self,start_point):
        # print("old start:",self.start,"old end:",self.end)
        cur_start = self.start
        cur_end = self.end
        l = self.length()
        start_point = np.array(start_point, dtype=float)
        self.start = start_point
        # print("diirection calc from:",start_point,cur_start)

        dir = self.direction( start_point,cur_start)
        print(start_point,cur_start,dir)
        if self.magnitude(dir) == 0:
            # print(start_point,cur_start,dir)
            return cur_end
        # print("direction:",dir)
        end_points = start_point + l * dir / self.magnitude(dir)
        self.end = end_points
        # print("new start:",self.start,"new end:",self.end)
        return end_points