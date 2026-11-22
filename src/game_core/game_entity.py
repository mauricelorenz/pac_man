from __future__ import annotations
from abc import ABC
import pygame


class GameEntity(ABC):
    def __init__(
        self,
        screen: pygame.Surface,
        px: int,
        py: int,
        width: int,
        height: int
    ):
        pass


class WallEntity(GameEntity):
    def __init__(
        self,
        screen: pygame.Surface,
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

    def draw(self) -> None:
        pygame.draw.rect(
            self.screen,
            self.color,
            (self.px, self.py, self.width, self.height)
        )
