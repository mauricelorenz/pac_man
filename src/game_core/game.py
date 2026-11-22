import pygame
from .game_levels import GameLevel
from ..config import Config


class CoreGameEngine:
    def __init__(
        self,
        config: Config,
        width: int = 1280,
        height: int = 800
    ):
        pygame.init()
        pygame.font.init()
        self.w_wdith = width
        self.w_height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.show_main_menu = True
        self.game_level = GameLevel(self.screen)

    def run_loop(self) -> None:
        while self.running:

            self.handle_events()

            # RENDER YOUR GAME HERE
            if self.show_main_menu:
                self.main_menu()
            else:
                self.load_game_levels()

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60
        self.release_resources()

    def release_resources(self) -> None:
        pygame.font.quit()
        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.show_main_menu = False

    def main_menu(self) -> None:

        def write_text_to_screen(
            txt: str, px: int, py: int,
            color: tuple[int, int, int] = (255, 255, 255)
        ) -> None:
            text_surface = self.font.render(txt, True, color)
            text_rect = text_surface.get_rect(center=(px, py))
            self.screen.blit(text_surface, text_rect)

        self.screen.fill("black")

        write_text_to_screen(
            "PAC-MAN", self.w_wdith // 2, 200, (255, 255, 0)
        )
        write_text_to_screen(
            "Press SPACE to start", self.w_wdith // 2, 250
        )
        write_text_to_screen(
            "High Scores", self.w_wdith // 2, 300
        )

        for i in range(4):
            write_text_to_screen(
                f"Player{i+1}  200",
                self.w_wdith // 2, 340 + (25 * i)
            )

    def load_game_levels(self) -> None:
        self.game_level.run()
