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


class COLORS:
    """
    Colors for pygame.
    """

    BLACK: tuple = 0, 0, 0
    WHITE: tuple = 255, 255, 255
    RED: tuple = 168, 13, 21
    BLUE: tuple = 0, 0, 255
    GREEN: tuple = 0, 255, 0


class PHYSICS_CONSTANTS:
    """
    Constants for physics.
    """

    GRAVITATIONAL_CONSTANT: float = 0.1
    MAX_PLANET_RADIUS: int = 100
    MIN_PLANET_RADIUS: int = 2
    DEFAULT_PLANET_DENSITY: float = 1
    VELOCITY_LOSS_FACTOR: float = 0.9
