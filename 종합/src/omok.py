import sys
import pygame
from math import *
import tkinter.messagebox
from pygame.locals import MOUSEBUTTONDOWN

pygame.init()
FPSCLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((700, 700))
SURFACE.fill((150, 75, 0))
Concave = [[0 for i in range(15)] for g in range(15)]
start = 0
change = 0
color = [(0, 0, 0), (255, 255, 255)]
dy = [-1, -1, -1, 0]
dx = [-1, 0, 1, 1]
finsh = 0


def count(y, x, gy, gx, Color):
    cnt = 0
    while True:
        y += gy
        x += gx
        if y < 0 or y > 14 or x < 0 or x > 14: return cnt
        if Concave[y][x] == Color:
            cnt += 1
        else:
            return cnt


def put(Ypos, Xpos):
    global start
    if 0 <= floor(Ypos) < 14 and 0 <= floor(Xpos) < 14:
        if Ypos - int(Ypos) <= int(Ypos) + 1 - Ypos:  # up
            if Xpos - int(Xpos) <= int(Xpos) + 1 - Xpos:  # left
                if Concave[int(Ypos)][int(Xpos)] == 0:
                    Concave[int(Ypos)][int(Xpos)] = start % 2 + 1  # 1 black 2 white
                    return [1, int(Ypos), int(Xpos)]

            else:  # right
                if Concave[int(Ypos)][int(Xpos) + 1] == 0:
                    Concave[int(Ypos)][int(Xpos) + 1] = start % 2 + 1  # 1 black 2 white
                    return [1, int(Ypos), int(Xpos) + 1]

        else:
            if Xpos - int(Xpos) <= int(Xpos) + 1 - Xpos:  # left
                if Concave[int(Ypos) + 1][int(Xpos)] == 0:
                    Concave[int(Ypos) + 1][int(Xpos)] = start % 2 + 1  # 1 black 2 white
                    return [1, int(Ypos) + 1, int(Xpos)]

            else:  # right
                if Concave[int(Ypos) + 1][int(Xpos) + 1] == 0:
                    Concave[int(Ypos) + 1][int(Xpos) + 1] = start % 2 + 1  # 1 black 2 white
                    return [1, int(Ypos) + 1, int(Xpos) + 1]
    return [0, 0, 0]

class Omok:
    @staticmethod
    def game_start():
        global start, finsh
        while True:
            SURFACE.fill((150, 75, 0))
            if start % 2 == 0:
                font = pygame.font.SysFont('notosansmonocjkkrregular', 50)
                img = font.render("Black turn", True, (0, 0, 0))
                SURFACE.blit(img, (300, 10))

            else:
                font = pygame.font.SysFont('notosansmonocjkkrregular', 50)
                img = font.render("White turn", True, (255, 255, 255))
                SURFACE.blit(img, (300, 10))

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    xpos, ypos = (event.pos[0] - 70) / 40, (event.pos[1] - 70) / 40
                    yx = put(ypos, xpos)
                    if yx[0]:
                        for i in range(4):
                            left = count(yx[1], yx[2], dy[i], dx[i], start % 2 + 1)
                            right = count(yx[1], yx[2], -dy[i], -dx[i], start % 2 + 1)

                            if left + right == 4:
                                finsh = 1
                                break
                        start += 1

            for i in range(70, 655, 40):
                pygame.draw.lines(SURFACE, (0, 0, 0), False, [[70, i], [630, i]], 2)
                pygame.draw.lines(SURFACE, (0, 0, 0), False, [[i, 70], [i, 630]], 2)

            for i in range(15):
                for g in range(15):
                    if Concave[i][g] != 0: pygame.draw.circle(SURFACE, color[Concave[i][g] - 1],
                                                              [g * 40 + 70, i * 40 + 70], 20)

            pygame.display.update()

            if finsh == 1:
                if start % 2 == 1:
                    tkinter.messagebox.showinfo("", "black win!")

                else:
                    tkinter.messagebox.showinfo("", "white win!")

                sys.exit()
