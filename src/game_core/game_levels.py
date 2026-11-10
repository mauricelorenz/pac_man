import pygame
from mazegenerator.mazegenerator import MazeGenerator
from .game_entity import WallEntity


class GameLevel:
    CELL_SIZE = 25
    WALL_THICKNESS = 3
    WALL_SEGMENTS = 3

    def __init__(self, game_screen: pygame.display):
        self.screen = game_screen
        self.font = pygame.font.Font(None, 36)
        self.mazegen = MazeGenerator()
        self.current_maze = self.mazegen.maze

    def run(self):
        self.screen.fill('black')
        if not self.current_maze:
            return

        rows, columns = len(self.current_maze), len(self.current_maze[0])

        for r in range(rows):
            for c in range(columns):
                g_val = self.current_maze[r][c]

                x = c * self.CELL_SIZE
                y = r * self.CELL_SIZE
                self.print_border(g_val, 0, x, y)
                self.print_border(g_val, 1, x, y)
                self.print_border(g_val, 2, x, y)
                self.print_border(g_val, 3, x, y)

    def print_border(self, val: int, dxn: int, px: int, py: int):
        if val & (1 << dxn) == 0:
            return

        segment_length = (
            self.CELL_SIZE - (self.WALL_SEGMENTS - 1) * self.WALL_THICKNESS
        ) // self.WALL_SEGMENTS
        spacing = segment_length + self.WALL_THICKNESS

        for i in range(self.WALL_SEGMENTS):
            offset = i * spacing
            if dxn == 0:  # top
                x, y = px + offset, py
                width, height = segment_length, self.WALL_THICKNESS
            elif dxn == 1:  # right
                x, y = px + self.CELL_SIZE - self.WALL_THICKNESS, py + offset
                width, height = self.WALL_THICKNESS, segment_length
            elif dxn == 2:  # bottom
                x, y = px + offset, py + self.CELL_SIZE - self.WALL_THICKNESS
                width, height = segment_length, self.WALL_THICKNESS
            elif dxn == 3:  # left
                x, y = px, py + offset
                width, height = self.WALL_THICKNESS, segment_length
            else:
                raise ValueError(f'Unknown wall direction: {dxn}')

            WallEntity(self.screen, x, y, width, height).draw()

    def write_text_to_screen(
        self, 
        txt: str, 
        px: int, 
        py: int, 
        color: tuple[int, int, int] = (255, 255, 255)
    ):
        text_surface = self.font.render(txt, True, color)
        text_rect = text_surface.get_rect(center=(px, py))
        self.screen.blit(text_surface, text_rect)
