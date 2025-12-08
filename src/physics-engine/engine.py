import colorsys
import random
import sys
from typing import Any

import pygame
from atom import Atom
from environment import PhysicsEnvironment


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
        4. Set Radius (-r N)
            - compatible with manual or auto mode
        5. Set V-Max (-v N)
            - set maximum object speed in simulation
        6. Set Spawn Velocity (-s X Y)
            - set the velocity with which objects are spawned
            - this will be unchanging
            - i.e. '-s 0 100' to send objects straight down
    """
    engine = Engine((800, 800), fps=120)
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-c":
            engine.colour_changes(True)
        elif sys.argv[i] == "-a":
            limit = _check_next_arg(i, "auto", "int")
            engine.auto_spawn(True)
            engine.set_obj_limit(limit)
        elif sys.argv[i] == "-r":
            radius = _check_next_arg(i, "radius", "float")
            engine.set_default_radius(radius)
        elif sys.argv[i] == "-v":
            vel = _check_next_arg(i, "v-max", "int")
            engine.set_vmax(vel)
        elif sys.argv[i] == "-s":
            x_vel = _check_next_arg(i, "spawn velocity", "float")
            y_vel = _check_next_arg(i + 1, "spawn velocity", "float")
            engine.constrain_velocity((x_vel, y_vel))

    engine.simulate()


def _check_next_arg(index: int, flag: str, type: str) -> Any:
    if index + 1 >= len(sys.argv):
        print(f"Error: value expected for flag '{flag}'", file=sys.stderr)
        sys.exit(1)
    try:
        value: Any
        match type:
            case "int":
                value = int(sys.argv[index + 1])
            case "float":
                value = float(sys.argv[index + 1])
            case _:
                raise TypeError(
                    "Invalid argument for 'type'\nExpected 'float' or 'int'"
                )
        if value < 0:
            raise ValueError
    except ValueError:
        print(f"Error: invalid value '{value}' for flag '{flag}'", file=sys.stderr)
        sys.exit(1)
    return value


class Engine:
    # engine configuration
    win_width: int
    win_height: int
    win_colour: tuple[int, int, int]
    fps: int

    # engine settings
    obj_limit: int | None
    auto: bool = False
    cycle_colours: bool = False
    constant_velocity: bool = False

    # private attributes
    _obj_hue = 0
    _vmax: int = 1000
    _default_radius: float = 10
    _default_velocity: tuple[float, float]

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
        window = pygame.display.set_mode(self.window_size())
        pygame.display.set_caption(caption)
        clock = pygame.time.Clock()
        env = PhysicsEnvironment(self.window_size())
        obj_count = 0
        frame_count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.auto:
                    if self.obj_limit is None or obj_count < self.obj_limit:
                        coords = pygame.mouse.get_pos()
                        self.spawn_object(env, coords, self._default_radius)
                        obj_count += 1
            if (
                self.auto
                and (self.obj_limit is None or obj_count < self.obj_limit)
                and frame_count % 10 == 0
            ):
                self.spawn_object(env, self.centre(), self._default_radius)
                obj_count += 1
            env.update(1 / self.fps, sub_steps=2)
            window.fill(self.win_colour)
            self.draw_objects(window, env)
            pygame.display.update()
            clock.tick(self.fps)
            frame_count += 1

    def spawn_object(
        self,
        env: PhysicsEnvironment,
        pos: tuple[float, float],
        radius: float,
        vel: tuple[float, float] | None = None,
        mass: float = 1,
    ):
        if vel is None:
            if self.constant_velocity:
                x_vel, y_vel = self._default_velocity
            else:
                x_vel, y_vel = self.random_velocity(self._vmax)
            atom = Atom(mass, radius, pos, (x_vel, y_vel))
        else:
            atom = Atom(mass, radius, pos, vel)
        if self.cycle_colours:
            atom.paint(self.get_next_hue())
        env.add(atom)

    def draw_objects(self, surface: pygame.Surface, env: PhysicsEnvironment):
        for atom in env.get_objects():
            pygame.draw.circle(surface, atom.colour(), atom.position(), atom.radius())

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

    def set_default_radius(self, value: float):
        self._default_radius = value

    def set_vmax(self, value: int):
        self._vmax = value

    def constrain_velocity(self, value: tuple[float, float]):
        self.constant_velocity = True
        self._default_velocity = value

    def release_velocity(self):
        self.constant_velocity = False

    def random_velocity(self, maximum: int) -> tuple[float, float]:
        x = random.randint(-maximum, maximum)
        y = random.randint(-maximum, maximum)
        return (x, y)


if __name__ == "__main__":
    main()
