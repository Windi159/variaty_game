import pygame
import sys
import random
from pygame.locals import K_ESCAPE

pygame.init()
screen = pygame.display.set_mode((640, 200))
pygame.display.set_caption("jump game")

black = (255, 255, 255)
white = (0, 0, 0)

playerGroup = pygame.sprite.Group()
obstaclesGroup = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.vel = 0
        self.clicked = False  # 스페이스바를 눌렀을 때 클릭 상태로 변경
        self.jump_cnt = 0  # 3단 점프까지 적용

    def update(self):
        #스페이스바를 눌렀을 때 클릭 상태로 변경하고 점프
        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.clicked:
            self.clicked = True
            if self.jump_cnt < 3:  # 3회까지
                self.vel = -12  # 점프 속도를 조절하여 느리게
                self.jump_cnt += 1

        if not pygame.key.get_pressed()[pygame.K_SPACE]:
            self.clicked = False

        self.vel += 1  # 1씩 아래로 떨어지게
        if self.vel > 10:  # 10 이상 안넘어가도록
            self.vel = 10

        if self.rect.bottom <= 200:
            self.rect.y += int(self.vel)
            if self.rect.y >= 200 - self.rect.height:
                self.rect.y = 200 - self.rect.height
                self.jump_cnt = 0  # 점프횟수 초기화


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        pt = [(width / 2, 0), (0, height), (width, height)]  # 세모(꼭지점. 왼쪽밑, 오른쪽 밑)
        pygame.draw.polygon(self.image, color, pt)
        self.rect = self.image.get_rect()
        self.vel = 5
        self.rect.x = 640  # 오른쪽에서 플레이어쪽으로 이동
        self.rect.y = 200 - self.rect.height


    def update(self):
        self.rect.x -= int(self.vel)

    def check_screen_out(self):  # 화면 밖으로 나갈시 객체를 삭제
        result = False
        if self.rect.x < 0:
            result = True
        return result


class Game_start:
    pygame.init()

    def __init__(self, is_true=False):
        self.game_over = False
        self.score = 0
        self.clock = pygame.time.Clock()
        self.t_tick = -1
        self.color = (0, 0, 0)
        self.start = is_true

        if self.start is True:
            self.game_start()

    def random_color(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return self.color

    def show_game_over(self):
        self.game_over = True

        font = pygame.font.SysFont("헤드라인", 60)
        over_text = font.render(f"Game Over", True, (50, 50, 255))
        screen.blit(over_text, (int(640 / 2 - over_text.get_width() / 2), int(200 / 3)))

        font = pygame.font.SysFont("헤드라인", 30)
        over_text = font.render(f"please, R key..", True, (200, 200, 255))
        screen.blit(over_text, (int(640 / 2 - over_text.get_width() / 2), int(200 / 4 * 2)))

    def restart_game(self):
        self.game_over = False
        obstaclesGroup.empty()
        self.score = 0

    def show_score(self):
        font = pygame.font.SysFont("헤드라인", 30)
        score_text = font.render(f"Score : {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (0, 0))

    def game_start(self):
        pygame.init()

        playerGroup.add(Player(30, 30, black))

        while True:
            self.clock.tick(60)
            self.t_tick += 1

            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            key_event = pygame.key.get_pressed()
            if key_event[pygame.K_r] and self.game_over:
                self.restart_game()

            if self.game_over is True:
                self.show_game_over()

            else:
                if self.t_tick % random.randint(20, 50) == 0:
                    self.t_tick = 0
                    obstaclesGroup.add(Obstacle(30, 30, self.random_color()))

                # 충돌 처리
                if pygame.sprite.groupcollide(playerGroup, obstaclesGroup, False, False):
                    self.show_game_over()

                # 장애물이 왼쪽 밖으로 넘어간 것 체크
                for o in obstaclesGroup:
                    if o.check_screen_out():
                        self.score += 1
                        obstaclesGroup.remove(o)

                screen.fill(white)
                self.show_score()

                playerGroup.update()
                playerGroup.draw(screen)

                obstaclesGroup.update()
                obstaclesGroup.draw(screen)

            pygame.display.update()

            if pygame.key.get_pressed()[K_ESCAPE]:
                for p in playerGroup:
                    playerGroup.remove(p)

                for o in obstaclesGroup:
                    obstaclesGroup.remove(o)

                self.game_over = False
                self.score = 0
                self.clock = pygame.time.Clock()
                self.t_tick = -1
                self.color = (0, 0, 0)
                self.start = False

                pygame.init()
                break

        from game_select_screen import MainScreen

        MainScreen()
