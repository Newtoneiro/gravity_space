"""An abstraction of planet on which the calculations are made."""


from __future__ import annotations

import pygame
import math

from gravity.constants import PYGAME_CONSTANTS, COLORS, PHYSICS_CONSTANTS


class Planet:
    """
    Abstraction representing a planet.
    Responsible for calculating the gravitational force exerted on it by other planets,
    and for drawing itself.
    """

    def __init__(
        self,
        win: pygame.Surface,
        mass: float,
        init_x: int,
        init_y: int,
        init_vector: list[int],
        is_stationary: bool = False,
        is_particle: bool = False,
        density: float = PHYSICS_CONSTANTS.DEFAULT_PLANET_DENSITY,
    ):
        self._win = win
        self._mass = mass
        self._x = init_x
        self._y = init_y
        self._vector = init_vector
        self._is_stationary = is_stationary
        self._is_particle = is_particle
        self._density = density

        self._calculate_radius()

    def _calculate_radius(self) -> None:
        """
        Calculate the Planet's radius from it's mass and density,
        using the formula V = m/d = 4/3(pi)(r^3). => r = (3 * m / 4 * pi * d) ** (1/3).

        If the Planet's radius exceeds the set boundaries, it get's reduced.
        """
        self._radius = (3 / 4 * math.pi) * (self._mass / self._density) ** (1 / 3)
        if self._radius > PHYSICS_CONSTANTS.MAX_PLANET_RADIUS:
            self._radius = PHYSICS_CONSTANTS.MAX_PLANET_RADIUS
        elif self._radius < PHYSICS_CONSTANTS.MIN_PLANET_RADIUS:
            self._radius = PHYSICS_CONSTANTS.MIN_PLANET_RADIUS

    def _check_and_update_boundary(
        self, axis: int, limit: int, radius: float, vector_index: int
    ) -> int:
        """
        Checks if the planet is within the boundaries of the simulation space.
        If the planet is outside the boundaries, it is bounced back with a reduced velocity.

        Args:
            axis (int): The current position of the planet on the given axis.
            limit (int): The maximum position of the planet on the given axis.
            radius (float): The radius of the planet.
            vector_index (int): The index of the vector component that corresponds to the given axis.

        Returns:
            int: The updated position of the planet on the given axis.
        """
        if axis < radius:
            axis = 1 + radius
            self._vector[vector_index] = (
                -PHYSICS_CONSTANTS.VELOCITY_LOSS_FACTOR * self._vector[vector_index]
            )
        elif axis > limit - radius:
            axis = limit - radius
            self._vector[vector_index] = (
                -PHYSICS_CONSTANTS.VELOCITY_LOSS_FACTOR * self._vector[vector_index]
            )

        return axis

    def calculate_impact_on(self, other: Planet) -> None:
        """
        Calculate the gravitational force between self and other Planet, and update
        the vector accordingly.

        Args:
            other(Planet): other planet, relative to which we calculate the gravitational force.
        """
        if self._is_stationary or self == other:
            # Stationary planets don't exert force on other planets
            return

        if self._is_particle and other._is_particle:
            # Particles don't exert force on each other
            return

        d = math.sqrt((self._x - other._x) ** 2 + (self._y - other._y) ** 2)
        if d <= self._radius + other._radius:
            # So the forces won't get extreme, when the planets get close
            return

        dx = self._x - other._x
        dy = self._y - other._y
        gravitational_force = (  # From the formula F = G * M * m / d^2
            PHYSICS_CONSTANTS.GRAVITATIONAL_CONSTANT * self._mass * other._mass
        ) / d**2
        Fx = gravitational_force * dx / d
        Fy = gravitational_force * dy / d

        self._vector[0] += -Fx / self._mass  # Update according to x acceleration
        self._vector[1] += -Fy / self._mass  # Update according to y acceleration

    def update(self) -> None:
        """
        Update the position of the planet, and check for collisions with the boundaries.
        """
        self._x += self._vector[0]
        self._y += self._vector[1]

        self._x = self._check_and_update_boundary(
            self._x, PYGAME_CONSTANTS.WIDTH, self._radius, 0
        )
        self._y = self._check_and_update_boundary(
            self._y, PYGAME_CONSTANTS.HEIGHT, self._radius, 1
        )

    def draw(self, show_velocity_vectors: bool = False) -> None:
        """
        Draw the planet on the canvas. If show_velocity_vectors is True, also draw the
        velocity vector of the planet.
        """
        pygame.draw.circle(
            surface=self._win,
            color=COLORS.PLANET_COLOR,
            center=(self._x, self._y),
            radius=self._radius,
        )
        if show_velocity_vectors:
            pygame.draw.line(
                surface=self._win,
                color=COLORS.VELOCITY_VECTORS_COLOR,
                start_pos=(self._x, self._y),
                end_pos=(
                    self._x + PYGAME_CONSTANTS.VECTOR_LENGTH_MULTI * self._vector[0],
                    self._y + PYGAME_CONSTANTS.VECTOR_LENGTH_MULTI * self._vector[1],
                ),
                width=PYGAME_CONSTANTS.VECTOR_WIDTH,
            )
