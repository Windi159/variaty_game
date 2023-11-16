import pygame
import sys
from src.numberYagu import NumberYagu
from src.jumpGame import Game_start
from src.omok import Omok
from src.yutNoriMain import App

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width, screen_height = 1000, 620
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Want game?")

#시작화면
title_screen = ".\\img\\start_screen.png"

start_screen = pygame.image.load(title_screen)
start_screen = pygame.transform.scale(start_screen, (screen_width, screen_height))

# 배경 음악 파일 경로 설정
background_music_file = ".\\music\\bgm.mp3"  # 음악 파일 경로

# 배경 음악 초기화 및 재생
pygame.mixer.music.load(background_music_file)
pygame.mixer.music.set_volume(0.5)  # 볼륨 설정 (0.0부터 1.0까지)

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)

# 폰트 설정
font = pygame.font.Font(None, 36)

# 버튼 클래스 정의
class Button:
    def __init__(self, x, y, width, height, text, bg_color, text_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.action = action

    def draw(self, main_screen, outline=None):
        if outline:
            pygame.draw.rect(main_screen, outline, self.rect, 0)
        pygame.draw.rect(main_screen, self.bg_color, self.rect, 0)

        if self.text:
            button_font = pygame.font.Font(None, 36)
            text_surface = button_font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = self.rect.center
            main_screen.blit(text_surface, text_rect)

    def is_clicked(self, got_pos):
        if self.rect.collidepoint(got_pos):
            self.action()

def select_game1_action():
    pygame.mixer.music.stop()
    pygame.init()
    print("원탁아 그래픽은 언제 만들거니")

def select_game2_action():
    pygame.mixer.music.stop()
    pygame.init()
    pygame.display.set_mode((640, 200))
    pygame.display.set_caption("jump game")

    Game_start(True)

def select_game3_action():
    pygame.mixer.music.stop()
    pygame.init()
    pygame.display.set_mode((700, 700))
    pygame.display.set_caption("omok")

    Omok().game_start()

def select_game4_action():
    pygame.mixer.music.stop()
    pygame.init()
    pygame.display.set_mode((600, 600))
    pygame.display.set_caption("yut nori")

    App().run()

def quit_action():
    pygame.quit()
    sys.exit()

class MainScreen:
    def __init__(self):
        global screen
        self.play_game1_button = Button(200, 200, 175, 50, "NumberYagu", white, black, select_game1_action)
        self.play_game2_button = Button(200, 300, 175, 50, "JumpKing", white, black, select_game2_action)
        self.play_game3_button = Button(450, 200, 175, 50, "Omok", white, black, select_game3_action)
        self.play_game4_button = Button(450, 300, 175, 50, "YutNori", white, black, select_game4_action)
        self.quit_button = Button(325, 400, 175, 50, "End", white, black, quit_action)
        self.screen_width, self.screen_height = 1000, 620
        self.main_screen = screen

        self.draw_screen()

    def draw_screen(self):
        self.screen_width, self.screen_height = 1000, 620
        self.main_screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Want game?")

        self.main_screen.blit(start_screen, (0, 0))

        pygame.mixer.music.play(-1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.play_game1_button.is_clicked(pos):
                            pass

                        elif self.play_game2_button.is_clicked(pos):
                            pass

                        elif self.play_game3_button.is_clicked(pos):
                            pass

                        elif self.play_game4_button.is_clicked(pos):
                            pass

                        elif self.quit_button.is_clicked(pos):
                            pass


            self.play_game1_button.draw(screen, white)
            self.play_game2_button.draw(screen, white)
            self.play_game3_button.draw(screen, white)
            self.play_game4_button.draw(screen, white)
            self.quit_button.draw(screen, white)

            pygame.display.update()


if __name__ == "__main__":
    MainScreen()
