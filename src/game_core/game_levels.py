import pygame
from mazegenerator.mazegenerator import MazeGenerator
from .game_entity import WallEntity


class GameLevel:
    def __init__(self, game_screen: pygame.display):
        self.screen = game_screen
        self.font = pygame.font.Font(None, 36)
        self.mazegen = MazeGenerator()
        self.current_maze = self.mazegen.maze

    def run(self):
        self.screen.fill('black')
        R, C = len(self.current_maze), len(self.current_maze[0])

        for r in range(R):
            for c in range(C):
                g_val = self.current_maze[r][c]

                if r == 0:
                    self.print_border(g_val, 0, 25*r, 25*c)
                    self.print_border(g_val, 3, 25*r, 25*c)
                    
                self.print_border(g_val, 1, 25*r, 25*c)
                self.print_border(g_val, 2, 25*r, 25*c)

    def print_border(self, val: int, dxn: int, px: int, py: int):
        if val & (1 << dxn)  == 0:
            return
        wall = WallEntity(self.screen, ) #draw the cell
        wall.draw()
        for i in range(3):
            if dxn == 0:
                pass
            elif dxn == 1:
                pass
            elif dxn == 2:
                pass
            else:
                pass

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
