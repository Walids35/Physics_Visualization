from vpython import *
from time import *

nlines = int(input("Enter the number of electric field lines"))

k = 9e9  # N*m^2/C^2
Q = 2e-9
L = 0.05
xo = 0.05
N = 100
dQ = Q / N
dy = L / N

ro = vector(0.0, 0.04, 0)

# Make Rod
rq = vector(0, -L / 2 + dy / 2, 0)
charges = [sphere(pos=rq, radius=L / 40, color=color.red, q=dQ)]
# print("rq last = ",L/2-dy/2)
while rq.y < (L / 2):
    rq = rq + vector(0, dy, 0)
    charges = charges + [sphere(pos=rq, radius=L / 40, color=color.red, q=dQ)]


def E(rob, charges):
    Et = vector(0, 0, 0)
    for charge in charges:
        r = rob - charge.pos
        dE = k * charge.q * norm(r) / mag(r) ** 2
        Et = Et + dE
    return (Et)


Escale = 2e-7

stepx = 0.3 * L
stepy = 0.2 * L

theta = 0
dtheta = 2 * pi / nlines

while theta < 2 * pi:
    ro = vector(stepx * cos(theta), -L, stepx * sin(theta))
    while ro.y < 1 * L:
        a = arrow(pos=ro, axis=Escale * E(ro, charges), color=color.yellow)
        ro.x = 2 * ro.x
        ro.z = 2 * ro.z
        b = arrow(pos=ro, axis=Escale * E(ro, charges), color=color.yellow)
        sleep(0.05)
        a.color = color.cyan
        b.color = color.cyan
        ro.x = ro.x / 2
        ro.z = ro.z / 2
        ro = ro + vector(0, stepy, 0)
    theta = theta + dtheta

################## ask user for the cordinates (x,y,y) of a point to visualize its E field then add this line of code ################""

#outputVector=vector(x,y,z)
#arrow(pos=outputVector, axis=Escale*E(outputVector,charges), color=color.yellow)