import pygame
import sys
from backgammon.core.backgammon import BackgammonGame
from backgammon.core.player import PasoMovimiento, SecuenciaMovimiento

# Constants
WIDTH, HEIGHT = 1200, 800
BOARD_COLOR = (244, 226, 198)  # A beige-like color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class PygameUI:
    """
    A class to handle the Pygame user interface for the Backgammon game.
    """

    def __init__(self):
        """
        Initializes the Pygame UI.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Backgammon")
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()

        # Dynamic board layout constants
        self.board_edge = int(WIDTH * 0.02)
        self.point_height = int(HEIGHT * 0.4)

        playing_width = WIDTH - (2 * self.board_edge)
        # Total horizontal space is divided into 12 points and 1 bar.
        # Let's consider the bar to be twice as wide as a point.
        # So, we have 12 + 2 = 14 "units" of width.
        unit_width = playing_width / 14
        self.point_width = int(unit_width)
        self.bar_width = int(unit_width * 2)

        self.checker_radius = int(self.point_width * 0.45)
        self.selected_point = None
        self.point_rects = [None] * 24
        self.bar_rects = {}
        self._calculate_point_rects()
        self._calculate_bar_rects()
        self.used_dice = []
        self.possible_moves = []
        self.possible_dests = []
        self.selected_source = None  # Can be point index or 'bar'

        self.game = BackgammonGame()
        self._setup_game()

    def _calculate_bar_rects(self):
        """Calculates the clickable rects for each player's bar."""
        bar_x = self.board_edge + 6 * self.point_width
        self.bar_rects["blancas"] = pygame.Rect(bar_x, 0, self.bar_width, HEIGHT / 2)
        self.bar_rects["negras"] = pygame.Rect(
            bar_x, HEIGHT / 2, self.bar_width, HEIGHT / 2
        )

    def _setup_game(self):
        """Sets up the players and starts the game."""
        player_configs = [
            {
                "id": "P1",
                "nombre": "Blanco",
                "color": "blancas",
                "direccion": 1,
                "home_points": range(18, 24),
                "entry_point": -1,
            },
            {
                "id": "P2",
                "nombre": "Negro",
                "color": "negras",
                "direccion": -1,
                "home_points": range(0, 6),
                "entry_point": 24,
            },
        ]
        self.game.setup_players(player_configs)
        self.game.start_game()
        self.game.roll_dice()

    def _calculate_point_rects(self):
        """Calculates the clickable rects for each point and stores them."""
        # i is the visual column from left to right
        for i in range(12):
            # Bottom row
            point_x_bottom = self.board_edge + i * self.point_width
            if i >= 6:
                point_x_bottom += self.bar_width

            # The core indices for the bottom row run from 11 (left) to 0 (right)
            core_idx_bottom = 11 - i
            self.point_rects[core_idx_bottom] = pygame.Rect(
                point_x_bottom,
                HEIGHT - self.board_edge - self.point_height,
                self.point_width,
                self.point_height,
            )

            # Top row
            point_x_top = self.board_edge + i * self.point_width
            if i >= 6:
                point_x_top += self.bar_width

            # The core indices for the top row run from 12 (left) to 23 (right)
            core_idx_top = 12 + i
            self.point_rects[core_idx_top] = pygame.Rect(
                point_x_top, self.board_edge, self.point_width, self.point_height
            )

    def _draw_checkers(self):
        """Draws the checkers on the board based on the game state."""
        checker_colors = {"blancas": WHITE, "negras": BLACK}

        # Highlight selected source
        if self.selected_source is not None:
            if self.selected_source == "bar":
                player_color = self.game.get_current_player().get_color()
                rect = self.bar_rects[player_color]
            else:
                rect = self.point_rects[self.selected_source]
            pygame.draw.rect(self.screen, GREEN, rect, 4)

        # Highlight possible destinations
        for dest_idx in self.possible_dests:
            rect = self.point_rects[dest_idx]
            pygame.draw.circle(
                self.screen, GREEN, rect.center, self.checker_radius * 0.3
            )

        # Draw checkers on points
        for point_idx, checkers in enumerate(self.game.board.points):
            if not checkers:
                continue

            rect = self.point_rects[point_idx]
            color = checker_colors[checkers[0].get_color()]

            # Determine stacking direction and base position
            is_top_row = point_idx >= 12
            direction = 1 if is_top_row else -1
            base_y = (
                rect.top + self.checker_radius
                if is_top_row
                else rect.bottom - self.checker_radius
            )

            for i, checker in enumerate(checkers):
                if i >= 5:  # If more than 5 checkers, draw a count
                    count_text = self.font.render(str(len(checkers)), True, RED)
                    # Position the count text on top of the 5th checker
                    text_y = base_y + (4 * 2 * self.checker_radius * direction)
                    self.screen.blit(
                        count_text, (rect.centerx - count_text.get_width() / 2, text_y)
                    )
                    break

                center_x = rect.centerx
                center_y = base_y + (i * 2 * self.checker_radius * direction)
                pygame.draw.circle(
                    self.screen, color, (center_x, center_y), self.checker_radius
                )
                pygame.draw.circle(
                    self.screen, RED, (center_x, center_y), self.checker_radius, 2
                )

        # Draw checkers on the bar
        bar_x = self.board_edge + 6 * self.point_width + self.bar_width / 2
        for color_name, checkers in self.game.board.bar.items():
            color = checker_colors[color_name]
            # Stack white checkers from top-middle, black from bottom-middle
            y_pos = (
                HEIGHT / 2 - self.checker_radius
                if color_name == "blancas"
                else HEIGHT / 2 + self.checker_radius
            )
            direction = -1 if color_name == "blancas" else 1
            for i, checker in enumerate(checkers):
                center_y = y_pos + (i * 2 * self.checker_radius * direction)
                pygame.draw.circle(
                    self.screen, color, (bar_x, center_y), self.checker_radius
                )
                pygame.draw.circle(
                    self.screen, RED, (bar_x, center_y), self.checker_radius, 2
                )

        # Draw borne-off checkers count
        borne_off_x = WIDTH - self.board_edge
        white_borne_off = len(self.game.board.get_borne_off("blancas"))
        black_borne_off = len(self.game.board.get_borne_off("negras"))

        white_text = self.font.render(f"White Off: {white_borne_off}", True, BLACK)
        black_text = self.font.render(f"Black Off: {black_borne_off}", True, WHITE)
        self.screen.blit(
            white_text, (borne_off_x - white_text.get_width() - 10, self.board_edge)
        )
        self.screen.blit(
            black_text,
            (
                borne_off_x - black_text.get_width() - 10,
                HEIGHT - self.board_edge - black_text.get_height(),
            ),
        )

    def _draw_game_info(self):
        """Displays the current player and dice roll."""
        player = self.game.get_current_player()
        dice = self.game.dice.get_values()

        player_text = f"Turn: {player.get_nombre()} ({player.get_color()})"
        dice_text = f"Dice: {dice[0]}, {dice[1]}" if dice else "Dice: Not rolled"

        player_surface = self.font.render(player_text, True, BLACK)
        dice_surface = self.font.render(dice_text, True, BLACK)

        info_x = self.board_edge + 6 * self.point_width + self.bar_width / 2

        self.screen.blit(
            player_surface, (info_x - player_surface.get_width() / 2, self.board_edge)
        )
        self.screen.blit(
            dice_surface, (info_x - dice_surface.get_width() / 2, self.board_edge + 30)
        )

    def _draw_board(self):
        """
        Draws the static elements of the backgammon board using pre-calculated rects.
        """
        # Draw the main board background and frame
        frame_color = (139, 69, 19)  # SaddleBrown
        self.screen.fill(BOARD_COLOR)
        pygame.draw.rect(
            self.screen, frame_color, (0, 0, WIDTH, HEIGHT), self.board_edge * 2
        )

        # Draw the bar
        bar_x = self.board_edge + 6 * self.point_width
        pygame.draw.rect(self.screen, frame_color, (bar_x, 0, self.bar_width, HEIGHT))

        # Points colors
        color1 = (210, 180, 140)  # Tan
        color2 = (139, 115, 85)  # Tan4

        # Draw the points (triangles) and numbers
        for i, rect in enumerate(self.point_rects):
            if rect is None:
                continue

            # Determine color based on visual column
            if i >= 12:
                vis_i = i - 12
            else:
                vis_i = 11 - i
            point_color = (
                color1 if vis_i % 2 != 0 else color2
            )  # Flipped this to match original look

            # Draw triangle
            if i >= 12:  # Top row points down
                pygame.draw.polygon(
                    self.screen,
                    point_color,
                    [rect.topleft, rect.topright, rect.midbottom],
                )
            else:  # Bottom row points up
                pygame.draw.polygon(
                    self.screen,
                    point_color,
                    [rect.bottomleft, rect.bottomright, rect.midtop],
                )

            # Draw number
            ui_number = i + 1
            num_text = self.font.render(str(ui_number), True, BLACK)
            if i >= 12:  # Top row
                self.screen.blit(
                    num_text, (rect.centerx - num_text.get_width() / 2, rect.bottom + 5)
                )
            else:  # Bottom row
                self.screen.blit(
                    num_text, (rect.centerx - num_text.get_width() / 2, rect.top - 25)
                )

    def _get_point_from_pos(self, pos):
        """Converts mouse coordinates to a board point index (0-23)."""
        for i, rect in enumerate(self.point_rects):
            if rect and rect.collidepoint(pos):
                return i
        return None

    def _get_possible_dests(self, source):
        """Get all possible destination points for a selected source."""
        dests = []
        start_point = None if source == "bar" else source

        for option in self.possible_moves:
            for paso in option.secuencia:
                if paso.desde == start_point:
                    if paso.hasta is not None:
                        dests.append(paso.hasta)
        return list(set(dests))

    def _attempt_move(self, source, dest_idx):
        """Finds the correct PasoMovimiento, applies it, and updates the turn state."""
        player = self.game.get_current_player()
        start_idx = None if source == "bar" else source

        # Find a legal move that matches the selected start/end and an available die
        move_to_apply = None
        for option in self.possible_moves:
            for paso in option.secuencia:
                if (
                    paso.desde == start_idx
                    and paso.hasta == dest_idx
                    and paso.dado in self._get_available_dice()
                ):
                    move_to_apply = paso
                    break
            if move_to_apply:
                break

        if not move_to_apply:
            print(f"Invalid move from {source} to {dest_idx}.")
            self.selected_source = None
            self.possible_dests = []
            return

        # The move is valid, so we can apply it.
        # The 'move_to_apply' object is a PasoMovimiento which contains all necessary info.
        secuencia = [move_to_apply]  # aplicar_movimiento expects a list of steps
        self.game.board.aplicar_movimiento(player, secuencia)
        self.used_dice.append(move_to_apply.dado)

        # Reset selection and recalculate moves for the rest of the turn
        self.selected_source = None
        self.possible_dests = []
        available_dice = self._get_available_dice()
        self.possible_moves = self.game.board.enumerar_opciones_legales(
            player, available_dice
        )

        # Check if turn is over
        if not available_dice or not self.possible_moves:
            self._end_turn()

    def _get_current_dice(self):
        """Returns the full list of dice for the current turn, handling doubles."""
        dice = list(self.game.dice.get_values())
        if len(dice) == 2 and dice[0] == dice[1]:
            return [dice[0]] * 4
        return dice

    def _get_available_dice(self):
        """Returns the dice that have not yet been used this turn."""
        available = self._get_current_dice()
        for die in self.used_dice:
            if die in available:
                available.remove(die)
        return available

    def _end_turn(self):
        """Finalizes the current turn and sets up the next one."""
        print("Turn over.")
        self.game.next_turn()
        self.game.roll_dice()
        self.used_dice = []
        self.possible_moves = self.game.board.enumerar_opciones_legales(
            self.game.get_current_player(), self._get_current_dice()
        )

    def _handle_click(self, pos):
        """Handles a mouse click on the board."""
        player = self.game.get_current_player()
        clicked_point = self._get_point_from_pos(pos)

        # Priority 1: Handle moves from the bar
        if self.game.board.jugador_tiene_en_barra(player):
            # If the bar is already selected, check for a valid destination click
            if self.selected_source == "bar":
                if clicked_point in self.possible_dests:
                    self._attempt_move("bar", clicked_point)
                else:  # Click was not on a valid destination, so deselect
                    self.selected_source = None
                    self.possible_dests = []
                return  # Action handled for this click

            # If the bar is NOT selected, check if the click is on the bar to select it
            elif self.bar_rects[player.get_color()].collidepoint(pos):
                self.selected_source = "bar"
                self.possible_dests = self._get_possible_dests(self.selected_source)
                return  # Action handled for this click

            # If click is elsewhere, do nothing (or reset) since player must play from bar
            else:
                self.selected_source = None
                self.possible_dests = []
            return  # IMPORTANT: prevent any other move logic from running

        # Priority 2: Handle regular moves if the bar is empty
        if clicked_point is None:
            self.selected_source = None
            self.possible_dests = []
            return

        # If a checker is already selected
        if self.selected_source is not None:
            # If a valid destination is clicked, attempt the move
            if clicked_point in self.possible_dests:
                self._attempt_move(self.selected_source, clicked_point)
            # If another of the player's checkers is clicked, switch selection
            elif (
                self.game.board.points[clicked_point]
                and self.game.board.points[clicked_point][0].get_color()
                == player.get_color()
            ):
                self.selected_source = clicked_point
                self.possible_dests = self._get_possible_dests(self.selected_source)
            # Otherwise, deselect
            else:
                self.selected_source = None
                self.possible_dests = []
        # If no checker is selected
        else:
            # If one of the player's checkers is clicked, select it
            if (
                self.game.board.points[clicked_point]
                and self.game.board.points[clicked_point][0].get_color()
                == player.get_color()
            ):
                self.selected_source = clicked_point
                self.possible_dests = self._get_possible_dests(self.selected_source)

    def run(self):
        """The main loop of the game."""
        self._end_turn()

        running = True
        while running:
            if not self.used_dice and not self.possible_moves:
                self._end_turn()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(event.pos)

            self.screen.fill(BOARD_COLOR)
            self._draw_board()
            self._draw_checkers()
            self._draw_game_info()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    ui = PygameUI()
    ui.run()
