import pygame
import tkinter.messagebox
from math import *
from pygame.locals import MOUSEBUTTONDOWN

pygame.init()
FPSCLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((700, 700))
SURFACE.fill((150, 75, 0))
color = [(0, 0, 0), (255, 255, 255)]
dy = [-1, -1, -1, 0]
dx = [-1, 0, 1, 1]

class Omok:
    def __init__(self):
        self.start = 0
        self.change = 0
        self.finish = 0
        self.concave = [[0 for i in range(15)] for g in range(15)]

        self.game_start()

    def init_var(self):
        self.start = 0
        self.change = 0
        self.finish = 0
        self.concave = [[0 for i in range(15)] for g in range(15)]

    def count(self, y, x, gy, gx, Color):
        cnt = 0
        while True:
            y += gy
            x += gx
            if y < 0 or y > 14 or x < 0 or x > 14:
                return cnt

            if self.concave[y][x] == Color:
                cnt += 1
            else:
                return cnt

    def put(self, Ypos, Xpos):
        if 0 <= floor(Ypos) < 14 and 0 <= floor(Xpos) < 14:
            if Ypos - int(Ypos) <= int(Ypos) + 1 - Ypos:  # up
                if Xpos - int(Xpos) <= int(Xpos) + 1 - Xpos:  # left
                    if self.concave[int(Ypos)][int(Xpos)] == 0:
                        self.concave[int(Ypos)][int(Xpos)] = self.start % 2 + 1  # 1 black 2 white
                        return [1, int(Ypos), int(Xpos)]

                else:  # right
                    if self.concave[int(Ypos)][int(Xpos) + 1] == 0:
                        self.concave[int(Ypos)][int(Xpos) + 1] = self.start % 2 + 1  # 1 black 2 white
                        return [1, int(Ypos), int(Xpos) + 1]

            else:
                if Xpos - int(Xpos) <= int(Xpos) + 1 - Xpos:  # left
                    if self.concave[int(Ypos) + 1][int(Xpos)] == 0:
                        self.concave[int(Ypos) + 1][int(Xpos)] = self.start % 2 + 1  # 1 black 2 white
                        return [1, int(Ypos) + 1, int(Xpos)]

                else:  # right
                    if self.concave[int(Ypos) + 1][int(Xpos) + 1] == 0:
                        self.concave[int(Ypos) + 1][int(Xpos) + 1] = self.start % 2 + 1  # 1 black 2 white
                        return [1, int(Ypos) + 1, int(Xpos) + 1]

        return [0, 0, 0]


    def game_start(self):
        self.init_var()

        while True:
            SURFACE.fill((150, 75, 0))
            if self.start % 2 == 0:
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
                    yx = self.put(ypos, xpos)
                    if yx[0]:
                        for i in range(4):
                            left = self.count(yx[1], yx[2], dy[i], dx[i], self.start % 2 + 1)
                            right = self.count(yx[1], yx[2], -dy[i], -dx[i], self.start % 2 + 1)

                            if left + right == 4:
                                self.finish = 1
                                break
                        self.start += 1

            for i in range(70, 655, 40):
                pygame.draw.lines(SURFACE, (0, 0, 0), False, [[70, i], [630, i]], 2)
                pygame.draw.lines(SURFACE, (0, 0, 0), False, [[i, 70], [i, 630]], 2)

            for i in range(15):
                for g in range(15):
                    if self.concave[i][g] != 0:
                        pygame.draw.circle(
                            surface=SURFACE,
                            color=color[self.concave[i][g] - 1],
                            center=[g * 40 + 70, i * 40 + 70],
                            radius=20
                        )

            pygame.display.update()

            if self.finish == 1:
                if self.start % 2 == 1:
                    tkinter.messagebox.showinfo("", "black win!")

                else:
                    tkinter.messagebox.showinfo("", "white win!")

                if tkinter.messagebox.askyesno("One more time?", "다시 하시겠습니까?"):
                    self.init_var()
                    pass

                else:
                    break


            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.init()
                break

        from game_select_screen import MainScreen

        MainScreen()
