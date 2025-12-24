import numpy as np
from numpy import sin,cos,radians
import re
# import matplotlib.pyplot as plt
import time
# from mpl_toolkits.mplot3d import Axes3D  # <-- add this
import sys
import argparse
class Fk:
        def __init__(self,L=1,vis=True):
            self.prev_pos=[np.array([i*L,0,0]) for i in range(1,5)]
            self.vis=vis
            if self.vis:
                 self.visulalize(self.prev_pos)
        def Rz(self,theta):
            
            return np.array(
                [
                    [cos(theta),-sin(theta),0],
                    [sin(theta),cos(theta),0],
                    [0,0,1]
                ]
            )
        def Ry(self,theta):
            return np.array(
                [
                    [cos(theta),0,sin(theta)],
                    [0,1,0],
                    [-sin(theta),0,cos(theta)]
                ]
            )
        def process(self,j1,j2,j3,j4,L=1):
            end_point=[np.zeros(3) for _ in range(4)]
            pos=[L,0,0]
            j1=radians(j1)
            R1=self.Rz(j1)
            
            end_point[0]=R1@pos
          
            
            j2=radians(j2)
            R2=self.Ry(j2)
            end_point[1]=end_point[0]+R1@R2@pos
      

            j3=radians(j3)
            R3=self.Rz(j3)
            end_point[2]=end_point[1]+R1@R2@R3@pos
    

            j4=radians(j4)
            R4=self.Ry(j4)
            end_point[3]=end_point[2]+R1@R2@R3@R4@pos
            

            self.prev_pos=np.round(end_point,4)
            # print("the end effector is at ",self.prev_pos[3])
            return self.prev_pos[-1]
            if self.vis:
                 self.visulalize(end_point)
        def on_close(self, event):
            
            print("closing")
            sys.exit(0)
         
        def visulalize(self, endpoints, steps=50):


            new_pts = np.vstack(([np.zeros(3)], endpoints))


            if not hasattr(self, 'fig'):
                plt.ion()
                self.fig = plt.figure()
                self.fig.canvas.mpl_connect('close_event', self.on_close)
                self.ax = self.fig.add_subplot(111, projection='3d')
                self.ax.view_init(elev=90, azim=-90)
                self.ax.set_xlim([-4, 4])
                self.ax.set_ylim([-4, 4])
                self.ax.set_zlim([-4, 4])
                self.ax.set_xlabel('X')
                self.ax.set_ylabel('Y')
                self.ax.set_zlabel('Z')

                xs, ys, zs = new_pts[:, 0], new_pts[:, 1], new_pts[:, 2]
                self.line, = self.ax.plot(xs, ys, zs, '-o', linewidth=3, markersize=8)
                self.texts = [self.ax.text(xs[i+1], ys[i+1], zs[i+1], f'J{i+1}', color='r', fontsize=10)
                            for i in range(len(xs)-1)]
                self.ee_text = self.ax.text(xs[-1], ys[-1], zs[-1], 'EE', color='g', fontsize=10)
                self.prev_pts = new_pts.copy()
                plt.draw()
                plt.pause(0.05)
                return


            old_pts = self.prev_pts
            for alpha in np.linspace(0, 1, steps):
                interp_pts = old_pts + alpha * (new_pts - old_pts)
                xs, ys, zs = interp_pts[:, 0], interp_pts[:, 1], interp_pts[:, 2]

                self.line.set_data(xs, ys)
                self.line.set_3d_properties(zs)

                for i, t in enumerate(self.texts):
                    t.set_position((xs[i+1], ys[i+1]))
                    t.set_3d_properties(zs[i+1])
                self.ee_text.set_position((xs[-1], ys[-1]))
                self.ee_text.set_3d_properties(zs[-1])

                plt.draw()
                plt.pause(0.02)
                if not plt.fignum_exists(self.fig.number):
                    print("Visualization closed.")
                    import sys; sys.exit(0)


            self.prev_pts = new_pts.copy()


             
            



def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-v","--vis",action="store_true")
    args=parser.parse_args()
    vis=args.vis
    obj=Fk(vis=vis)
    try:
        while True:
            inp=input("enter angles j1,j2,j3,j4: ")
            vals=list(map(float,re.split(r'[,\s]+',inp)))

            
            j1,j2,j3,j4=vals
            obj.process(j1,j2,j3,j4)
    except KeyboardInterrupt:
        print("done")
if __name__=="__main__":
    main()  