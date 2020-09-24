import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np

l1 = 2 #length of the first limb
l2 = 2 #length of the second limb

total_length = l1 + l2

# lets plot a double pendulum with initial angle of -45 and -90 (anti-clockwise)
## important to note that numpy trig methods use radian values
th1 = np.radians(315)
x1 = l1 * np.cos(th1)
y1 = l1 * np.sin(th1)

th2 = np.radians(270)
x2 = x1+l2 * np.cos(th2)
y2 = y1+l2 * np.sin(th2)

# did I really have to do this? No. Did I still do it? Yes. It's good practice.
x = [0,x1,x2]
y = [0,y1,y2]

# angle markers
angle1 = Arc((0,0), height=1, width=1, angle=0, theta1=0, theta2=315, color='grey')
angle2 = Arc((x[1],y[1]), height=1, width=1, angle=0, theta1=0, theta2=270, color='grey')

fig, ax = plt.subplots()

# set up aspect ratio, axes limits, grid, figure size and dpi
ax.set_aspect('equal')
ax.set_xlim(-total_length,total_length)
ax.set_ylim(-total_length,total_length)
ax.grid(True)
fig.set_dpi(100)
fig.set_size_inches((7,7))

# @TODO: find numpy documentation of array slicing
# plot the two limbs of the pendulum
ax.plot(x[0:2],y[0:2],'g-') #what a lot of beginners fail to understand is how to slice mumpy arrays 
ax.text(x[1]-0.8,y[1]+1, r'Limb 1') 
ax.plot(x[1:],y[1:],'b-')
ax.text(x[2]+0.4,y[2]+1, r'Limb 2') 
# plot the joints
ax.plot(x[0],y[0],'co') #fixed point/joint
ax.plot(x[1],y[1],'mo') #joint between the two limbs
ax.plot(x[2],y[2],'yo') #end of the second limb

# add patches for angles markers
ax.add_patch(angle1)
ax.add_patch(angle2)

# add axis for second angle marker
ax.plot([x1-0.6, x1+0.6], [y1, y1], [x1, x1], [y1-0.6, y1+0.6], color='grey', linestyle='-', lw=0.4)

# Add text
ax.text(0.4, 0.4, r'$\theta_{1}$')
ax.text(x1+0.4, y1+0.4, r'$\theta_{2}$')

plt.show()
# plt.savefig('double-pendulum-drawing.png')
