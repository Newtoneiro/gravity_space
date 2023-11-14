"""An abstraction of canvas, on which the planets interact with eachother."""

import pygame

from gravity.objects.planet import Planet


class Canvas:
    """
    Abstraction representing the sky, on which the planets interact.
    Responsible for updating the planets' positions and displaying other features.
    """

    def __init__(self, win: pygame.Surface):
        self._win = win
        self._planets = []
        self._show_vectors = False

    def toggle_vectors_display(self) -> None:
        """
        Switch between displaying planets' vectors and not doing that.
        """
        self._show_vectors = not self._show_vectors

    def clear(self) -> None:
        """
        Removes all planets from the canvas.
        """
        self._planets = []

    def add_planet(
        self,
        mass: float,
        init_x: int,
        init_y: int,
        init_vector: list[float],
        is_stationary: bool = False,
        is_particle: bool = False,
    ) -> None:
        """
        Initialize and add a planet to the canvas.

        Args:
            mass(float): the mass of the planet
            init_x(int): the initial x coordinate of the planet
            init_y(int): the initial y coordinate of the planet
            init_vector(list[float]): the initial velocity vector of the planet
            is_stationary(bool): whether the planet is stationary or not
        """
        self._planets.append(
            Planet(self._win, mass, init_x, init_y, init_vector, is_stationary, is_particle)
        )

    def update(self) -> None:
        """
        Update the positions of the planets and draw them.
        """
        for planet1 in self._planets:
            for planet2 in self._planets:
                if planet1 == planet2:
                    continue
                planet1.calculate_impact_on(planet2)

            planet1.update()
