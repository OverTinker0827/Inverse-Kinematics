import numpy as np
from vector import Vector
class IK:
    def __init__(self,joints=None):
        self.joints=joints
    def shift(self,joints,target):
        cur_base_target = np.array(target, dtype=float)
        for joint in joints:
            cur_base_target=joint.move(cur_base_target)

        return joints
    def angle(self,a,b):
        v1 = a.end - a.start
        v2 = b.end - b.start
        denom = np.linalg.norm(v1) * np.linalg.norm(v2)
        if denom == 0:
            return 0.0
        cosang = np.dot(v1, v2) / denom
        cosang = np.clip(cosang, -1.0, 1.0)
        return float(np.arccos(cosang))


    def ik(self,target):
        joints = self.joints
        cur_base = np.array(joints[0].start, dtype=float)
        for _ in range(1000):
            joints = self.shift(joints[::-1], target)
            # print("After shifting:")
            # for j in joints:
            #     print(j.start,j.end)
            joints = self.shift(joints[::-1], cur_base)

        angles = np.empty(0)

        for i in range(len(joints)-1):
            j1, j2 = joints[i], joints[i+1]
            angles = np.append(angles, round(self.angle(j1, j2), 2))
        return angles



j = Vector([0,0,0],[0,0,1])
k = Vector([0,0,1],[0,0,2])
solver=IK([j,k])
print(solver.ik([0,0,1]))

