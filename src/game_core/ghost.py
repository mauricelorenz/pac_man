from .game_entity import GameEntity
import pygame
from .pac_man import PacMan
from .game_levels import GameLevel
import enum
from collections import deque


class GhostType(enum.Enum):
    SHADOW = 0
    SPEEDY = 1
    BASHFUL = 2
    CLYDE = 3


class Ghost(GameEntity):
    MOVE_DELAY_MS = 550

    def __init__(
        self,
        row: int,
        col: int,
        radius: int,
        screen: pygame.Surface,
        level: GameLevel,
        pacman: PacMan,
        ghost_type: GhostType = GhostType.SHADOW,
        color: tuple[int, int, int] = (2, 78, 120)
    ):
        self.row = row
        self.col = col
        self.radius = radius
        self.screen = screen
        self.pacman = pacman
        self.g_type = ghost_type
        self.color = color
        self.level = level
        self.last_move = pygame.time.get_ticks()

    def draw(self) -> None:
        pygame.draw.circle(
            self.screen,
            self.color,
            self.level.cell_center(self.row, self.col),
            self.radius
        )
        self.update()

    def update(self) -> None:
        if self.g_type == GhostType.SHADOW:
            self._shadow_movement()

    def _shadow_movement(self) -> None:
        now = pygame.time.get_ticks()

        if now - self.last_move < self.MOVE_DELAY_MS:
            return
        self.last_move = now

        pr, pc = self.pacman.row, self.pacman.col
        dxns = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        parents: dict[tuple[int, int], tuple[int, int]] = dict()
        seen = set([(pr, pc)])

        q = deque([(pr, pc)])
        while q:
            cnt = len(q)
            for _ in range(cnt):
                r, c = q.popleft()
                if self.row == r and self.col == c:
                    self.row, self.col = parents.get((r, c), (r, c))
                    return

                for i, (dr, dc) in enumerate(dxns):
                    if self.level.current_maze[r][c] & (1 << i) != 0:
                        continue
                    if (r+dr, c+dc) in seen:
                        continue
                    q.append((r + dr, c + dc))
                    parents[(r+dr, c+dc)] = (r, c)
                    seen.add((r+dr, c+dc))
