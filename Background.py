from Tunnel import Tunnel
import random
import numpy as np
from OpenGL.GL import *


class Background:

    particles = []

    def __init__(self, num_of_particles):
        self.num = num_of_particles
        for i in range(self.num):
            self.particles.append(self.random_point)

    @property
    def random_point(self):
        x = random.randint(-Tunnel.radius, Tunnel.radius)
        y = random.randint(-Tunnel.radius, Tunnel.radius)
        z = random.randint(-10 * Tunnel.interval, -2 * Tunnel.interval)
        return[x, y, z]

    def move(self):
        for p in range(len(self.particles)):
            self.particles[p] = np.add(self.particles[p], [0, 0, 10])
            if self.particles[p][2] > 2 * Tunnel.interval:
                self.particles[p] = self.random_point

    def draw(self):
        glLineWidth(1)
        glBegin(GL_LINES)
        for p in self.particles:
            glColor3f(0.8, 0.8, 0.9)
            glVertex3fv(np.add(p, [0, 0, -60]))
            glVertex3fv(p)
        glEnd()
