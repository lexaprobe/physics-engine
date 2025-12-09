import sys
from typing import Any

from engine import Engine


def main():
    """
    Program Flags:\n
    Default Behaviour
        - click to spawn objects
        - no colour variation
        - rectangular environment
    Colour Objects (-c)
        - cycle through colours when spawning objects
    Auto Mode (-a N)
        - automatically spawn N objects (1 per frame)
        - manual spawning is turned off
    Set Radius (-r N)
        - compatible with manual or auto mode
        - sets the default radius of an object
    Set V-Max (-v N)
        - set maximum object speed in simulation
    Set Spawn Velocity (-s X Y)
        - set the velocity with which objects are spawned
        - this will be unchanging
        - i.e. '-s 0 100' to send objects straight down
    Random Radii (-R)
        - each object will spawn with a random radius
        - will be ±10 from the default radius
    Circular Environment (-C)
        - use a circle rather than a rectangle for an env
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
            case "-R":
                engine.random_obj_radius(True)
            case "-C":
                engine.circular_environment(True)
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


if __name__ == "__main__":
    main()
