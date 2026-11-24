import importlib
from typing import Any
import pygame

from .game_entity import WallEntity

mazegenerator = importlib.import_module("mazegenerator.mazegenerator")
MazeGenerator: Any = getattr(mazegenerator, "MazeGenerator")


class GameLevel:
    WALL_SIZE = 10        # thickness of walls/pillars
    CORRIDOR_SIZE = 40    # width of corridors (change this to taste)

    def __init__(self, game_screen: pygame.Surface):
        self.screen = game_screen
        self.font = pygame.font.Font(None, 36)
        self.mazegen = MazeGenerator()
        self.current_maze = self.mazegen.maze
        self.level_state = self._build_state()

    # --- grid index -> pixel helpers -------------------------------------
    # Even grid indices are walls, odd indices are corridors.
    def _offset(self, i: int) -> int:
        return ((i + 1) // 2) * self.WALL_SIZE + (i // 2) * self.CORRIDOR_SIZE

    def _size(self, i: int) -> int:
        return self.CORRIDOR_SIZE if i % 2 else self.WALL_SIZE

    def maze_pixel_size(self) -> tuple[int, int]:
        """Use this to size your window."""
        rows, cols = len(self.current_maze), len(self.current_maze[0])
        w = (cols + 1) * self.WALL_SIZE + cols * self.CORRIDOR_SIZE
        h = (rows + 1) * self.WALL_SIZE + rows * self.CORRIDOR_SIZE
        return w, h

    def cell_center(self, r: int, c: int) -> tuple[int, int]:
        """Pixel center of maze cell (r, c) -- handy for placing the player."""
        gr, gc = 2 * r + 1, 2 * c + 1
        return (self._offset(gc) + self.CORRIDOR_SIZE // 2,
                self._offset(gr) + self.CORRIDOR_SIZE // 2)

    # --- drawing ---------------------------------------------------------
    def draw_wall(self, r: int, c: int) -> None:
        """r, c are grid coordinates (0 .. 2*n)."""
        WallEntity(
            self.screen,
            self._offset(c), self._offset(r),
            self._size(c), self._size(r),
        ).draw()

    def run(self) -> None:
        self.screen.fill('black')
        if not self.current_maze:
            return

        rows, columns = len(self.current_maze), len(self.current_maze[0])
        R, C = 2 * rows + 1, 2 * columns + 1

        # pillars (even, even)
        for r in range(0, R, 2):
            for c in range(0, C, 2):
                self.draw_wall(r, c)

        # walls between cells
        for r in range(rows):
            for c in range(columns):
                self.print_border(
                    self.current_maze[r][c], 2 * r + 1, 2 * c + 1
                )

        self._place_pacgums()

    def print_border(self, val: int, r: int, c: int) -> None:
        if val & (1 << 0):
            self.draw_wall(r - 1, c)   # north
        if val & (1 << 1):
            self.draw_wall(r, c + 1)   # east
        if val & (1 << 2):
            self.draw_wall(r + 1, c)   # south
        if val & (1 << 3):
            self.draw_wall(r, c - 1)   # west

    def write_text_to_screen(
        self,
        txt: str,
        px: int,
        py: int,
        color: tuple[int, int, int] = (255, 255, 255)
    ) -> None:
        text_surface = self.font.render(txt, True, color)
        text_rect = text_surface.get_rect(center=(px, py))
        self.screen.blit(text_surface, text_rect)

    def _build_state(self) -> list[list[int]]:
        R, C = len(self.current_maze), len(self.current_maze[0])
        ret = [[1 for _ in range(C)] for _ in range(R)]
        for r in range(R):
            for c in range(C):
                if self.current_maze[r][c] == 15:
                    ret[r][c] = 0
        return ret

    def _place_pacgums(self) -> None:
        R, C = len(self.level_state), len(self.level_state[0])
        for r in range(R):
            for c in range(C):
                if not self.level_state[r][c]:
                    continue
                gum_rad = 4
                if (
                    (r == 0 and c == 0) or
                    (r == 0 and c == C-1) or
                    (r == R-1 and c == 0) or
                    (r == R-1 and c == C-1)
                ):
                    gum_rad = 8
                pygame.draw.circle(
                    self.screen,
                    (25, 125, 25),
                    self.cell_center(r, c),
                    gum_rad
                )
