import random
import pygame
from game.rope import Rope
from game.player import Puller


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rope = Rope(width, height)

        self.player = Puller(
            90,
            height // 2,
            (50, 120, 220),
            "PLAYER (A/D)"
        )

        self.computer = Puller(
            width - 90,
            height // 2,
            (220, 80, 50),
            "COMPUTER"
        )

        # Task 1: Alternating A/D input.
        self.last_key = None

        self.winner = None
        self.game_state = "PLAYING"

        # Task 2: Normal computer behavior.
        self.normal_computer_cooldown = 180
        self.normal_computer_strength = (0.7, 1.2)

        # Task 2: Panic surge behavior.
        # Faster and stronger than normal, but still beatable.
        self.panic_threshold = 260
        self.panic_computer_cooldown = 120
        self.panic_computer_strength = (1.0, 1.4)

        self.computer_pull_cooldown = self.normal_computer_cooldown
        self.last_computer_pull = pygame.time.get_ticks()
        self.panic_mode = False

        # Task 4: Match timer.
        self.match_duration = 45
        self.match_start_time = pygame.time.get_ticks()
        self.sudden_death = False

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 26)

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d):

                # Task 1: Only accept alternating A/D presses.
                if event.key != self.last_key:

                    # Task 4: Double player pulling power
                    # during Sudden Death.
                    player_strength = 2.0 if self.sudden_death else 1.0

                    self.rope.pull_left(player_strength)
                    self.last_key = event.key

    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()

        # --------------------------------------------------
        # TASK 4: MATCH TIMER
        # --------------------------------------------------

        elapsed_seconds = (
            now - self.match_start_time
        ) / 1000.0

        if elapsed_seconds >= self.match_duration:
            self.sudden_death = True

        # --------------------------------------------------
        # TASK 2: AI PANIC SURGE
        # --------------------------------------------------

        player_distance = (
            self.rope.marker_x - self.rope.left_win_x
        )

        if player_distance <= self.panic_threshold:
            self.panic_mode = True

            # Faster reaction than normal computer.
            self.computer_pull_cooldown = (
                self.panic_computer_cooldown
            )

            # Stronger pulling than normal computer.
            computer_strength = random.uniform(
                *self.panic_computer_strength
            )

        else:
            self.panic_mode = False

            self.computer_pull_cooldown = (
                self.normal_computer_cooldown
            )

            computer_strength = random.uniform(
                *self.normal_computer_strength
            )

        # --------------------------------------------------
        # TASK 4: SUDDEN DEATH
        # --------------------------------------------------

        if self.sudden_death:
            # Double computer pulling power.
            computer_strength *= 2.0

        # Computer automatically pulls.
        if (
            now - self.last_computer_pull
            >= self.computer_pull_cooldown
        ):
            self.rope.pull_right(computer_strength)
            self.last_computer_pull = now

        # --------------------------------------------------
        # TASK 3: PULLER LEANING
        # --------------------------------------------------

        center_x = self.width / 2

        position_difference = (
            self.rope.marker_x - center_x
        )

        lean_amount = max(
            -20.0,
            min(
                20.0,
                position_difference / 8.0
            )
        )

        self.player.set_lean(-lean_amount)
        self.computer.set_lean(lean_amount)

        # --------------------------------------------------
        # WINNER CHECK
        # --------------------------------------------------

        result = self.rope.check_winner()

        if result:
            self.winner = result
            self.game_state = "GAME_OVER"

    def reset(self):
        self.rope.reset()

        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"

        self.computer_pull_cooldown = (
            self.normal_computer_cooldown
        )

        self.last_computer_pull = pygame.time.get_ticks()

        self.panic_mode = False

        # Task 4: Reset timer and sudden death.
        self.match_start_time = pygame.time.get_ticks()
        self.sudden_death = False

        # Task 3: Reset leaning.
        self.player.set_lean(0)
        self.computer.set_lean(0)

    def render(self, screen):
        screen.fill((30, 32, 36))

        mud_rect = pygame.Rect(
            self.width // 2 - 120,
            self.height // 2 - 80,
            240,
            160
        )

        pygame.draw.rect(
            screen,
            (45, 38, 30),
            mud_rect,
            border_radius=12
        )

        self.rope.render(screen)

        self.player.render(screen)
        self.computer.render(screen)

        # --------------------------------------------------
        # TASK 4: LIVE TIMER
        # --------------------------------------------------

        now = pygame.time.get_ticks()

        elapsed_seconds = (
            now - self.match_start_time
        ) / 1000.0

        remaining_seconds = max(
            0,
            self.match_duration - elapsed_seconds
        )

        timer_text = f"TIME: {remaining_seconds:04.1f}s"

        timer_surf = self.font_small.render(
            timer_text,
            True,
            (240, 240, 240)
        )

        screen.blit(
            timer_surf,
            (
                self.width // 2
                - timer_surf.get_width() // 2,
                10
            )
        )

        # Instructions.
        inst_surf = self.font_small.render(
            "Alternate [A] and [D] keys rapidly to pull!",
            True,
            (210, 210, 210)
        )

        screen.blit(
            inst_surf,
            (
                self.width // 2
                - inst_surf.get_width() // 2,
                40
            )
        )

        # --------------------------------------------------
        # TASK 2: PANIC INDICATOR
        # --------------------------------------------------

        if self.panic_mode:
            panic_surf = self.font_small.render(
                "COMPUTER PANIC SURGE!",
                True,
                (255, 180, 60)
            )

            screen.blit(
                panic_surf,
                (
                    self.width // 2
                    - panic_surf.get_width() // 2,
                    75
                )
            )

        # --------------------------------------------------
        # TASK 4: SUDDEN DEATH INDICATOR
        # --------------------------------------------------

        if self.sudden_death:
            sudden_surf = self.font_small.render(
                "SUDDEN DEATH! PULLING POWER x2",
                True,
                (255, 80, 80)
            )

            screen.blit(
                sudden_surf,
                (
                    self.width // 2
                    - sudden_surf.get_width() // 2,
                    105
                )
            )

        # --------------------------------------------------
        # GAME OVER
        # --------------------------------------------------

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = f"{self.winner} WINS!"

            color = (
                (80, 220, 80)
                if self.winner == "PLAYER"
                else (240, 80, 80)
            )

            text_surf = self.font_big.render(
                win_text,
                True,
                color
            )

            screen.blit(
                text_surf,
                (
                    self.width // 2
                    - text_surf.get_width() // 2,
                    self.height // 2 - 50
                )
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again",
                True,
                (240, 240, 240)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2
                    - restart_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )