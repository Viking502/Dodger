import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
import random

RED = (0.8, 0.1, 0.1)
GREEN = (0.1, 0.8, 0.1)
BLUE = (0.1, 0.1, 0.8)
PINK = (0.8, 0.1, 0.4)


class Tunel:
    radius = 42
    sides_num = 12

    depth = 20
    interval = 30

    velocity = 3

    vertices = []
    edges = []
    sides = []
    blocks = []

    def __init__(self):
        self.start_flag = True

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

        c = [1, 1, 0.9]
        if self.start_flag:
            c = [0.8, 0.8, 0.2]

        for side in self.sides:
            for vertex in side:

                glColor3f(c[0], c[1], c[2])
                glVertex3fv(self.vertices[vertex])

        glEnd()

        glLineWidth(4)
        glBegin(GL_LINES)

        for edge in self.edges:
            for vertex in edge:
                glColor3f(0, 0, 0)
                glVertex3fv(self.vertices[vertex])
        glEnd()

        for block in self.blocks:
            block.draw()

    def rotate(self, x):

        cos_x = math.cos(math.pi / self.sides_num / 2 * x)
        sin_x = math.sin(math.pi / self.sides_num / 2 * x)

        rotation_matrix = np.array([[cos_x, -sin_x, 0],
                                    [sin_x, cos_x, 0],
                                    [0, 0, 1]])

        for v in range(0, self.sides_num * self.depth):
            self.vertices[v] = np.matmul(rotation_matrix, self.vertices[v])

        for block in self.blocks:
            for v in range(0, len(block.vertices)):
                block.vertices[v] = np.matmul(rotation_matrix, block.vertices[v])

    def clear(self):
        length = len(self.vertices)

        if self.vertices[length - 1][2] >= (self.depth - 1) * self.interval:
            temp = []

            for i in range(length - self.sides_num, length):
                temp.append(self.vertices[length - self.sides_num])
                self.vertices.pop(length - self.sides_num)
            for i in range(0, self.sides_num):
                temp[i][2] = -self.interval
                self.vertices.insert(i, temp[i])
            if random.randint(0, 10) == 0:
                self.start_flag = False
                self.add_block(random.randint(0, 4))

        for block in self.blocks:
            if block.vertices[3][2] >= (self.depth - 1) * self.interval:
                self.blocks.remove(block)

    def move(self):
        for v in range(0, self.sides_num * self.depth):
            self.vertices[v] = np.add(self.vertices[v], [0, 0, self.velocity])
        for block in self.blocks:
            for v in range(0, len(block.vertices)):
                block.vertices[v] = np.add(block.vertices[v], [0, 0, self.velocity])

    def add_block(self, a):
        bot = [Tunel.vertices[a], Tunel.vertices[a + 1], Tunel.vertices[a + 13], Tunel.vertices[a + 12]]
        b = a + 6
        top = [Tunel.vertices[b + 1], Tunel.vertices[b], Tunel.vertices[b + 12], Tunel.vertices[b + 13]]

        rand = random.randint(0, 4)

        if rand == 0:
            color = RED
        elif rand == 1:
            color = BLUE
        elif rand == 3:
            color = GREEN
        else:
            color = PINK

        block = Block(bot, top, True, color)
        block.build()
        self.blocks.append(block)

    def collsion(self):
        for block in self.blocks:
            if (block.vertices[0][0] > 0 > block.vertices[1][0])\
                    or (block.vertices[5][0] > 0 > block.vertices[4][0]):
                if (block.vertices[0][1] > 20 - self.radius > block.vertices[4][1])\
                        or (block.vertices[4][1] > 20 - self.radius > block.vertices[0][1]):
                    if block.vertices[2][2] > 540 > block.vertices[0][2]:
                        print("game over")
                        self.restart()

    def restart(self):
        self.blocks.clear()
        self.start_flag = True


class Block:

    def __init__(self, pos_bottom, pos_top, sided_flag, color):
        self.long_flag = sided_flag
        self.pos_a = pos_bottom
        self.pos_b = pos_top
        self.vertices = []
        self.edges = []
        self.sides = []
        self.color = color
        self.size_z = math.fabs(pos_bottom[2][2] - pos_bottom[0][2])
        self.size_x = math.fabs(pos_bottom[0][0] - pos_bottom[1][0])
        self.size_y = math.fabs(pos_bottom[0][1] - pos_top[0][1])

    def build(self):
        for v in self.pos_a:
            self.vertices.append(v)

        for v in self.pos_b:
            self.vertices.append(v)

        for i in range(0, 4):
            self.edges.append([i, (i + 1) % 4])
        for i in range(0, 4):
            self.edges.append([i + 4, (i + 1) % 4 + 4])
        for i in range(0, 4):
            self.edges.append([i, i + 4])

        for i in range(0, 1):
            self.sides.append([4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3])
        for i in range(0, 4):
            self.sides.append([i, (i + 1) % 4, (i + 1) % 4 + 4, i + 4])

    def draw(self):
        glBegin(GL_QUADS)

        for side in self.sides:
            for vertex in side:
                glColor3f(self.color[0], self.color[1], self.color[2])
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
    pygame.display.set_mode(win_size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    gluPerspective(60, (win_size[0]/win_size[1]), 0.9, 600)
    glTranslate(0, terrain.radius - 20, -560)
    glEnable(GL_DEPTH_TEST)

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
        if keys[pygame.K_ESCAPE]:
            exit_flag = True

        terrain.clear()
        terrain.move()
        terrain.collsion()

        # glRotatef(1, 0, 0, int(2 * mat.pi))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        terrain.draw()
        pygame.display.flip()


main()
