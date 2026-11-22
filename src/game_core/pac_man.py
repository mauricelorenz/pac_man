from .game_entity import GameEntity
from .game_levels import GameLevel
import pygame


class PacMan(GameEntity):
    MOVE_DELAY_MS = 150   # time between cell steps

    def __init__(
        self,
        row: int,
        col: int,
        radius: int,
        height: int,
        screen: pygame.Surface,
        level: GameLevel
    ):
        self.row = row
        self.col = col
        self.radius = radius
        self.screen = screen
        self.level = level
        self.dr = 0   # row direction
        self.dc = 0   # column direction
        self.last_move = pygame.time.get_ticks()

    def draw(self) -> None:
        pygame.draw.circle(
            self.screen, (255, 234, 0),
            self.level.cell_center(self.row, self.col),
            self.radius,
        )
        self.update()

    def handle_user_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_UP]:
            self.dr, self.dc = -1, 0
        elif keys[pygame.K_DOWN]:
            self.dr, self.dc = 1, 0
        elif keys[pygame.K_LEFT]:
            self.dr, self.dc = 0, -1
        elif keys[pygame.K_RIGHT]:
            self.dr, self.dc = 0, 1

    def update(self) -> None:
        now = pygame.time.get_ticks()
        if now - self.last_move < self.MOVE_DELAY_MS:
            return
        self.last_move = now

        cell = self.level.current_maze[self.row][self.col]
        if self.dr == -1 and cell & (1 << 0):
            self.dr = 0   # north wall
        if self.dc == 1 and cell & (1 << 1):
            self.dc = 0   # east wall
        if self.dr == 1 and cell & (1 << 2):
            self.dr = 0   # south wall
        if self.dc == -1 and cell & (1 << 3):
            self.dc = 0   # west wall

        self.row += self.dr
        self.col += self.dc
