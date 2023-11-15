import pygame
import pygame.gfxdraw
import ctypes
from src.tactical_yutnori import *
from math import hypot
from pygame import Surface, Color, Rect


# 게임 설정을 담고 있는 클래스입니다.
class App:
    config = dict(
        WSIZE=(600, 600),  # 화면 크기 설정
        FPS=30,  # 초당 프레임 수 설정
        TITLE='다함께 윷윷윷'  # 게임 창 제목 설정
    )

    def __init__(self):
        self.game = YutNoriHumVsCom()  # YutNoriHumVsCom 클래스로 게임 객체 초기화
        self._config()  # 환경 설정 메서드 호출

    def _config(self):
        self.WIDTH, self.HEIGHT = self.config['WSIZE']  # 화면 너비와 높이 설정
        self.FPS = self.config['FPS']  # 프레임 수 설정

        pygame.init()  # pygame 초기화
        ctypes.windll.user32.SetProcessDPIAware()  # DPI 설정

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # 게임 화면 설정
        self.clock = pygame.time.Clock()  # 게임 시간 설정
        pygame.display.set_caption(self.config['TITLE'])  # 게임 창 제목 설정

    # 게임 실행 메서드
    def run(self):
        self.game.reset()  # 게임 초기화
        self.GUI = GUI(self.game)  # GUI 클래스로 GUI 객체 초기화

        stop = False  # 종료 플래그

        while not stop:
            self.GUI.draw(self.screen)  # 화면 그리기

            for event in pygame.event.get():
                # 게임 종료 이벤트 처리
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    stop = True

            self.GUI.update()  # 화면 업데이트

            pygame.display.flip()  # 화면 업데이트
            self.clock.tick(self.FPS)  # 프레임 수 맞추기

        pygame.quit()  # pygame 종료


# 시간 측정을 위한 클래스
class Timer:

    # 타이머가 활성화되어 있는지 확인
    def is_on(self, name=0):
        return hasattr(self, f't_{name}')

    # 타이머 시작
    def start(self, name=0):
        if not hasattr(self, f't_{name}'):
            setattr(self, f't_{name}', pygame.time.get_ticks())

    # 경과 시간 계산
    def elapsed(self, name=0):
        return (pygame.time.get_ticks() - getattr(self, f't_{name}')) / 1000.0

    # 타이머 리셋
    def reset(self, name=0):
        delattr(self, f't_{name}')

    # 타이머 리셋 및 시작
    def restart(self):
        self.reset()
        self.start()


