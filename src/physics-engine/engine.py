import colorsys
import random
import sys

import pygame

from atom import Atom
from container import Container


class JEngine:
    # engine configuration
    win_width: int
    win_height: int
    win_colour: tuple[int, int, int]
    fps: int

    # engine settings
    obj_limit: int | None
    auto: bool = False
    cycle_colours: bool = False

    # private attributes
    _obj_hue = 0
    _vmax = 1000

    def __init__(
        self,
        size: tuple[int, int] = (1000, 1000),
        background: tuple[int, int, int] = (0, 0, 0),
        obj_limit: int | None = None,
        fps: int = 60,
    ):
        self.win_width, self.win_height = size
        self.win_colour = background
        self.obj_limit = obj_limit
        self.fps = fps

    def simulate(self, caption: str = "Physics Engine"):
        pygame.init()
        screen = pygame.display.set_mode(self.window_size())
        pygame.display.set_caption(caption)
        clock = pygame.time.Clock()
        env = Container(self.window_size())
        obj_count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.auto:
                    if self.obj_limit is None or obj_count < self.obj_limit:
                        coords = pygame.mouse.get_pos()
                        self.spawn_object(env, coords)
                        obj_count += 1
            if self.auto and (self.obj_limit is None or obj_count < self.obj_limit):
                self.spawn_object(env, self.centre())
                obj_count += 1
            screen.fill(self.win_colour)
            env.step(1 / self.fps)
            # env.resolve()
            self.draw_objects(screen, env)
            pygame.display.update()
            clock.tick(self.fps)

    def spawn_object(
        self,
        env: Container,
        pos: tuple[float, float],
        mass: float = 1,
        radius: float = 10,
    ):
        x_vel = random.randint(-self._vmax, self._vmax)
        y_vel = random.randint(-self._vmax, self._vmax)
        atom = Atom(mass, radius, pos, (x_vel, y_vel))
        if self.cycle_colours:
            atom.paint(self.get_next_hue())
        env.add(atom)

    def draw_objects(self, screen: pygame.Surface, env: Container):
        for atom in env.get_objects():
            pygame.draw.circle(screen, atom.colour(), atom.pos(), atom.radius())

    def get_next_hue(self):
        self._obj_hue += 0.05 % 1
        rgb = colorsys.hsv_to_rgb(self._obj_hue, 1, 1)
        return (rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)

    def centre(self) -> tuple[float, float]:
        return (self.win_width / 2, self.win_height / 2)

    def window_size(self) -> tuple[int, int]:
        return (self.win_width, self.win_height)

    def set_obj_limit(self, limit: int):
        self.obj_limit = limit

    def auto_spawn(self, auto: bool):
        self.auto = auto

    def colour_changes(self, cycle: bool):
        self.cycle_colours = cycle


def main():
    """
    Program Flags:
        1. None (default)
            - click to spawn objects
            - no colour variation
        2. Colour Objects (-c)
            - cycle through colours when spawning objects
        3. Auto Mode (-a N)
            - automatically spawn N objects (1 per frame)
            - manual spawning is turned off
    """
    engine = JEngine((800, 800))
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-c":
            engine.colour_changes(True)
        elif sys.argv[i] == "-a":
            if i + 1 >= len(sys.argv):
                print(f"Error: value expected for flag 'auto'")
                sys.exit(1)
            try:
                limit = int(sys.argv[i + 1])
                if limit <= 0:
                    raise ValueError
            except ValueError:
                print(f"Error: invalid value '{limit}' for flag 'auto'")
                sys.exit(1)
            engine.auto_spawn(True)
            engine.set_obj_limit(limit)
    engine.simulate()


if __name__ == "__main__":
    main()
