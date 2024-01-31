import math
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

import pygame


class Game(ABC):
    def __init__(self, screen_size: Optional[tuple] = None) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            screen_size if screen_size else (640, 480)
        )
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def events(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass


class Clock(Game):
    def __init__(
        self, screen_size: tuple | None = None, clock_radius: int = 200
    ) -> None:
        """
        Initialize the clock with the given screen size and clock radius.

        Parameters:
            screen_size (tuple | None): The size of the screen. Defaults to None.
            clock_radius (int): The radius of the clock. Defaults to 200.
        """
        super().__init__(screen_size)
        self.font = pygame.font.Font(None, 36)
        self.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.clock_radius = clock_radius
        self.hour_hand_length = self.clock_radius * 0.5
        self.minute_hand_length = self.clock_radius * 0.75
        self.second_hand_length = self.clock_radius * 0.85

    def run(self) -> None:
        """
        Run the game loop.
        """
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def events(self) -> None:
        """
        This function handles events using the pygame library. It does not take any parameters and does not return any value.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        """
        Update the state of the object.
        """
        pass

    def draw(self) -> None:
        """
        Draws a clock on the screen with the current time, including the clock face, tick marks, and clock hands.
        Does not take any parameters.
        Returns None.
        """
        # Preenche o fundo com a cor
        self.screen.fill((255, 255, 255))

        # Desenha o círculo externo do relógio
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, self.clock_radius, 3)

        # Desenhar os tracinhos ao redor do círculo do relógio
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            inner_radius = self.clock_radius - (15 if i % 15 == 0 else 10)
            outer_radius = self.clock_radius - 5
            inner_point = (
                self.center[0] + int(inner_radius * math.cos(angle)),
                self.center[1] + int(inner_radius * math.sin(angle)),
            )
            outer_point = (
                self.center[0] + int(outer_radius * math.cos(angle)),
                self.center[1] + int(outer_radius * math.sin(angle)),
            )
            pygame.draw.line(self.screen, (0, 0, 0), inner_point, outer_point, 2)

        # Pega a hora atual
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # Renderizando o texto a ser desenhado
        time_text = self.font.render(current_time, True, (0, 0, 0))

        # Desenhando o texto na superfície usando as coordenadas
        self.screen.blit(time_text, (self.center[0] - time_text.get_width() // 2, 100))

        # Desenhando os ponteiros de hora, minuto e segundos
        hour_angle = math.radians(int(now.strftime("%I")) * 30 - 90)
        minute_angle = math.radians(int(now.strftime("%M")) * 6 - 90)
        second_angle = math.radians(int(now.strftime("%S")) * 6 - 90)
        hour_hand_end = (
            self.center[0] + self.hour_hand_length * math.cos(hour_angle),
            self.center[1] + self.hour_hand_length * math.sin(hour_angle),
        )
        minute_hand_end = (
            self.center[0] + self.minute_hand_length * math.cos(minute_angle),
            self.center[1] + self.minute_hand_length * math.sin(minute_angle),
        )
        second_hand_end = (
            self.center[0] + self.second_hand_length * math.cos(second_angle),
            self.center[1] + self.second_hand_length * math.sin(second_angle),
        )

        # Desenhando
        pygame.draw.line(self.screen, (0, 0, 0), self.center, hour_hand_end, 6)
        pygame.draw.line(self.screen, (0, 0, 0), self.center, minute_hand_end, 3)
        pygame.draw.line(self.screen, (255, 0, 0), self.center, second_hand_end, 1)

        pygame.display.flip()


if __name__ == "__main__":
    clock_radius = 200  # Defina o raio do relógio aqui
    clock = Clock(clock_radius=clock_radius)
    clock.run()
