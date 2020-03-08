import numpy as np
import random

from Block import *

RED = (0.8, 0.1, 0.1)
GREEN = (0.1, 0.8, 0.1)
BLUE = (0.1, 0.1, 0.8)
PINK = (0.8, 0.1, 0.4)


class Tunnel:
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
        bot = [Tunnel.vertices[a], Tunnel.vertices[a + 1], Tunnel.vertices[a + 13], Tunnel.vertices[a + 12]]
        b = a + 6
        top = [Tunnel.vertices[b + 1], Tunnel.vertices[b], Tunnel.vertices[b + 12], Tunnel.vertices[b + 13]]

        color = random.choice(RED, BLUE, PINK, GREEN)
        block = Block(bot, top, True, color)
        block.build()
        self.blocks.append(block)

    def collision(self):
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
