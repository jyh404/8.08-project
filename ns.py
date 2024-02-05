from dataclasses import dataclass
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# for simulation
import os
import subprocess
import glob

# hard constants:
#   N is the number of positions in the system
#   F is the number of frames produced during the simulation
N = 100
F = 100

@dataclass
class particle:
    """represents a particle in the system"""
    position: int
    velocity: int


def step(s, v_m, p):
    """
    simulate the NS model for a single step
        s is an array of particles, stored in left to right order (with PBC, doesn't matter where to start)
        v_m is the maximum velocity
        p is the probability of reducing velocity
    mutates the original array of particles
    outputs the sum of velocities (for current calculations)
    """
    # in order to update in parallel, we first set the velocities
    for i in range(len(s)):
        cur = s[i]
        next = s[(i+1) % len(s)]
        cur.velocity = min(cur.velocity + 1, v_m)
        cur.velocity = min(cur.velocity, (next.position-cur.position-1) % N)
        if np.random.rand() < p: cur.velocity = max(cur.velocity - 1, 0)
    # then update the positions
    for particle in s:
        particle.position = (particle.position + particle.velocity) % N
    return sum(particle.velocity for particle in s)

def setup(ax):
    """
    set up a number line plot in python by only displaying the x-axis
    """
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    ax.set_xlim(0, N)
    ax.set_ylim(0, 1)
    ax.patch.set_alpha(0.0)

def simulate(c, v_m, p, t = 100, video = False):
    """
    simulate the NS model for some amount of time
        c is the density of particles 
        v_m is the maximum velocity
        p is the probability of reducing velocity
        t is the number of timesteps
        video is a boolean that decides whether a video is created
    output the flow/current at steady state
        in addition, if video is True, create a video with F frames where the nth frame 
        represents the model configuration at n/F of the way through the simulation
    """
    # randomly initialize the positions of n = c*N particles
    n = int(c*N)
    positions = sorted(np.random.choice(np.arange(N), size = n, replace = False))
    # set up particle array
    particles = [particle(pos, 0) for pos in positions]
    total = 0
    for i in range(t):
        if video and i % (t/F) == 0: 
            # save this frame for image
            frame = i / (t/F)
            positions = [particle.position for particle in particles]
            # plot the things on a 2d graph with y = 0, but don't display the y-axis
            fig, ax = plt.subplots()
            setup(ax)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(N/10))
            ax.xaxis.set_minor_locator(ticker.NullLocator())
            plt.title(f"Nagel-Schreckenberg simulation with\nc = {c}, v_m = {v_m}, p = {p}")
            plt.scatter(positions, [0 for _ in range(n)])
            fig.savefig("sim%04d.png" % frame)
            plt.close()
        total += step(particles, v_m, p)
    # make video from saved frames
    if video:
        subprocess.call(
            ['ffmpeg', '-framerate', '8', '-i', 'sim%04d.png', '-r', '30', '-pix_fmt', 'yuv420p', f'NS-{N}-{c}-{v_m}-{p}.mp4']
        )
        for file_name in glob.glob("sim*.png"):
            os.remove(file_name)
    return total/N/t

def predict_flow(c, p):
    """
    output predicted flow for v_m = 1 from theory
    """
    return 0.5 * (1 - sqrt(1 - 4 * (1-p)*c*(1-c)))

def graph_1(p):
    """
    Tests that simulations match theory for v_max = 1
    """
    v_m = 1
    points = np.linspace(0, 1, 1001)
    plt.title(f"Nagel-Schreckenberg with\nv_m = {v_m}, p = {p}")
    plt.plot(points, [simulate(c, v_m, p) for c in points], 'g', label = "simulation")
    plt.plot(points, [predict_flow(c, p) for c in points], 'b', label = "theory")
    plt.xlim(0, 1)
    plt.xlabel('density (c)')
    plt.ylabel('flow (f)')
    plt.legend(loc='best')
    plt.savefig(f"NS-v_m={v_m}-p={p}.png")
    plt.close()

def graph_2():
    """
    Graphs flow vs. density for varying levels of v_m
    """
    cases = [(1, 'r'), (2, 'y'), (5, 'g'), (10, 'b')] #(v_max, color)
    p = 0.5
    points = np.linspace(0, 1, 1001)
    plt.title(f"Nagel-Schreckenberg with varying v_m, p = {p}")
    for v_m, color in cases:
        plt.plot(points, [simulate(c, v_m, p) for c in points], color, label = f"v_m = {v_m}")
    plt.xlim(0, 1)
    plt.xlabel('density (c)')
    plt.ylabel('flow (f)')
    plt.legend(loc='best')
    plt.savefig(f"NS-v_ms.png")
    plt.close()

# Test the functions above:
# simulate(0.5, 1, 0.5, video = True)
# graph_1(0.5)
# graph_1(0.3)
# graph_2()