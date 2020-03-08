import math
import pygame
from OpenGL.GLU import *
from OpenGL.GL import *

from Background import Background
from Block import Block
from Tunnel import Tunnel


def main():

    background = Background(20)

    terrain = Tunnel()
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

        background.move()

        terrain.clear()
        terrain.move()
        terrain.collision()

        # glRotatef(1, 0, 0, int(2 * mat.pi))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        background.draw()
        terrain.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
