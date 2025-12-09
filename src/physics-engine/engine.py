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
        - rectangular environment
    2. Colour Objects (-c)
        - cycle through colours when spawning objects
    3. Auto Mode (-a N)
        - automatically spawn N objects (1 per frame)
        - manual spawning is turned off
    4. Set Radius (-r N)
        - compatible with manual or auto mode
        - sets the default radius of an object
    5. Set V-Max (-v N)
        - set maximum object speed in simulation
    6. Set Spawn Velocity (-s X Y)
        - set the velocity with which objects are spawned
        - this will be unchanging
        - i.e. '-s 0 100' to send objects straight down
    7. Random Radii (-R)
        - each object will spawn with a random radius
        - will be ±10 from the default radius
    8. Circular Environment (-C)
        - physics environment will be circular
    """
    engine = Engine((800, 800), fps=120)
    for i in range(1, len(sys.argv)):
        match sys.argv[i]:
            case "-c":
                engine.change_colours(True)
            case "-a":
                limit = _check_next_arg(i, "auto", "int")
                engine.auto_spawn(True)
                engine.set_obj_limit(limit)
            case "-r":
                radius = _check_next_arg(i, "radius", "float")
                engine.set_default_radius(radius)
            case "-v":
                vel = _check_next_arg(i, "v-max", "int")
                engine.set_vmax(vel)
            case "-s":
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
    _env: PhysicsEnvironment
    _obj_hue = 0
    _vmax: int = 500
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
        self._env = PhysicsEnvironment(self.window_size())
        obj_count = 0
        frame_count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self._manual_valid(obj_count):
                        coords = pygame.mouse.get_pos()
                        self.spawn_object(coords, self._default_radius)
                        obj_count += 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self._env.clear()
            if self._auto_valid(obj_count, frame_count):
                self.spawn_object(self.centre(), self._default_radius)
                obj_count += 1
            self._env.update(1 / self.fps, sub_steps=2)
            window.fill(self.win_colour)
            self.draw_objects(window)
            pygame.display.update()
            clock.tick(self.fps)
            frame_count += 1

    def spawn_object(
        self,
        pos: tuple[float, float],
        radius: float,
        vel: tuple[float, float] | None = None,
        mass: float = 1,
    ):
        if self._env is None:
            return
        if vel is None:
            atom = Atom(mass, radius, pos, self.spawn_velocity())
        else:
            atom = Atom(mass, radius, pos, self.scale(vel))
        if self.cycle_colours:
            atom.paint(self.get_next_hue())
        self._env.add(atom)

    def draw_objects(self, surface: pygame.Surface):
        if self._env is None:
            return
        for atom in self._env.get_objects():
            pygame.draw.circle(surface, atom.colour(), atom.position(), atom.radius())

    def get_next_hue(self):
        self._obj_hue += 0.05 % 1
        rgb = colorsys.hsv_to_rgb(self._obj_hue, 1, 1)
        return (rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)

    def centre(self) -> tuple[float, float]:
        return (self.win_width / 2, self.win_height / 2)

    def window_size(self) -> tuple[int, int]:
        return (self.win_width, self.win_height)

    def spawn_velocity(self) -> tuple[float, float]:
        if self.constant_velocity:
            x_vel, y_vel = self._default_velocity
        else:
            x_vel, y_vel = self.random_velocity(self._vmax)
        return self.scale((x_vel, y_vel))

    def set_obj_limit(self, limit: int):
        self.obj_limit = limit

    def scale(self, vel: tuple[float, float]) -> tuple[float, float]:
        dt = 1 / self.fps
        return (vel[0] * dt, vel[1] * dt)

    def auto_spawn(self, auto: bool):
        self.auto = auto

    def change_colours(self, cycle: bool):
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

    def _auto_valid(self, obj_count: int, frame_count: int) -> bool:
        return (
            self.auto
            and (self.obj_limit is None or obj_count < self.obj_limit)
            and frame_count % 10 == 0
        )

    def _manual_valid(self, obj_count: int) -> bool:
        return not self.auto and (self.obj_limit is None or obj_count < self.obj_limit)


if __name__ == "__main__":
    main()
