from __future__ import annotations
from abc import ABC, abstractmethod
import pygame


class GameEntity(ABC):
    def __init__(
        self, 
        screen: pygame.display, 
        px: int, 
        py: int, 
        width: int, 
        height: int
    ):
        pass
    
    @abstractmethod
    def intersect_with(self, other: GameEntity) -> bool:
        pass    


class WallEntity(GameEntity):
    def __init__(
        self, 
        screen: pygame.display,
        px: int,
        py: int,
        width: int, 
        height: int, 
        color: tuple[int, int, int] = (255, 0, 0)
    ):
        self.screen = screen
        self.width = width
        self.height = height
        self.px = px
        self.py = py
        self.color = color

    def draw(self):
        pygame.draw.rect(
            self.screen, 
            self.color, 
            (self.px, self.py, self.width, self.height),
            width=2, border_radius=3
        )

    def intersect_with(self, other: GameEntity) -> bool:
        return False
    