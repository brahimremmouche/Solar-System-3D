from math import sqrt, pi, cos, sin
from random import randint
import numpy as np
import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_a, K_z, K_KP_PLUS, K_KP_MINUS, K_LSHIFT, K_RSHIFT, K_EQUALS, K_6


class Objet:

    objets = []
    dt = 0.5
    Scale = 1.0

    @ classmethod
    def color(cls):
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    @ classmethod
    def weight(cls, r):
        return (4 / 3) * pi * r**3 * 0.0005

    @ classmethod
    def Distance(cls, v1, v2):
        return sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + (v1[2] - v2[2])**2)

    @ classmethod
    def Normalisation(cls, v):
        nv = sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        return np.array([v[0] / nv, v[1] / nv, v[2] / nv])

    def __init__(self, position, r, weight, speed, SUN=False):
        self.position = position
        self.r = r
        # self.weight = Objet.weight(r)
        self.weight = weight
        self.force = 0
        self.speed = speed
        self.queue = []
        if SUN:
            self.color = (255, 255, 0)
            # self.weight = 300000
            self.r = 30
        else:
            self.color = Objet.color()

    @ classmethod
    def C(cls, Z):
        return -300 * 1 / Z

    def show(self, screen, position):
        pygame.draw.circle(screen, self.color,
                           position[:2] * Objet.C(position[2]) * Objet.Scale + np.array([500, 300]), self.r * Objet.Scale)

    def trace(self, screen, rotation):
        for q in self.queue[-80:]:
            rot = np.dot(q, rotation)
            pygame.draw.circle(screen, self.color,
                               rot[:2] * Objet.C(rot[2]) * Objet.Scale + np.array([500, 300]), 2)

    @classmethod
    def Forces(cls):
        F = np.array([[0, 0, 0] for _ in range(len(Objet.objets))])
        G = 0.1
        i = 0
        for objet in Objet.objets:
            f = np.array([0, 0, 0])
            for o in Objet.objets:
                if objet != o:
                    f = G * o.weight * objet.weight / \
                        Objet.Distance(objet.position, o.position)**2
                    u = Objet.Normalisation(o.position - objet.position)
                    F[i] = F[i] + f * u
            i += 1
        return F


def calculate_rotation(_alpha, _beta, _gamma):
    s_alpha, c_alpha = sin(_alpha), cos(_alpha)
    s_beta, c_beta = sin(_beta), cos(_beta)
    s_gamma, c_gamma = sin(_gamma), cos(_gamma)
    return (
        (c_beta * c_gamma, -c_beta * s_gamma, s_beta),
        (c_alpha * s_gamma + s_alpha * s_beta * c_gamma, c_alpha *
         c_gamma - s_gamma * s_alpha * s_beta, -c_beta * s_alpha),
        (s_gamma * s_alpha - c_alpha * s_beta * c_gamma, c_alpha *
         s_gamma * s_beta + s_alpha * c_gamma, c_alpha * c_beta)
    )


def main_loop(screen):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text1 = font.render(
        'Use Buttons:  ', True, (0, 255, 0), (0, 0, 0))
    textRect1 = text1.get_rect()
    text2 = font.render(
        '[UP]  [DOWN]  [LEFT]  [RIGHT]  [A]  [Z]  [+]  [-]', True, (255, 0, 0), (0, 0, 0))
    textRect2 = text2.get_rect()
    textRect1.center = (800 // 2 - 160, 20)
    textRect2.center = (800 // 2 + 70, 20)

    Objet.objets = [Objet(
        np.array([800 // 2, 600 // 2, 300 // 2]), 50, 1000000, np.array([0, 0, 0]), SUN=True)]
    weights = np.array([300, 30, 300, 30])
    Speeds = np.array([[-5, 5, 0], [5, 5, 5], [10, -1, 1], [-20, 10, -10]])
    positions = np.array([[200, 40, 100], [440, 40, 300], [
                         600, 560, 130], [440, 440, 200]])
    raduis = np.array([20, 15, 15, 10])
    for i in range(4):
        # pos = np.array([randint(15, 785), randint(15, 585)])
        # pos = np.array([randint(200, 600), randint(150, 450)])
        # r = randint(15, 25)
        # speed = np.array([randint(-10, 10), randint(-10, 10)])
        Objet.objets.append(
            Objet(positions[i], raduis[i], weights[i], Speeds[i]))

    rotation = [-7.6, -8.2, 3.1]
    mouse_direction = np.array([0, 0])
    last_mouse_pos = np.array([0, 0])
    while True:
        screen.fill(0)
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)
        pygame.time.Clock().tick(60)
        # --------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        # --------------------------------------
        if event.type == pygame.MOUSEMOTION:
            mouse_position = np.array(pygame.mouse.get_pos())
            mouse_direction = last_mouse_pos - mouse_position
            last_mouse_pos = mouse_position
            if abs(mouse_direction[0]) != 0:
                mouse_direction[0] //= abs(mouse_direction[0])
            if abs(mouse_direction[1]) != 0:
                mouse_direction[1] //= abs(mouse_direction[1])
            if pygame.mouse.get_pressed()[0]:
                c = -0.05
                rotation[1] += c * mouse_direction[0]
                rotation[2] += c * mouse_direction[1]
                rotation[0] += c * mouse_direction[0] + \
                    c * mouse_direction[1]
        # --------------------------------------
        c = -0.1
        if pygame.key.get_pressed()[K_UP]:
            rotation[0] -= c
        if pygame.key.get_pressed()[K_DOWN]:
            rotation[0] += c
        if pygame.key.get_pressed()[K_LEFT]:
            rotation[1] -= c
        if pygame.key.get_pressed()[K_RIGHT]:
            rotation[1] += c
        if pygame.key.get_pressed()[K_a]:
            rotation[2] -= c
        if pygame.key.get_pressed()[K_z]:
            rotation[2] += c
        if pygame.key.get_pressed()[K_KP_PLUS] or ((pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]) and pygame.key.get_pressed()[K_EQUALS]):
            Objet.Scale += 0.03
        if (pygame.key.get_pressed()[K_KP_MINUS] or ((pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]) and pygame.key.get_pressed()[K_6])) and Objet.Scale > 0.2:
            Objet.Scale -= 0.03
        # --------------------------------------
        F = Objet.Forces()
        for objet, f in zip(Objet.objets, F):
            objet.speed = objet.speed + Objet.dt * (1. / objet.weight) * f
            objet.position = objet.position + Objet.dt * objet.speed
            objet.queue.append(objet.position)
        Objet.objets = sorted(Objet.objets, key=lambda x: x.position[2])
        # --------------------------------------
        for objet in Objet.objets:
            objet.trace(screen, calculate_rotation(
                rotation[0], rotation[1], rotation[2]))
            objet.show(screen, np.dot(objet.position,
                                      calculate_rotation(rotation[0], rotation[1], rotation[2])))
        # --------------------------------------
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('TP VPE')
    screen = pygame.display.set_mode((800, 600))
    main_loop(screen)
