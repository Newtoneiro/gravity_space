"""Main file presenting the whole program in action."""

import pygame

from gravity.objects.canvas import Canvas
from gravity.constants import PYGAME_CONSTANTS, COLORS, PHYSICS_CONSTANTS


class Simulation:
    """
    Class representing the whole simulation.
    """

    # ============== INITIALIZATION =============== #

    def __init__(self, init_planets: list = None) -> None:
        self._init_pygame()
        self._init_enviroment()
        self._init_canvas(init_planets)

    def _init_pygame(self) -> None:
        """
        Initializes pygame.
        """
        pygame.init()
        pygame.display.set_caption(PYGAME_CONSTANTS.WINDOW_TITLE)
        self._win = pygame.display.set_mode(
            (PYGAME_CONSTANTS.WIDTH, PYGAME_CONSTANTS.HEIGHT)
        )
        self._clock = pygame.time.Clock()

    def _init_enviroment(self) -> None:
        """
        Initializes the enviroment.
        """
        self._last_pos_clicked = [0, 0]
        self._selected_mass = PHYSICS_CONSTANTS.DEFAULT_PLANET_MASS
        self._hold = False
        self._run = True

    def _init_canvas(self, init_planets: list) -> None:
        """
        Initializes the canvas.
        """
        self._canvas = Canvas(self._win)
        for planet in init_planets:
            self._canvas.add_planet(*planet)

    # =============================================== #

    def run(self) -> None:
        """
        Runs the simulation.
        """
        self._init_event_callbacks()
        while self._run:
            self._win.fill(COLORS.BLACK)
            self._clock.tick(PYGAME_CONSTANTS.FPS)
            self._canvas.update()

            self._draw_action_vector()
            self._draw_planets()
            self._handle_events()

            pygame.display.flip()

    def _draw_action_vector(self) -> None:
        """
        Draw action vector when holding mouse button.
        """
        if self._hold:
            pygame.draw.line(
                surface=self._win,
                color=COLORS.SPAWN_VECTOR_COLOR,
                start_pos=self._last_pos_clicked,
                end_pos=pygame.mouse.get_pos(),
                width=PYGAME_CONSTANTS.VECTOR_WIDTH,
            )

    def _draw_planets(self) -> None:
        """
        Draws all planets on the canvas.
        """
        for planet in self._canvas._planets:
            planet.draw(self._canvas._show_vectors)

    def _handle_events(self) -> None:
        """
        Handles all events.
        """
        for event in pygame.event.get():
            self._event_callbacks.get(event.type, lambda _: None)(event)

    def _init_event_callbacks(self) -> None:
        """
        Initializes pygame callbacks.
        """
        self._key_to_mass = {
            pygame.K_t: lambda: self._handle_mass_change(
                PHYSICS_CONSTANTS.SMALL_PLANET_MASS
            ),
            pygame.K_y: lambda: self._handle_mass_change(
                PHYSICS_CONSTANTS.DEFAULT_PLANET_MASS
            ),
            pygame.K_u: lambda: self._handle_mass_change(
                PHYSICS_CONSTANTS.BIG_PLANET_MASS
            ),
        }

        self._event_callbacks = {
            pygame.QUIT: lambda event: self._handle_stop(event),
            pygame.MOUSEBUTTONDOWN: lambda event: self._handle_mouse_down(event),
            pygame.MOUSEBUTTONUP: lambda event: self._handle_mouse_up(event),
            pygame.KEYDOWN: lambda event: self._handle_key_down(event),
        }

        self._key_callbacks = {
            pygame.K_c: self._handle_clear,
            pygame.K_v: self._handle_show_vectors,
            pygame.K_a: self._handle_add_particles,
            **self._key_to_mass,
        }

    # ================== EVENT HANDLERS ================== #

    def _handle_stop(self, event: pygame.event.Event) -> None:
        """
        Stops the simulation.
        """
        self._run = False

    def _handle_mouse_down(self, event: pygame.event.Event) -> None:
        """
        Handles mouse down event.
        """
        self._hold = True
        self._last_pos_clicked = pygame.mouse.get_pos()

    def _handle_mouse_up(self, event: pygame.event.Event) -> None:
        """
        Handles mouse up event.
        """
        self._hold = False
        finalx, finaly = pygame.mouse.get_pos()
        spawnx, spawny = self._last_pos_clicked
        velx = (finalx - spawnx) / PHYSICS_CONSTANTS.SPAWN_VECTOR_DIVIDER
        vely = (finaly - spawny) / PHYSICS_CONSTANTS.SPAWN_VECTOR_DIVIDER
        self._canvas.add_planet(
            mass=self._selected_mass,
            init_x=spawnx,
            init_y=spawny,
            init_vector=[velx, vely],
            is_stationary=False,
        )

    def _handle_key_down(self, event: pygame.event.Event) -> None:
        """
        Handles key down event.
        """
        self._key_callbacks.get(event.key, lambda: None)()

    # ================== KEY CALLBACKS ================== #

    def _handle_clear(self) -> None:
        """
        Handles clear event.
        """
        self._canvas.clear()

    def _handle_show_vectors(self) -> None:
        """
        Handles show vectors event.
        """
        self._canvas.toggle_vectors_display()

    def _handle_add_particles(self) -> None:
        """
        Handles add particles event.
        """
        x, y = pygame.mouse.get_pos()
        for i in range(PHYSICS_CONSTANTS.PARTICLES_PER_CLICK):
            self._canvas.add_planet(
                mass=1,
                init_x=x,
                init_y=y + i,
                init_vector=[1, 1],
                is_stationary=False,
                is_particle=True,
            )

    def _handle_mass_change(self, mass: int) -> None:
        """
        Handles mass change event.
        """
        self._selected_mass = mass


if __name__ == "__main__":
    init_planets = [[10**5, 500, 500, [0, 0], True]]
    simulation = Simulation(init_planets)
    simulation.run()
