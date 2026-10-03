import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from astropy import constants as const
from astropy import units as u
#vector operation functions that i didnt use all of lmao
def addvectors(a,b):
    return([x + y for x, y in zip(a, b)])
def vform(a):
    return([math.hypot(a[0],a[1]), math.atan2(a[1],a[0])])
def rform(a):
    return([round(a[0]*math.cos(a[1]),10),round(a[0]*math.sin(a[1]),10)])
def dtscale(a):
    return([b * dt for b in a])
#timestep of 1 day per frame, gravitational constant in (au^3)/(kgs^2) since these are the units my calculations use, may change from kg to earth masses in the future
dt = 3600
G = const.G.to(u.au**3/u.kg/u.s**2)

#starting data for the simulation based on ~jan 3 2026. velocity vector, position, year length in earth days, plot color, plot size
#starting angles are perfectly tangential to the sun because I honestly dont know where to find that data
planetdata = { 
    "sun": {"v": [0,0], "pos": [0,0], "color": 'yellow', "size": 15, "mass": 1.989*10**30},
    "earth": {"v": [0, 0.00000020247614], "pos": [0.983302765686, 0], "reset": 365, "color": 'blue', "size": 7, "mass": 5.9722*10**24},
    "Venus": {"v": rform([0.0000002326236,math.radians(276+90)]), "pos": rform([0.728,math.radians(276)]), "reset": 225, "color": 'yellow', "size": 6, "mass": 4.86732*10**24},
    "mercury": {"v": rform([0.000000374,math.radians(268+90)]), "pos": rform([0.313,math.radians(268)]), "reset": 88, "color": 'brown', "size": 4, "mass": 0.33010*10**24},
    "mars": {"v": rform([0.000000175,math.radians(176+90)]), "pos": rform([1.404,math.radians(176)]), "reset": 687, "color": 'red', "size": 5, "mass": 0.64171*10**24},
    "jupiter": {"v": rform([0.000000092,math.radians(32+90)]), "pos": rform([4.953,math.radians(32)]), "reset": 4333, "color": 'tan', "size": 13, "mass": 1.89813*10**27},
    "saturn": {"v": rform([0.000000062,math.radians(70+90)]), "pos": rform([9.875,math.radians(70)]), "reset": 10756, "color": 'wheat', "size": 11, "mass": 5.68317*10**26},
    "uranus": {"v": rform([0.000000044,math.radians(49+90)]), "pos": rform([19.541,math.radians(49)]), "reset": 30687, "color": 'blue', "size": 9, "mass": 8.6811*10**25},
    "neptune": {"v": rform([0.000000037,math.radians(63+90)]), "pos": rform([29.904,math.radians(63)]), "reset": 60190, "color": 'blue', "size": 9, "mass": 1.024*10**26},
    "pluto": {"v": rform([0.000000031,math.radians(203+90)]), "pos": rform([35.531,math.radians(203)]), "reset": 90560, "color": 'pink', "size": 1, "mass": 1.30900*10**22}
}

#set up plot
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_xlim(-3,3) 
ax.set_ylim(-3,3)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.5)

#create a dot on the plot for each planet. god be damned if i write this out manually
for planet, data in planetdata.items():
    data['plot'] = ax.plot([], [],marker='o', color=data['color'], markersize=data['size'])

#function to calculate the vector of acceleration from gravity between two bodies
def gvcalc(velocity, position, position2, mass): #velocity vector in rectanular form, position in x, y, position of second body in x, y, mass of the second body

    #find distance between the two bodies
    r = math.hypot(abs(position[0]-position2[0]),abs(position[1]-position2[1]))

    #calculate the acceleration due to gravity acting on the body being calculated for
    gv = [-((G.value*mass*position[0]/r**3)), -((G.value*mass*position[1]/r**3))]

    #scale the acceleration vector and add it to the velocity vector
    velocity = addvectors(velocity,dtscale(gv))

    return velocity

#magic. also it grabs and plots the dots for each planet at the start of the simulation
def init():
    global planetdata
    dots =[]
    for planet, data in planetdata.items():
        data['plot'][0].set_data([data['pos'][0]],[data['pos'][1]])
        dots.append(data['plot'][0])
    return dots

#main simulation loop! yippee!
def update(frame):
    global planetdata, dt, G
    dots = []

    #i am a mature adult
    for poop in range(24):

        #grab data from the main library and perform calculations for each body
        for planet, data in planetdata.items():

            #grab data again to perform calculations for every other body's interaction with the current body
            for planet2, data2 in planetdata.items():

                if not planet2 == planet: #   ;)

                    #calls the gv function to update the velocity and position of the current body
                    data['v'] = gvcalc(data['v'], data['pos'], data2['pos'], data2['mass'])

        #changes positions after all velocity changes are done to avoid leapfrogging errors! very smart. thanks internet
        for planet, data in planetdata.items():
            data['pos'] = addvectors(data["pos"],dtscale(data['v']))
            data['plot'][0].set_data([data['pos'][0]], [data['pos'][1]])
            dots.append(data['plot'][0])
    return dots

#no clue what this does but if i touch it things break
frames_sequence = np.linspace(0, 2*np.pi, 365, endpoint=False)

#50fps
ani = anim.FuncAnimation(
    fig, update, frames=frames_sequence, init_func=init, blit=True, interval=20
)
plt.show()