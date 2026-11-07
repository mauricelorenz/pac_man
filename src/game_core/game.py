import pygame


class CoreGameEngine:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        while self.running:

            self.handle_events() # handle this like key press etc

            # RENDER YOUR GAME HERE
            self.main_menu()

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60
        self.release_resources()

    def release_resources(self):
        pygame.font.quit()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            print("open main game") # TODO insert function to open screen with maze gen level here

    def main_menu(self):

        def write_text_to_screen(txt: str, px: int, py: int):
            text_surface = self.font.render(txt, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(px, py))
            self.screen.blit(text_surface, text_rect)

        self.screen.fill("black")

        write_text_to_screen("PAC-MAN", 300, 200)
        write_text_to_screen("Press SPACE to start", 300, 250)
        write_text_to_screen("High Scores", 300, 300)

        for i in range(4):
            write_text_to_screen(f"Player{i+1}", 300, 320 + (20 * i))



if __name__ == "__main__":
    game_engine = CoreGameEngine()
    game_engine.draw()