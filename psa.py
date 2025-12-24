import numpy as np
from fk import Fk

class PSA:
    def __init__(self,joints):
        self.joints = joints
        self.dim=len(joints)
        
    
    def optimize(self,iterations,N,a,b,c,target):
        dim=self.dim
        pos=np.array([[np.random.uniform(0,180) for _ in range(dim)] for _ in range(N)])
  
        vel=np.array([[0 for _ in range(dim)] for _ in range(N)])
        best_pos=pos.copy()
        local_min_pos=pos.copy()
        for _ in range(iterations):
            
            best_pos=pos[np.argmin([self.evaluate(p,target) for p in pos])]


            for i in range(N):
                r1,r3=np.random.uniform(),np.random.uniform()
                vel[i]= (a*vel[i] + b*r1*(best_pos-pos[i]) + c*r3*(local_min_pos[i]-pos[i]))
                local_min_pos[i]=pos[i] if self.evaluate(pos[i],target)<self.evaluate(local_min_pos[i],target) else local_min_pos[i]

                pos[i]=pos[i]+vel[i]

        return best_pos
    def evaluate(self,pos,target):
        if any(abs(j) >180 for j in pos):
            return float('inf')
        fk=Fk(L=1,vis=False)
        final_pos=fk.process(*pos,L=1)
        # print(np.linalg.norm(final_pos - np.array(self.target)))
        return 100*np.linalg.norm(final_pos - np.array(target))
        
    
solver=PSA([[1,0,0],[2,0,0],[3,0,0],[4,0,0]])
best_parameters=solver.optimize(iterations=10000,N=200,a=0.70,b=1.2,c=1.9,target=[0,4,0])
print(best_parameters)
best_parameters=np.round(best_parameters,2)
value=solver.evaluate(best_parameters,target=[0,4,0])
print("Best Parameters:",best_parameters)
print("Final Position Error:",value)
