import math
import pygame


class Rope:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_y = screen_height // 2
        self.marker_x = float(screen_width // 2)

        self.left_win_x = 180
        self.right_win_x = screen_width - 180
        self.pull_step = 12

        # Task 3: Track rope movement so visual tension can
        # respond to the intensity of the struggle.
        self.previous_marker_x = self.marker_x
        self.tension = 0.0

    def pull_left(self, strength=1.0):
        self.marker_x -= self.pull_step * strength

    def pull_right(self, strength=1.0):
        self.marker_x += self.pull_step * strength

    def check_winner(self):
        if self.marker_x <= self.left_win_x:
            return "PLAYER"
        if self.marker_x >= self.right_win_x:
            return "COMPUTER"
        return None

    def reset(self):
        self.marker_x = float(self.screen_width // 2)
        self.previous_marker_x = self.marker_x
        self.tension = 0.0

    def update_tension(self):
        # Measure how much the marker has moved since the
        # previous frame.
        movement = abs(self.marker_x - self.previous_marker_x)

        # Smooth the tension value so the animation does not
        # change too abruptly.
        target_tension = min(movement / 4.0, 1.0)
        self.tension += (target_tension - self.tension) * 0.2

        self.previous_marker_x = self.marker_x

    def render(self, surface):
        self.update_tension()

        start_x = 60
        end_x = self.screen_width - 60

        # Task 3: Increase sag and vibration as tension rises.
        time_value = pygame.time.get_ticks() / 1000.0

        sag_amount = 5 + (self.tension * 25)
        vibration_amount = self.tension * 5

        points = []

        segments = 40

        for i in range(segments + 1):
            progress = i / segments
            x = start_x + (end_x - start_x) * progress

            # The rope sags most strongly around the middle.
            sag = math.sin(progress * math.pi) * sag_amount

            # Add a small high-frequency vibration when tension
            # is high.
            vibration = (
                math.sin(
                    time_value * 25 + progress * 35
                )
                * vibration_amount
            )

            y = self.center_y + sag + vibration

            points.append((int(x), int(y)))

        pygame.draw.lines(
            surface,
            (180, 140, 90),
            False,
            points,
            10
        )

        pygame.draw.line(
            surface,
            (50, 200, 50),
            (self.left_win_x, self.center_y - 40),
            (self.left_win_x, self.center_y + 40),
            4
        )

        pygame.draw.line(
            surface,
            (200, 50, 50),
            (self.right_win_x, self.center_y - 40),
            (self.right_win_x, self.center_y + 40),
            4
        )

        pygame.draw.line(
            surface,
            (120, 120, 120),
            (self.screen_width // 2, self.center_y - 20),
            (self.screen_width // 2, self.center_y + 20),
            2
        )

        flag_rect = pygame.Rect(
            int(self.marker_x) - 12,
            self.center_y - 24,
            24,
            48
        )

        pygame.draw.rect(
            surface,
            (230, 40, 40),
            flag_rect,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            (255, 255, 255),
            flag_rect,
            width=2,
            border_radius=4
        )