# 게임 GUI를 나타내는 클래스
class GUI:

    def __init__(self, game):
        self.game = game

        # 상수와 참조 변수
        self.PLAYER1, self.PLAYER2 = game.players  # 플레이어 1과 플레이어 2 설정
        self.N_PIECES_PER_PLAYER = game.N_PIECES_PER_PLAYER  # 플레이어 당 말 개수 설정
        self.NODE_OUT, self.NODE_WON = game.NODE_OUT, game.NODE_WON  # 게임 노드 상태 설정

        # 람다 함수로 플레이어 1 및 플레이어 2 여부 확인
        self.isP1 = lambda p: self.game.owner(p) == self.PLAYER1
        self.isP2 = lambda p: self.game.owner(p) == self.PLAYER2

        # 위치 및 스케일링 설정
        W, H = pygame.display.get_surface().get_size()

        # 게임 보드 그래프
        x, y, w, h = self.graph_rect = Rect([W // 25, W // 25, W * 63 // 100, W * 63 // 100])  # 게임 보드 위치 및 크기 설정
        self.corner_node_radius = self.graph_rect.width // 25  # 모퉁이 노드 반지름 설정
        self.normal_node_radius = self.graph_rect.width // 30  # 일반 노드 반지름 설정
        self.piece_radius = self.normal_node_radius * 3 // 4  # 말 반지름 설정

        # 외부 영역 설정
        s = W - w  # 오른쪽 공간
        self.regout1_rect = Rect([x + w + s // 4, y, s // 2, h * 22 // 100])  # 외부 영역 1 위치 및 크기 설정
        self.regout2_rect = Rect([x + w + s // 4, y + h * 33 // 100, s // 2, h * 22 // 100])  # 외부 영역 2 위치 및 크기 설정

        # Table
        s = H - h  # 하단 여백 설정
        *_, w, h = self.table_rect = Rect([x, H - s * 3 // 4, w, s * 3 // 4])  # 테이블 영역 설정
        self.sset_size = w * 27 // 100, h * 2 // 3
        self.stick_size = w * 6 // 100, h * 2 // 3

        # Nodes in (= Pieces in = centers rel to graph)
        self.nodes_rel_centers = self._arrange_nodes()
        self.nodes_abs_centers = self.get_nodes_abs_centers()

        # Pieces out (centers rel to regions out)
        self.piecesout_rel_centers = self._arrange_pieces()
        self.piecesout_abs_centers = self.get_piecesout_abs_centers()

        # Sticksets (toplefts rel to table)
        self.ssets_rel_toplefts = self._arrange_sticksets()
        self.ssets_abs_toplefts = self.get_sticksets_abs_toplefts()

        # Tossed-Sticks (toplefts rels to table)
        self.tossedsticks_rel_toplefts = self._arrange_tossedsticks()
        self.tossedsticks_abs_toplefts = self.get_tossedsticks_abs_toplefts()

        # 스타일 설정
        self.BGCOLOR = Color(235, 235, 235)  # 배경색 설정
        self.FONT = pygame.font.SysFont('Arial', 13)  # 폰트 설정
        self.FONT.set_bold(True)  # 굵은 글꼴 설정

        # 노드 설정
        self.corner_style = (Color('skyblue'), Color('black'), 1)  # 모퉁이 노드 스타일 설정
        self.normal_style = (Color('white'), Color('black'), 1)  # 일반 노드 스타일 설정
        self.hlight_style = (Color('lightblue'), 3)  # 강조 효과 스타일 설정

        # 외부 영역 설정 (플레이어 1, 플레이어 2)
        self.regout1_style = (Color('blue'), Color('black'), 2, 0.5)  # 외부 영역 스타일 설정 (플레이어 1)
        self.regout2_style = (Color('red'), Color('black'), 2, 0.5)  # 외부 영역 스타일 설정 (플레이어 2)

        # 말 설정 (플레이어 1, 플레이어 2)
        self.player1_color_str, self.player2_color_str = 'BLUE', 'RED'  # 플레이어 색상 설정
        self.piece1_style = (Color('blue'), Color('black'), 0)  # 말 스타일 설정 (플레이어 1)
        self.piece2_style = (Color('red'), Color('black'), 0)  # 말 스타일 설정 (플레이어 2)

        # 테이블 및 막대 스타일 설정
        self.table_style = (Color('brown'), Color('black'), 0, 0.95)  # 테이블 스타일 설정
        self.stick_style = (Color('beige'), Color('black'), 2)  # 막대 스타일 설정

        # 정적 이미지 설정
        self.graph_im = self.get_graph_image()  # 게임 그래프 이미지 설정
        self.regout1_im, self.regout2_im = self.get_regionsout_images()  # 외부 영역 이미지 설정 (플레이어 1, 플레이어 2)
        self.table_im = self.get_table_image()  # 테이블 이미지 설정
        self.stickM_im = self.get_stick_image(StickType.MARKED)  # 표시된 막대 이미지 설정
        self.stickU_im = self.get_stick_image(StickType.UNMARKED)  # 표시되지 않은 막대 이미지 설정
        self.ssets_im = self.get_sticksets_images()  # 막대 세트 이미지 설정
        self.playerturn_im = self.get_playerturn_images()  # 플레이어 턴 이미지 설정
        self.playerwins_im = self.get_playerwins_images()  # 플레이어 승리 이미지 설정

        # 표현 로직 설정
        self.timer = Timer()  # 타이머 객체 생성
        self.timer.start()  # 타이머 시작
        self.sset_sel = None  # 선택된 막대 세트 초기화
        self.node_sel = None  # 선택된 노드 초기화
        self.hlight_nodes = []  # 강조된 노드 초기화
        self.winner = None  # 승자 초기화

    # UPDATE 메서드
    def update(self):

        if self.get_winner():
            self.check_replay_selection()

        else:

            if not self.timer.is_on('turn'):
                self.timer.start('turn')

            if not self.game.sticks_been_tossed():
                self.check_sticksets_selection()
                sel = self.get_stickset_selected()
                if sel in self.game.valid_stick_pairs:
                    self.game.toss(sel)
                    self.timer.start('delay')

            elif self.timer.elapsed('delay') > 0.5:

                if not self.game.orig_node_been_selected():
                    self.highlight_nodes(self.game.valid_orig_nodes_for_selection())
                    self.check_node_selection(self.hlight_nodes)
                    sel = self.get_node_selected()
                    if sel in self.game.valid_orig_nodes_for_selection():
                        self.game.select_orig_node(sel)

                elif not self.game.dest_node_been_selected():
                    self.highlight_nodes(self.game.valid_dest_nodes_for_selection())
                    self.check_node_selection(self.hlight_nodes)
                    sel = self.get_node_selected()
                    if sel in self.game.valid_dest_nodes_for_selection():
                        self.game.select_dest_node(sel)

                elif self.timer.elapsed('turn') > 1.8:
                    # 모든 것이 선택됨 -> 진행
                    ok = self.game.step()
                    if ok:
                        self.timer.reset('turn')
                        self.timer.reset('delay')
                        self.hlight_nodes = []
                        self.node_sel = None
                        self.sset_sel = None
                        self.check_winner()

    # DRAW
    def draw(self, surf):
        # static
        surf.fill(self.BGCOLOR)  # 배경 채우기
        surf.blit(self.graph_im, self.graph_rect)  # 그래프 이미지 그리기
        surf.blit(self.regout1_im, self.regout1_rect)  # 플레이어 1 영역 이미지 그리기
        surf.blit(self.regout2_im, self.regout2_rect)  # 플레이어 2 영역 이미지 그리기
        surf.blit(self.table_im, self.table_rect)  # 게임 보드 이미지 그리기
        # dynamic
        self.draw_playerturn(surf)  # 현재 플레이어 턴 표시
        self.draw_highlighted_nodes(surf)  # 강조된 노드 표시
        self.draw_pieces(surf)  # 말 표시
        self.draw_sticks(surf)  # 스틱(막대기) 표시
        self.draw_playerwins(surf)  # 플레이어 승리 상태 표시

    def draw_playerturn(self, surf):
        surf.blit(self.playerturn_im[self.game.cur_player], self.playerturn_rect)  # 현재 플레이어의 턴 이미지 표시

    def draw_highlighted_nodes(self, surf):
        stroke, t = self.hlight_style  # 노드 강조 스타일 설정

        for nodekey in self.hlight_nodes:
            if nodekey == self.NODE_OUT:
                radius = self.piece_radius
                pieces = (p for p in self.game.board[self.NODE_OUT] if self.game.owner(p) == self.game.cur_player)
                for piece, center in zip(pieces, self.piecesout_abs_centers[self.game.cur_player]):
                    pygame.draw.circle(surf, stroke, center, radius + t, t)  # 노드 주변에 강조된 원 그리기

            elif nodekey == self.NODE_WON:
                radius = self.corner_node_radius
                x, y = self.nodes_abs_centers[BoardNode.CORNERS.SE]
                x += 4 * radius
                pygame.gfxdraw.aacircle(surf, x, y, radius + t, Color('gold'))  # 강조된 코너 노드 원 표시
                pygame.gfxdraw.filled_circle(surf, x, y, radius + t, Color('gold'))
                fill, stroke, t = self.normal_style
                pygame.gfxdraw.aacircle(surf, x, y, radius, stroke)
                pygame.gfxdraw.filled_circle(surf, x, y, radius, stroke)
                pygame.gfxdraw.aacircle(surf, x, y, radius - t - t, fill)
                pygame.gfxdraw.filled_circle(surf, x, y, radius - t - t, fill)

            else:
                radius = self.corner_node_radius if nodekey in BoardNode.CORNERS else self.normal_node_radius
                center = self.nodes_abs_centers[nodekey]
                pygame.draw.circle(surf, stroke, center, radius + t, t)  # 노드 주변에 강조된 원 그리기

    def draw_pieces(self, surf):
        piecesout1 = (p for p in self.piecesout_abs_centers[self.PLAYER1])
        piecesout2 = (p for p in self.piecesout_abs_centers[self.PLAYER2])

        for piece, nodekey in self.game.all_pieces_and_nodes():
            if nodekey == self.NODE_OUT:
                if self.isP1(piece):
                    x, y = next(piecesout1)
                    fill, stroke, t = self.piece1_style
                else:
                    x, y = next(piecesout2)
                    fill, stroke, t = self.piece2_style

                pygame.gfxdraw.aacircle(surf, x, y, self.piece_radius, stroke)  # 강조된 원 테두리 그리기
                pygame.gfxdraw.filled_circle(surf, x, y, self.piece_radius, stroke)
                pygame.gfxdraw.aacircle(surf, x, y, self.piece_radius - t - t, fill)  # 강조된 원 내부 채우기
                pygame.gfxdraw.filled_circle(surf, x, y, self.piece_radius - t - t, fill)

            elif nodekey != self.NODE_WON:
                x, y = self.nodes_abs_centers[nodekey]
                fill, stroke, t = self.piece1_style if self.isP1(piece) else self.piece2_style
                pygame.gfxdraw.aacircle(surf, x, y, self.piece_radius, stroke)  # 강조된 원 테두리 그리기
                pygame.gfxdraw.filled_circle(surf, x, y, self.piece_radius, stroke)
                pygame.gfxdraw.aacircle(surf, x, y, self.piece_radius - t - t, fill)  # 강조된 원 내부 채우기
                pygame.gfxdraw.filled_circle(surf, x, y, self.piece_radius - t - t, fill)

                # 말이 쌓인 경우 개수 표시
                if len(self.game.board[nodekey]) > 1:
                    n_stacked = len(self.game.board[nodekey])
                    text_surf = self.FONT.render(str(n_stacked), True, Color('white'))
                    text_rect = text_surf.get_rect(center=(x, y))
                    surf.blit(text_surf, text_rect)

    def draw_sticks(self, surf):
        if self.game.sticks_been_tossed():
            # 스틱이 던져진 경우
            outcome = self.game.get_toss_outcome()
            for stick_type, xy in zip(outcome, self.tossedsticks_abs_toplefts):
                stick_im = self.stickM_im if stick_type == StickType.M else self.stickU_im
                surf.blit(stick_im, xy)  # 스틱 이미지 그리기
        else:
            # 스틱이 던져지지 않은 경우
            for sset_im, xy in zip(self.ssets_im.values(), self.ssets_abs_toplefts):
                surf.blit(sset_im, xy)  # 스틱 세트 이미지 그리기

    def draw_playerwins(self, surf):
        winner = self.get_winner()
        if winner:
            # 승자가 있는 경우
            winner_im = self.playerwins_im[winner]
            surf.blit(winner_im, winner_im.get_rect(center=self.playerwins_rect.center))  # 승자 이미지 그리기

    # STATIC IMAGES
    def get_graph_image(self):
        surf = Surface(self.graph_rect.size)
        surf.fill(self.BGCOLOR)
        surf.set_colorkey(self.BGCOLOR)

        for name, center in self.nodes_rel_centers.items():
            if name in BoardNode.CORNERS:
                fill, stroke, t = self.corner_style
                radius = self.corner_node_radius
            else:
                fill, stroke, t = self.normal_style
                radius = self.normal_node_radius
            pygame.gfxdraw.aacircle(surf, *center, radius, stroke)
            pygame.gfxdraw.filled_circle(surf, *center, radius, stroke)
            pygame.gfxdraw.aacircle(surf, *center, radius - t - t, fill)
            pygame.gfxdraw.filled_circle(surf, *center, radius - t - t, fill)

        return surf.convert_alpha()

    def get_regionsout_images(self):
        surf1 = Surface(self.regout1_rect.size)
        surf2 = Surface(self.regout2_rect.size)

        fill1, stroke1, t1, alpha1 = self.regout1_style
        fill2, stroke2, t2, alpha2 = self.regout2_style

        surf1.fill(stroke1)
        surf1.fill(fill1, (t1, t1, surf1.get_width() - t1 - t1, surf1.get_height() - t1 - t1))

        surf2.fill(stroke2)
        surf2.fill(fill2, (t2, t2, surf2.get_width() - t2 - t2, surf2.get_height() - t2 - t2))

        surf1.set_alpha(int(alpha1 * 255))
        surf2.set_alpha(int(alpha2 * 255))

        return surf1.convert_alpha(), surf2.convert_alpha()

    def get_table_image(self):
        surf = Surface(self.table_rect.size)

        fill, stroke, t, alpha = self.table_style

        surf.fill(stroke)
        surf.fill(fill, (t, t, surf.get_width() - t - t, surf.get_height() - t - t))
        surf.set_alpha(int(alpha * 255))

        return surf.convert_alpha()

    def get_sticksets_images(self):
        surf_mm = Surface(self.sset_size)
        surf_mu = Surface(self.sset_size)
        surf_uu = Surface(self.sset_size)

        for surf in (surf_mm, surf_mu, surf_uu):
            surf.fill(self.table_style[0])
            surf.set_colorkey(surf.get_at([0, 0]))

        sset_w, sset_h = self.sset_size
        stick_w, stick_h = self.stick_size
        sx = sset_w - 2 * stick_w
        sy = sset_h - stick_h

        surf_mm.blit(self.stickM_im, (0, sy))
        surf_mm.blit(self.stickM_im, (stick_w + sx, sy))
        surf_mu.blit(self.stickM_im, (0, sy))
        surf_mu.blit(self.stickU_im, (stick_w + sx, sy))
        surf_uu.blit(self.stickU_im, (0, sy))
        surf_uu.blit(self.stickU_im, (stick_w + sx, sy))

        return {StickComb.MM: surf_mm.convert_alpha(),
                StickComb.MU: surf_mu.convert_alpha(),
                StickComb.UU: surf_uu.convert_alpha()}

    def get_stick_image(self, stick_type):
        assert stick_type in StickType, \
            f'Invalid stick type {stick_type!r} given!\n' \
            f'Valid stick types = {StickType!r}.'

        surf = Surface(self.stick_size)

        fill, stroke, t = self.stick_style

        surf.fill(stroke)
        surf.fill(fill, (t, t, surf.get_width() - t - t, surf.get_height() - t - t))

        if stick_type == StickType.MARKED:
            # 표시된 스틱 이미지 생성
            n = 3
            r = surf.get_width() // 5
            cross_h = r + r

            # 간격
            sx = surf.get_width() // 2
            sy = (surf.get_height() - n * cross_h) // (n + 1)

            # 오프셋
            x = sx
            y = sy + r

            for i in range(n):
                cx, cy = (x, y + (sy + cross_h) * i)
                pygame.draw.line(surf, stroke, (cx - r, cy - r), (cx + r, cy + r), t)
                pygame.draw.line(surf, stroke, (cx - r, cy + r), (cx + r, cy - r), t)

        return surf

    def get_playerturn_images(self):
        # 설정
        player1_color_str = self.player1_color_str
        player2_color_str = self.player2_color_str
        player1_color = self.piece1_style[0]
        player2_color = self.piece2_style[0]

        # 폰트 렌더링
        font = pygame.font.SysFont('Arial', 13)
        surf1 = font.render(f'{player1_color_str} TURN', True, player1_color)
        surf2 = font.render(f'{player2_color_str} TURN', True, player2_color)

        # 아웃 리전 사이에 위치
        x0, y0 = self.regout1_rect.bottomleft
        x1, y1 = self.regout2_rect.topright
        x = x0 + (x1 - x0) // 2
        y = y0 + (y1 - y0) // 2
        self.playerturn_rect = surf1.get_rect(center=(x, y))

        return {self.PLAYER1: surf1,
                self.PLAYER2: surf2}

    def get_playerwins_images(self):
        # 설정
        player1_color_str = self.player1_color_str
        player2_color_str = self.player2_color_str
        player1_color = self.piece1_style[0]
        player2_color = self.piece2_style[0]

        # 폰트 렌더링
        font = pygame.font.SysFont('Arial', 56)
        surf1 = font.render(f'{player1_color_str} WINS', True, Color('gold'))
        surf2 = font.render(f'{player2_color_str} WINS', True, Color('gold'))

        # 중앙에 위치
        self.playerwins_rect = surf1.get_rect()
        self.playerwins_rect.center = self.nodes_abs_centers[BoardNode.CORNERS.CC]

        bg = Surface(self.playerwins_rect.size)

        bg1 = bg.copy()
        bg1.fill(player1_color)
        bg1.blit(surf1, (0, 0))

        bg2 = bg.copy()
        bg2.fill(player2_color)
        bg2.blit(surf2, (0, 0))

        return {self.PLAYER1: bg1.convert_alpha(),
                self.PLAYER2: bg2.convert_alpha()}

    # LAYOUT / POSITIONING
    def vert(self, cornerA, cornerB, n_nodes=4):
        (x, Ay), (x, By) = cornerA, cornerB

        R = self.corner_node_radius
        dy = (abs(By - Ay) - 2 * R) // (n_nodes + 1)
        dy = +dy if Ay < By else -dy

        beg_y = Ay + R if Ay < By else Ay - R

        return [(x, beg_y + i * dy) for i in range(1, n_nodes + 1)]

    def horz(self, cornerA, cornerB, n_nodes=4):
        (Ax, y), (Bx, y) = cornerA, cornerB

        R = self.corner_node_radius
        dx = (abs(Bx - Ax) - 2 * R) // (n_nodes + 1)
        dx = +dx if Ax < Bx else -dx

        beg_x = Ax + R if Ax < Bx else Ax - R

        return [(beg_x + i * dx, y) for i in range(1, n_nodes + 1)]

    def diag(self, cornerA, cornerB, n_nodes=2):
        (Ax, Ay), (Bx, By) = cornerA, cornerB

        R = self.corner_node_radius
        d = (abs(Bx - Ax) - 2 * R) // (n_nodes + 1)
        dx = +d if Ax < Bx else -d
        dy = +d if Ay < By else -d

        beg_x = Ax + R if Ax < Bx else Ax - R
        beg_y = Ay + R if Ay < By else Ay - R

        return [(beg_x + i * dx, beg_y + i * dy) for i in range(1, n_nodes + 1)]

    def _arrange_nodes(self):
        nodes = {}

        # corners positions (including center)
        S = self.graph_rect.width
        R = self.corner_node_radius

        nodes[BoardNode.CORNERS.SW] = sw = (R, S - 1 - R)
        nodes[BoardNode.CORNERS.NW] = nw = (R, R)
        nodes[BoardNode.CORNERS.CC] = cc = (S // 2, S // 2)
        nodes[BoardNode.CORNERS.NE] = ne = (S - 1 - R, R)
        nodes[BoardNode.CORNERS.SE] = se = (S - 1 - R, S - 1 - R)

        nodes[BoardNode.CrossA.G1] = g1 = (S // 2, R)
        nodes[BoardNode.CrossA.G4] = g4 = (S // 2, S - 1 - R)
        nodes[BoardNode.CrossB.R1] = r1 = (R, S // 2)
        nodes[BoardNode.CrossB.R4] = r4 = (S - 1 - R, S // 2)

        nodes[BoardNode.SPECIAL.WON] = (S + R + R, S - 1 - R)

        # circuit nodes (clockwise) for vertical and horizontal paths
        n_nodes = 5
        # se -> ne (vertical)
        for nodekey, xy in zip(BoardNode.EAST, self.vert(se, ne, n_nodes)):
            nodes[nodekey] = xy
        # ne -> nw (horizontal)
        for nodekey, xy in zip(BoardNode.NORTH, self.horz(ne, nw, n_nodes)):
            nodes[nodekey] = xy
        # nw -> sw (vertical)
        for nodekey, xy in zip(BoardNode.WEST, self.vert(nw, sw, n_nodes)):
            nodes[nodekey] = xy
        # sw -> se (horizontal)
        for nodekey, xy in zip(BoardNode.SOUTH, self.horz(sw, se, n_nodes)):
            nodes[nodekey] = xy

        # cross nodes
        n_nodes = 4

        # g1 -> g4
        for nodekey, xy in zip(BoardNode.CrossA, self.vert(g1, g4, n_nodes)):
            nodes[nodekey] = xy
        # r1 -> r4
        for nodekey, xy in zip(BoardNode.CrossB, self.horz(r1, r4, n_nodes)):
            nodes[nodekey] = xy

        return nodes

    def _arrange_pieces(self):
        n = self.N_PIECES_PER_PLAYER  # 각 플레이어의 말 개수
        r = self.piece_radius  # 말의 반지름
        diam = r + r  # 말의 지름

        # 플레이어 1, 2의 아웃 영역 위치와 크기
        x1, y1, (w1, h1) = 0, 0, self.regout1_rect.size
        x2, y2, (w2, h2) = 0, 0, self.regout2_rect.size

        # 각 플레이어의 아웃 영역 내에서 말을 배치하기 위한 간격 계산
        sx1 = (w1 - diam * n) // (n + 1)  # x1 좌표 간격 계산
        sy1 = (h1 - diam * 1) // 2  # y1 좌표 계산 (수직 가운데 정렬)
        sx2 = (w2 - diam * n) // (n + 1)  # x2 좌표 간격 계산
        sy2 = (h2 - diam * 1) // 2  # y2 좌표 계산 (수직 가운데 정렬)

        # 말의 첫 번째 위치 계산 (중앙 정렬 후 반지름 추가)
        x1 += sx1 + r
        y1 += sy1 + r
        x2 += sx2 + r
        y2 += sy2 + r

        # 각 플레이어의 말 위치 계산
        pieces1 = [(x1 + (sx1 + diam) * i, y1) for i in range(n)]
        pieces2 = [(x2 + (sx2 + diam) * i, y2) for i in range(n)]

        return {self.PLAYER1: pieces1, self.PLAYER2: pieces2}

    def _arrange_sticksets(self):
        table_w, table_h = self.table_rect.size  # 게임 테이블의 크기
        w, h = self.sset_size  # 스틱세트 이미지의 크기
        n = 2  # 스틱세트 수 (marked (mm), mismatch (mu), unmarked (uu))

        # 각 스틱세트 사이의 간격 계산
        sx = (table_w - w * n) // (n + 1)
        sy = (table_h - h * 1) // 2  # 수직 가운데 정렬

        # 게임 테이블 상대 좌표 (topleft)에서의 스틱세트 위치 계산
        x = sx
        y = sy

        # 각 스틱세트의 상대 좌표 (topleft) 계산
        xys = [(x + (sx + w) * i, y) for i in range(n)]

        return xys

    def _arrange_tossedsticks(self):
        table_w, table_h = self.table_rect.size  # 게임 테이블의 크기
        stick_w, stick_h = self.stick_size  # 토스된 스틱 이미지의 크기
        n = 4  # 토스된 스틱 개수

        # 토스된 스틱 사이의 간격 계산
        sx = stick_w

        # 모든 네 개의 토스된 스틱을 수평 중앙 정렬하기 위해 오프셋 계산
        x = (table_w - (stick_w + sx) * n) // 2
        y = (table_h - stick_h) // 2  # 수직 중앙 정렬

        # 각 토스된 스틱의 상대 좌표 (topleft) 계산
        sticks_xys = [(x + (stick_w + sx) * i, y) for i in range(n)]

        return sticks_xys

    def get_nodes_abs_centers(self):
        # 게임 보드의 모든 노드의 절대 중심 좌표 계산
        x, y = self.graph_rect.topleft  # 게임 보드의 왼쪽 상단 절대 좌표
        return {nodekey: (x + dx, y + dy) for nodekey, (dx, dy) in self.nodes_rel_centers.items()}

    def get_piecesout_abs_centers(self):
        x1, y1 = self.regout1_rect.topleft  # 플레이어 1 아웃 영역의 왼쪽 상단 절대 좌표
        x2, y2 = self.regout2_rect.topleft  # 플레이어 2 아웃 영역의 왼쪽 상단 절대 좌표
        P1, P2 = self.PLAYER1, self.PLAYER2

        # 각 플레이어의 아웃 영역에 상대적인 중심 좌표에 절대 좌표를 추가하여 계산
        return {P1: [(x1 + dx1, y1 + dy1) for dx1, dy1 in self.piecesout_rel_centers[P1]],
                P2: [(x2 + dx2, y2 + dy2) for dx2, dy2 in self.piecesout_rel_centers[P2]]}

    def get_sticksets_abs_toplefts(self):
        x, y = self.table_rect.topleft  # 게임 테이블의 왼쪽 상단 절대 좌표
        return [(x + dx, y + dy) for dx, dy in self.ssets_rel_toplefts]

    def get_tossedsticks_abs_toplefts(self):
        x, y = self.table_rect.topleft  # 게임 테이블의 왼쪽 상단 절대 좌표
        return [(x + dx, y + dy) for dx, dy in self.tossedsticks_rel_toplefts]

    def get_node_selected(self):
        return self.node_sel

    def get_stickset_selected(self):
        return self.sset_sel

    def get_winner(self):
        return self.winner

    def highlight_nodes(self, nodes):
        self.hlight_nodes = nodes

    def check_node_selection(self, nodes):
        pressed = pygame.mouse.get_pressed()[0]

        if pressed:
            ux, uy = pygame.mouse.get_pos()
            for nodekey in nodes:
                if nodekey == self.NODE_OUT:
                    r = self.piece_radius
                    for x, y in self.piecesout_abs_centers[self.game.cur_player]:
                        if hypot(y - uy, x - ux) < r:
                            self.node_sel = nodekey
                            return nodekey
                else:
                    x, y = self.nodes_abs_centers[nodekey]
                    r = self.normal_node_radius
                    if nodekey in BoardNode.CORNERS or nodekey == self.NODE_WON:
                        r = self.corner_node_radius
                    if hypot(y - uy, x - ux) < r:
                        self.node_sel = nodekey
                        return nodekey

        self.node_sel = None
        return None

    def check_sticksets_selection(self):
        pressed = pygame.mouse.get_pressed()[0]

        if pressed:
            ux, uy = pygame.mouse.get_pos()
            for (comb, sset_im), (x, y) in zip(self.ssets_im.items(), self.ssets_abs_toplefts):
                rect = Rect(x, y, *sset_im.get_size())
                if rect.collidepoint(ux, uy):
                    self.sset_sel = comb
                    return comb

        self.sset_sel = None
        return None

    def check_replay_selection(self):
        pressed = pygame.mouse.get_pressed()[0]

        if pressed:
            ux, uy = pygame.mouse.get_pos()
            if self.playerwins_rect.collidepoint(ux, uy):
                self.game.reset()
                self.check_winner()

    def check_winner(self):
        self.winner = self.game.check_winner()

