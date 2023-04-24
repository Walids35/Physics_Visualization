import numpy as np
from scipy.integrate import quad
import plotly.graph_objects as go
from IPython.display import HTML

np.seterr(divide='ignore', invalid='ignore')

# grid size
N = 25
M = 25
U = 25
# coordinates
X = np.arange(0, M, 1)
Y = np.arange(0, N, 1)
Z = np.arange(0, U, 1)
X, Y,Z = np.meshgrid(X, Y,Z)
# strength
Ex = np.zeros((N, M,U))
Ey = np.zeros((N, M,U))
Ez = np.zeros((N, M,U))
# amount of charges
nq = int(input('Enter the number of point charges\n'))
#nq = 3

# computing
qq = [[], [],[]]  # to store charges coordinates

t = 0
while t in range(nq):
    q = float(input('enter the charge of the point charge\n'))
    qx = float(input('Enter the x coordinate component of the point charge (max 15 )'))
    qy = float(input('Enter the y coordinate component of the point charge (max 25)'))
    qz = float(input('Enter the z coordinate component of the point charge (max 25)'))

    #qx, qy = random.randrange(1, N), random.randrange(1, M)
    # print(q, qx, qy)
    qq[0].append(qz)
    qq[1].append(qy)
    qq[2].append(qx)
    t =t +1

    for i in range(N):
        for j in range(M):
            for k in range(U):
                denom = ((i - qx) ** 2 + (j - qy) ** 2 + ( k - qz) ** 2) ** 1.5
                if denom != 0:
                    Ex[i, j,k] += q * (k - qy) / denom
                    Ey[i, j,k] += q * (j - qx) / denom
                    Ez[i,j,k] += q * (i - qx) / denom

# arrows color
C = np.hypot(Ex, Ey,Ez)
# normalized values for arrows to be of equal length
E = (Ex ** 2 + Ey ** 2 + Ez**2) ** .5
Ex = Ex / E
Ey = Ey / E
Ez = Ez / E

def E(x, y, z):
    denom = ((x - qx) ** 2 + (y - qy) ** 2 + ( z - qz) ** 2) ** 1.5
    ElectricX = q * (z - qy) / denom
    ElectricY = q * (y - qx) / denom
    ElectricZ = q * (x - qx) / denom
    return np.array([quad(ElectricX, args=(x, y, z))[0],
                     quad(ElectricY, args=(x, y, z))[0],
                     quad(ElectricZ, args=(x, y, z))[0]])
x = np.linspace(-N, N)
y = np.linspace(-M, M)
z = np.linspace(-U, U)
xv, yv, zv = np.meshgrid(x, y, z)

E_field = np.vectorize(E, signature='(),(),()->(n)')(xv, yv, zv)
Ex = E_field[:,:,:,0]
Ey = E_field[:,:,:,1]
Ez = E_field[:,:,:,2]

# drawing
#plt.figure(figsize=(12, 8))


# charges
#plt.plot(*qq, 'bo')
# field

#plt.quiver(X, Y, Ex, Ey, C, pivot='mid')
#draw cones
data= go.Cone(x=xv.ravel(), y=yv.ravel(), z=zv.ravel(), u=Ex.ravel(), v=Ey.ravel(), w=Ez.ravel(),colorscale='Inferno', colorbar=dict(title='$x^2$'),
               sizemode="scaled", sizeref=0.2)
layout = go.Layout(title=r'Plot Title',
                     scene=dict(xaxis_title=r'x',
                                yaxis_title=r'y',
                                zaxis_title=r'z',
                                aspectratio=dict(x=1, y=1, z=1),
                                camera_eye=dict(x=1.2, y=1.2, z=1.2)))
fig = go.Figure(data = data, layout=layout)
#fig.update_layout(scene_camera_eye=dict(x=-0.76, y=1.8, z=0.92))
# the point charges
#fig = plt.figure()
fig.add_scatter3d(x=qq[0], y=qq[1], z=qq[2])
#ax.scatter(*qq, c= 'r', marker='o', )
HTML(fig.to_html(default_width=1000, default_height=600))
fig.show()
# colorbar for magnitude
#cbar = plt.colorbar()
#cbar.ax.set_ylabel('Magnitude')
# misc






