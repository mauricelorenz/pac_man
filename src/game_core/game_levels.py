import pygame
from mazegenerator.mazegenerator import MazeGenerator
from .game_entity import WallEntity


class GameLevel:
    CELL_SIZE = 25
    WALL_THICKNESS = 3
    WALL_SEGMENTS = 3
    TILE_WALL_SIZE = 25
    FLOOR_SIZE = 2 * TILE_WALL_SIZE

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
        R, C = 2*rows + 1, 2*columns + 1

        for r in range(0, R, 2):
            for c in range(0, C, 2):
                WallEntity(
                    self.screen, 
                    c * self.CELL_SIZE, 
                    r * self.CELL_SIZE, 
                    self.CELL_SIZE, self.CELL_SIZE
                ).draw()
        
        for r in range(rows):
            for c in range(columns):
                cell_value = self.current_maze[r][c]
                self.print_border(cell_value, 2*r+1, 2*c+1)

    def print_border(self, val: int, r: int, c: int):
        if val & (1 << 0):
            WallEntity(
                self.screen, 
                self.CELL_SIZE * (c), 
                self.CELL_SIZE * (r - 1), 
                self.CELL_SIZE, self.CELL_SIZE
            ).draw()
    
        if val & (1 << 1):
            WallEntity(
                self.screen, 
                self.CELL_SIZE * (c + 1), 
                self.CELL_SIZE * (r), 
                self.CELL_SIZE, self.CELL_SIZE
            ).draw()
        
        if val & (1 << 2):
            WallEntity(
                self.screen, 
                self.CELL_SIZE * (c), 
                self.CELL_SIZE * (r + 1), 
                self.CELL_SIZE, self.CELL_SIZE
            ).draw()

        if val & (1 << 3):
            WallEntity(
                self.screen, 
                self.CELL_SIZE * (c - 1), 
                self.CELL_SIZE * (r), 
                self.CELL_SIZE, self.CELL_SIZE
            ).draw()

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
    
    def draw_wall(self, r: int, c: int):
        wall = self.TILE_WALL_SIZE
        floor = self.FLOOR_SIZE
        stride = wall + floor

        x = (c // 2) * stride + (c % 2) * wall
        y = (r // 2) * stride + (r % 2) * wall

        width = floor if c % 2 else wall
        height = floor if r % 2 else wall

        WallEntity(self.screen, x, y, width, height).draw()
