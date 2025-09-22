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

        # Board layout constants
        self.point_width = 50
        self.point_height = 200
        self.bar_width = 100
        self.board_edge = 20
        self.checker_radius = 20
        self.selected_point = None
        self.point_rects = [None] * 24
        self._calculate_point_rects()
        self.used_dice = []
        self.possible_moves = []

        self.game = BackgammonGame()
        self._setup_game()

    def _setup_game(self):
        """Sets up the players and starts the game."""
        player_configs = [
            {
                "id": "P1", "nombre": "Blanco", "color": "blancas", "direccion": 1,
                "home_points": range(18, 24), "entry_point": -1
            },
            {
                "id": "P2", "nombre": "Negro", "color": "negras", "direccion": -1,
                "home_points": range(0, 6), "entry_point": 24
            }
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
            if i >= 6: point_x_bottom += self.bar_width

            # The core indices for the bottom row run from 11 (left) to 0 (right)
            core_idx_bottom = 11 - i
            self.point_rects[core_idx_bottom] = pygame.Rect(point_x_bottom, HEIGHT - self.board_edge - self.point_height, self.point_width, self.point_height)

            # Top row
            point_x_top = self.board_edge + i * self.point_width
            if i >= 6: point_x_top += self.bar_width

            # The core indices for the top row run from 12 (left) to 23 (right)
            core_idx_top = 12 + i
            self.point_rects[core_idx_top] = pygame.Rect(point_x_top, self.board_edge, self.point_width, self.point_height)

    def _draw_checkers(self):
        """Draws the checkers on the board based on the game state."""
        checker_colors = {"blancas": WHITE, "negras": BLACK}

        # Highlight selected point
        if self.selected_point is not None:
            rect = self.point_rects[self.selected_point]
            pygame.draw.rect(self.screen, GREEN, rect, 4) # 4 is the width of the border

        # Draw checkers on points
        for point_idx, checkers in enumerate(self.game.board.points):
            if not checkers:
                continue

            rect = self.point_rects[point_idx]
            color = checker_colors[checkers[0].get_color()]

            # Determine stacking direction and base position
            is_top_row = point_idx >= 12
            direction = 1 if is_top_row else -1
            base_y = rect.top + self.checker_radius if is_top_row else rect.bottom - self.checker_radius

            for i, checker in enumerate(checkers):
                if i >= 5: # If more than 5 checkers, draw a count
                    count_text = self.font.render(str(len(checkers)), True, RED)
                    # Position the count text on top of the 5th checker
                    text_y = base_y + (4 * 2 * self.checker_radius * direction)
                    self.screen.blit(count_text, (rect.centerx - count_text.get_width() / 2, text_y))
                    break

                center_x = rect.centerx
                center_y = base_y + (i * 2 * self.checker_radius * direction)
                pygame.draw.circle(self.screen, color, (center_x, center_y), self.checker_radius)
                pygame.draw.circle(self.screen, RED, (center_x, center_y), self.checker_radius, 2)

        # Draw checkers on the bar
        bar_x = self.board_edge + 6 * self.point_width + self.bar_width / 2
        for color_name, checkers in self.game.board.bar.items():
            color = checker_colors[color_name]
            # Stack white checkers from top-middle, black from bottom-middle
            y_pos = HEIGHT / 2 - self.checker_radius if color_name == "blancas" else HEIGHT / 2 + self.checker_radius
            direction = -1 if color_name == "blancas" else 1
            for i, checker in enumerate(checkers):
                center_y = y_pos + (i * 2 * self.checker_radius * direction)
                pygame.draw.circle(self.screen, color, (bar_x, center_y), self.checker_radius)
                pygame.draw.circle(self.screen, RED, (bar_x, center_y), self.checker_radius, 2)

        # Draw borne-off checkers count
        borne_off_x = WIDTH - self.board_edge
        white_borne_off = len(self.game.board.get_borne_off("blancas"))
        black_borne_off = len(self.game.board.get_borne_off("negras"))

        white_text = self.font.render(f"White Off: {white_borne_off}", True, BLACK)
        black_text = self.font.render(f"Black Off: {black_borne_off}", True, WHITE)
        self.screen.blit(white_text, (borne_off_x - white_text.get_width() - 10, self.board_edge))
        self.screen.blit(black_text, (borne_off_x - black_text.get_width() - 10, HEIGHT - self.board_edge - black_text.get_height()))

    def _draw_game_info(self):
        """Displays the current player and dice roll."""
        player = self.game.get_current_player()
        dice = self.game.dice.get_values()

        player_text = f"Turn: {player.get_nombre()} ({player.get_color()})"
        dice_text = f"Dice: {dice[0]}, {dice[1]}" if dice else "Dice: Not rolled"

        player_surface = self.font.render(player_text, True, BLACK)
        dice_surface = self.font.render(dice_text, True, BLACK)

        info_x = self.board_edge + 6 * self.point_width + self.bar_width / 2

        self.screen.blit(player_surface, (info_x - player_surface.get_width()/2, self.board_edge))
        self.screen.blit(dice_surface, (info_x - dice_surface.get_width()/2, self.board_edge + 30))

    def _draw_board(self):
        """
        Draws the static elements of the backgammon board using pre-calculated rects.
        """
        # Draw the main board background and frame
        frame_color = (139, 69, 19) # SaddleBrown
        self.screen.fill(BOARD_COLOR)
        pygame.draw.rect(self.screen, frame_color, (0, 0, WIDTH, HEIGHT), self.board_edge * 2)

        # Draw the bar
        bar_x = self.board_edge + 6 * self.point_width
        pygame.draw.rect(self.screen, frame_color, (bar_x, 0, self.bar_width, HEIGHT))

        # Points colors
        color1 = (210, 180, 140)  # Tan
        color2 = (139, 115, 85)   # Tan4

        # Draw the points (triangles) and numbers
        for i, rect in enumerate(self.point_rects):
            if rect is None: continue

            # Determine color based on visual column
            if i >= 12: vis_i = i - 12
            else: vis_i = 11 - i
            point_color = color1 if vis_i % 2 != 0 else color2 # Flipped this to match original look

            # Draw triangle
            if i >= 12: # Top row points down
                pygame.draw.polygon(self.screen, point_color, [rect.topleft, rect.topright, rect.midbottom])
            else: # Bottom row points up
                pygame.draw.polygon(self.screen, point_color, [rect.bottomleft, rect.bottomright, rect.midtop])

            # Draw number
            ui_number = i + 1
            num_text = self.font.render(str(ui_number), True, BLACK)
            if i >= 12: # Top row
                self.screen.blit(num_text, (rect.centerx - num_text.get_width()/2, rect.bottom + 5))
            else: # Bottom row
                self.screen.blit(num_text, (rect.centerx - num_text.get_width()/2, rect.top - 25))


    def _get_point_from_pos(self, pos):
        """Converts mouse coordinates to a board point index (0-23)."""
        for i, rect in enumerate(self.point_rects):
            if rect and rect.collidepoint(pos):
                return i
        return None

    def _attempt_move(self, start_idx, end_idx):
        """
        Attempts to make a move, interfacing with the core logic.

        NOTE: This is a simplified implementation to provide basic interactivity.
        The core game logic is designed around evaluating and applying full turns
        (sequences of moves), which is ideal for an AI but not for a direct
        human-in-the-loop UI. A more robust implementation would require either
        refactoring the core logic to be more UI-friendly or building a much
        more complex state machine in the UI to manage the turn.
        """
        player = self.game.get_current_player()

        move_dist = abs(start_idx - end_idx)

        available_dice = list(self.game.dice.get_values())
        for die in self.used_dice:
            if die in available_dice:
                available_dice.remove(die)

        if move_dist not in available_dice:
            print(f"Invalid move: No available die for distance {move_dist}")
            return

        # Check if this move is legal according to the core logic
        is_legal = False
        for option in self.possible_moves:
            for paso in option.secuencia:
                if paso.desde == start_idx and paso.hasta == end_idx:
                    is_legal = True
                    break
            if is_legal:
                break

        if not is_legal:
            print("Move not found in legal options.")
            return

        # Create and apply the move
        is_capture = len(self.game.board.points[end_idx]) == 1 and self.game.board.points[end_idx][0].get_color() != player.get_color()
        paso = PasoMovimiento(desde=start_idx, hasta=end_idx, dado=move_dist, captura=is_capture)
        secuencia = SecuenciaMovimiento([paso])
        self.game.board.aplicar_movimiento(player, secuencia)
        self.used_dice.append(move_dist)

        # Check if turn is over
        if len(self.used_dice) >= len(self.game.dice.get_values()):
            self.game.next_turn()
            self.game.roll_dice()
            self.used_dice = []
            self.possible_moves = self.game.board.enumerar_opciones_legales(self.game.get_current_player(), self.game.dice)


    def run(self):
        """
        The main loop of the game.
        """
        self.possible_moves = self.game.board.enumerar_opciones_legales(self.game.get_current_player(), self.game.dice)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_point = self._get_point_from_pos(event.pos)

                    if self.selected_point is None:
                        # Nothing selected, try to select a point
                        if clicked_point is not None and self.game.board.points[clicked_point]:
                            checker_color = self.game.board.points[clicked_point][0].get_color()
                            if checker_color == self.game.get_current_player().get_color():
                                self.selected_point = clicked_point
                    else:
                        # A point is already selected, try to move
                        if clicked_point is not None and clicked_point != self.selected_point:
                            self._attempt_move(self.selected_point, clicked_point)
                        self.selected_point = None # Deselect after move attempt


            self.screen.fill(BOARD_COLOR)

            self._draw_board()
            self._draw_checkers()
            self._draw_game_info()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    ui = PygameUI()
    ui.run()
