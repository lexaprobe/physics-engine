# Simple 2D Physics Engine

This project is not supposed to be sophisticated or fast. It's more so just a proof of concept that I created out of interest in the topic. I'm working on a more robust and expandable physics engine that can be found in [this repo](https://github.com/lexaprobe/JEngine).

## How to Run

To start the engine with its default behaviour, run the following command. Add any of the optional flags to customise the engine's behaviour.

```bash
python src/physics-engine/main.py
```

### Program Flags

- Default Behaviour (no arguments)
  - click to spawn objects
  - no colour variation
  - rectangular environment
- Colour Objects `-c`
  - cycle through colours when spawning objects
- Auto Mode `-a N`
  - automatically spawn $N$ objects
  - manual spawning is turned off
- Set Radius `-r N`
  - compatible with manual or auto mode
  - sets the default radius of an object
- Set V-Max `-v N`
  - set maximum object speed in simulation
- Set Spawn Velocity `-s X Y`
  - set the velocity with which objects are spawned
  - this will be unchanging
  - i.e. `-s 0 100` to send objects straight down
- Random Radii `-R`
  - each object will spawn with a random radius
  - will be $±10$ from the default radius
- Circular Environment `-C`
  - use a circle rather than a rectangle for an an environment
