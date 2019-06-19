import pygame
from pygame import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math as mat
# import numpy as np
import random

class Tunel:

    def __init__(self):
        self.radius = 42
        self.sides_num = 12

        self.depth = 30
        self.interval = 30

        self.vertices = []
        self.edges = []
        self.sides = []

    def build(self):
        for z in range(0, self.depth):
            for i in range(0, self.sides_num):
                self.vertices.append([int(mat.sin(2 * mat.pi / self.sides_num * i) * self.radius),
                                      int(mat.cos(2 * mat.pi / self.sides_num * i) * self.radius) + self.radius - 20, z * self.interval])

        for z in range(0, self.depth):
            for i in range(0, self.sides_num):
                self.edges.append([i + z * self.sides_num, ((i + 1) % self.sides_num) + z * self.sides_num])

        for z in range(0, self.depth-1):
            for i in range(0, self.sides_num):
                self.edges.append([i + z * self.sides_num, i + ((z + 1) * self.sides_num)])

        for z in range(0, self.depth - 1):
            for i in range(0, self.sides_num):
                self.sides.append([i + z * self.sides_num, (i + 1) % self.sides_num + z * self.sides_num,
                                   (i + 1) % self.sides_num + (z + 1) * self.sides_num, i + (z + 1) * self.sides_num])

    def draw(self):
        glBegin(GL_QUADS)

        for side in self.sides:
            for vertex in side:

                # r = random.random()
                # g = random.random()
                # b = random.random()

                glColor3f(1, 1, 0.9)
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glLineWidth(4)
        glBegin(GL_LINES)

        for edge in self.edges:
            for vertex in edge:
                glColor3f(0, 0, 0)
                glVertex3fv(self.vertices[vertex])
        glEnd()


def main():

    terrain = Tunel()
    terrain.build()

    pygame.init()

    win_size = (1200, 900)
    pygame.display.set_mode(win_size, DOUBLEBUF | OPENGL)

    gluPerspective(90, (win_size[0]/win_size[1]), 0.9, 500)
    glTranslate(0, 0, -400)
    # glEnable(GL_DEPTH_TEST)

    clock = pygame.time.Clock()
    exit_flag = False

    while not exit_flag:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag = True

        glRotatef(1, 0, 0, int(2 * mat.pi))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        terrain.draw()
        pygame.display.flip()


main()
