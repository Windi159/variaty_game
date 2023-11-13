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
start_screen = pygame.image.load(".\\img\\start_screen.png")
start_screen = pygame.transform.scale(start_screen, (screen_width, screen_height))

# 배경 음악 파일 경로 설정
background_music_file = ".\\music\\bgm.mp3"  # 음악 파일 경로

# 배경 음악 초기화 및 재생
pygame.mixer.music.load(background_music_file)
pygame.mixer.music.set_volume(0.5)  # 볼륨 설정 (0.0부터 1.0까지)
pygame.mixer.music.play(-1)  # -1은 무한 반복을 의미

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

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, self.rect, 0)
        pygame.draw.rect(screen, self.bg_color, self.rect, 0)

        if self.text:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = self.rect.center
            screen.blit(text_surface, text_rect)

    def is_clicked(self, got_pos):
        if self.rect.collidepoint(got_pos):
            self.action()

def select_game1_action():
    NumberYagu()

def select_game2_action():
    pygame.init()
    pygame.display.set_mode((640, 200))
    pygame.display.set_caption("jump game")

    Game_start(True)

def select_game3_action():
    pygame.init()
    pygame.display.set_mode((700, 700))
    pygame.display.set_caption("omok")

    Omok.game_start()

def select_game4_action():
    pygame.init()
    pygame.display.set_mode((600, 600))
    pygame.display.set_caption("yut nori")

    App().run()

def quit_action():
    pygame.quit()
    sys.exit()

play_game1_button = Button(200, 200, 175, 50, "NumberYagu", white, black, select_game1_action)
play_game2_button = Button(200, 300, 175, 50, "JumpKing", white, black, select_game2_action)
play_game3_button = Button(450, 200, 175, 50, "Omok", white, black, select_game3_action)
play_game4_button = Button(450, 300, 175, 50, "YutNori", white, black, select_game4_action)
quit_button = Button(325, 400, 175, 50, "End", white, black, quit_action)

# 배경 이미지 그리기
screen.blit(start_screen, (0, 0))
    
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if play_game1_button.is_clicked(pos):
                    pass

                elif play_game2_button.is_clicked(pos):
                    pass

                elif play_game3_button.is_clicked(pos):
                    pass

                elif play_game4_button.is_clicked(pos):
                    pass

                elif quit_button.is_clicked(pos):
                    running = False

   
    play_game1_button.draw(screen, white)
    play_game2_button.draw(screen, white)
    play_game3_button.draw(screen, white)
    play_game4_button.draw(screen, white)
    quit_button.draw(screen, white)
    pygame.display.update()

pygame.quit()
