from time import *
import vobject
import numpy as np
import scipy as sp
from scipy.integrate import quad
import matplotlib.pyplot as plt
import sympy as smp
import plotly
import plotly.graph_objects as go
from IPython.display import HTML
import random

from vpython import sphere

q = float(input("Enter the charge q (max 10)"))
R = float(input("Enter the radius r"))

k = 9e9
Q = q * 1e-9
pi = 3.14

# cring=ring(pos=vector(0,0,0),axis=vector(1,0,0), radius=R,thickness=R/10,color=color.red)

N = 200
theta = 0
dtheta = 2 * pi / N
dq = Q / N
vector = smp.Matrix([0, 0, 0])
points = []
##drawing the ring

while theta < 2 * pi:
    points = points + [sphere(pos=R * vector(0, smp.cos(theta), smp.sin(theta)), radius=R / 15, color=color.red)]
    theta = theta + dtheta

##drawing one observational point
stepx = 0.8 * R
stepy = 0.8 * R
stepz = 0.8 * R
ro = vector(-R, -2 * R, -2 * R)
while ro.y < 4 * R:
    while ro.z < 4 * R:
        while ro.x < R:
            obs = sphere(pos=ro, radius=R / 25, color=color.cyan)
            E = vector(0, 0, 0)
            for p in points:
                r = obs.pos - p.pos
                dE = k * dq * norm(r) / mag(r) ** 2
                E = E + dE
            Escale = 0.005 / mag(E)
            Earrow = arrow(pos=obs.pos, axis=Escale * E, color=color.cyan)
            sleep(0.001)
            Earrow.color = color.yellow
            ro.x += stepx
        ro.x = -R
        ro.z += stepz
    ro.z = -2 * R
    ro.y += stepy