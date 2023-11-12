"""
Constants defined for other files.
"""


class PYGAME_CONSTANTS:
    """
    Constants for pygame config.
    """

    WIDTH: int = 1000
    HEIGHT: int = 1000
    FPS: int = 120
    WINDOW_TITLE: str = "t-tiny, y-small, u-big, a-particles, v-vectors"

    VECTOR_WIDTH: int = 2
    VECTOR_LENGTH_MULTI: int = 10


class COLORS:
    """
    Colors for pygame.
    """

    BLACK: tuple = 0, 0, 0
    WHITE: tuple = 255, 255, 255
    RED: tuple = 168, 13, 21
    BLUE: tuple = 0, 0, 255
    GREEN: tuple = 0, 255, 0

    BACKGROUND_COLOR: tuple = BLACK
    SPAWN_VECTOR_COLOR: tuple = GREEN
    VELOCITY_VECTORS_COLOR: tuple = BLUE
    PLANET_COLOR: tuple = RED


class PHYSICS_CONSTANTS:
    """
    Constants for physics.
    """

    # Constants for physics
    GRAVITATIONAL_CONSTANT: float = 0.1

    # Planet constants
    MAX_PLANET_RADIUS: int = 100
    MIN_PLANET_RADIUS: int = 2
    DEFAULT_PLANET_DENSITY: float = 1
    SMALL_PLANET_MASS: int = 10
    DEFAULT_PLANET_MASS: int = 200
    BIG_PLANET_MASS: int = 10000

    # Vector constants
    VELOCITY_LOSS_FACTOR: float = 0.9
    SPAWN_VECTOR_DIVIDER: int = 50

    # Particle constants
    PARTICLES_PER_CLICK: int = 50
