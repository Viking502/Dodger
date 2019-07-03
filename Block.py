import math
from OpenGL.GL import *


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
