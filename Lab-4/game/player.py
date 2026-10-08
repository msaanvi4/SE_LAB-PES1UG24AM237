import math
import pygame


class Puller:
    """Represents a puller character anchor on either side of the rope."""

    def __init__(self, x, y, color, label):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.font = pygame.font.SysFont(None, 24)

        # Task 3: Animation state.
        self.lean = 0.0

    def set_lean(self, lean):
        """Set the character's leaning angle in degrees."""
        self.lean = max(-25.0, min(25.0, lean))

    def render(self, surface):
        """Draw avatar with a dynamic leaning posture."""

        # Create a transparent surface for the character so the
        # body and head can be rotated together.
        character_surface = pygame.Surface(
            (100, 140),
            pygame.SRCALPHA
        )

        center_x = 50
        body_y = 55

        # Body
        body_rect = pygame.Rect(
            center_x - 20,
            body_y - 35,
            40,
            70
        )

        pygame.draw.rect(
            character_surface,
            self.color,
            body_rect,
            border_radius=6
        )

        # Head
        pygame.draw.circle(
            character_surface,
            (240, 210, 180),
            (center_x, body_y - 50),
            16
        )

        # Rotate the character to create a leaning posture.
        rotated_character = pygame.transform.rotate(
            character_surface,
            self.lean
        )

        character_rect = rotated_character.get_rect(
            center=(self.x, self.y)
        )

        surface.blit(
            rotated_character,
            character_rect
        )

        # Name / control tag remains readable below the character.
        label_surf = self.font.render(
            self.label,
            True,
            (240, 240, 240)
        )

        surface.blit(
            label_surf,
            (
                self.x - label_surf.get_width() // 2,
                self.y + 45
            )
        )