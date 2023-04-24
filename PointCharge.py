import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
import sympy as smp
import plotly.graph_objects as go
from IPython.display import HTML

# define the variable where to calculate the electric field on the charged shape
t = smp.symbols('t', positive=True)
# define our variables
x, y, z = smp.symbols('x y z')
# define the vector position where you are
r = smp.Matrix([x, y, z])
# define where the charged shape is located
print('Enter the coordinates of the location where is the charged shape')
xpos = input("enter the x component\n")
ypos = input("enter the y component\n")
zpos = input("enter the z component\n")



# initialize the vector of the charged shape location
r_p = smp.Matrix([xpos, ypos, zpos])
# calculate the distance and initilaize it in a vector
sep = r - r_p

# get the total charge
q = input("Enter the total charge of the shape \n ")
Q = float(q)

# diferntiate the r' over t
dr_pdt = smp.diff(r_p, t).norm().simplify()



integrand = 9e9* Q * sep/sep.norm()**2
dExdt = smp.lambdify([t, x, y, z], integrand[0])
dEydt = smp.lambdify([t, x, y, z], integrand[1])
dEzdt = smp.lambdify([t, x, y, z], integrand[2])
def E(x, y, z):
    return np.array([quad(dExdt, 0, 2*np.pi, args=(x, y, z))[0],
                     quad(dEydt, 0, 2*np.pi, args=(x, y, z))[0],
                     quad(dEzdt, 0, 2*np.pi, args=(x, y, z))[0]])

x = np.linspace(-2, 2, 10)
y = np.linspace(-2, 2, 10)
z = np.linspace(0, 2*np.pi, 10)
xv, yv, zv = np.meshgrid(x, y, z)

E_field = np.vectorize(E, signature='(),(),()->(n)')(xv, yv, zv)
Ex = E_field[:,:,:,0]
Ey = E_field[:,:,:,1]
Ez = E_field[:,:,:,2]

plt.hist(Ex.ravel(), bins=100, histtype='step',label='Ex')
plt.hist(Ey.ravel(), bins=100, histtype='step',label='Ey')
plt.hist(Ez.ravel(), bins=100, histtype='step',label='Ez')
plt.legend()
plt.xlabel('Electric Field Magnitude')
plt.ylabel('Frequency')
plt.show()

E_max = 150
Ex[Ex>E_max] = E_max
Ey[Ey>E_max] = E_max
Ez[Ez>E_max] = E_max

Ex[Ex<-E_max] = -E_max
Ey[Ey<-E_max] = -E_max
Ez[Ez<-E_max] = -E_max


tt = np.linspace(0, 50000, 1000)



lx, ly, lz = xpos, ypos, zpos
data = go.Cone(x=xv.ravel(), y=yv.ravel(), z=zv.ravel(),
               u=Ex.ravel(), v=Ey.ravel(), w=Ez.ravel(),
               colorscale='Inferno', colorbar=dict(title='$x^2$'),
               sizemode="scaled", sizeref=0.5)

layout = go.Layout(title=r'Plot Title',
                     scene=dict(xaxis_title=r'x',
                                yaxis_title=r'y',
                                zaxis_title=r'z',
                                aspectratio=dict(x=1, y=1, z=1),
                                camera_eye=dict(x=1.2, y=1.2, z=1.2)))

fig = go.Figure(data = data, layout=layout)
fig.add_scatter3d(x=[lx], y=[ly], z=[lz])


HTML(fig.to_html(default_width=1000, default_height=600))

fig.show()