import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np


class Tunel:

    def __init__(self):
        self.radius = 42
        self.sides_num = 12

        self.depth = 15
        self.interval = 30

        self.vertices = []
        self.edges = []
        self.sides = []

    def build(self):
        for z in range(0, self.depth):
            for i in range(0, self.sides_num):
                self.vertices.append([int(math.sin(2 * math.pi / self.sides_num * i) * self.radius),
                                      int(math.cos(2 * math.pi / self.sides_num * i) * self.radius), z * self.interval])
#  + self.radius - 20
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

    def rotate(self, x):

        cos_x = math.cos(math.pi / self.sides_num / 2 * x)
        sin_x = math.sin(math.pi / self.sides_num / 2 * x)

        rotation_matrix = np.array([[cos_x, -sin_x, 0],
                                    [sin_x, cos_x, 0],
                                    [0, 0, 1]])

        for v in range(0, self.sides_num * self.depth):
            self.vertices[v] = np.matmul(rotation_matrix, self.vertices[v])

    def move(self):

        length = len(self.vertices)

        if self.vertices[length - 1][2] >= 400:

            temp = []

            for i in range(length - self.sides_num, length):
                temp.append(self.vertices[length - self.sides_num])
                self.vertices.pop(length - self.sides_num)
            for i in range(0, self.sides_num):
                temp[i][2] = -self.interval
                self.vertices.insert(i, temp[i])
        for v in range(0, self.sides_num * self.depth):
            self.vertices[v] = np.add(self.vertices[v], [0, 0, 2])


def main():

    terrain = Tunel()
    terrain.build()

    pygame.init()

    win_size = (1200, 900)
    pygame.display.set_mode(win_size, pygame.DOUBLEBUF | pygame.OPENGL)

    gluPerspective(90, (win_size[0]/win_size[1]), 0.9, 400)
    glTranslate(0, terrain.radius - 20, -400)
    # glEnable(GL_DEPTH_TEST)

    clock = pygame.time.Clock()
    exit_flag = False

    while not exit_flag:
        clock.tick(60)
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                exit_flag = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            terrain.rotate(-1)
        if keys[pygame.K_a]:
            terrain.rotate(1)

        terrain.move()

        # glRotatef(1, 0, 0, int(2 * mat.pi))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        terrain.draw()
        pygame.display.flip()


main()
