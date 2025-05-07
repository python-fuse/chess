import copy
import pygame

from colors import RED, WHITE, YELLOW, with_alpha

pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60
SQUARE_SIZE = SCREEN_WIDTH // 8
EMPTY_SQUARE = "--"
EMPTY_POSITION = (None, None)


# TODO: Filter out exposing moves


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("uChess")
        self.clock = pygame.time.Clock()
        self.selected_pos = (None, None)
        self.selected_piece = None
        self.turn = "white"
        self.valid_moves = []
        self.target_square = (None, None)
        self.checked_king = EMPTY_POSITION

        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp"] * 8,
            [EMPTY_SQUARE] * 8,
            [EMPTY_SQUARE] * 8,
            [EMPTY_SQUARE] * 8,
            [EMPTY_SQUARE] * 8,
            ["wr"] * 8,
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]

    def draw_board(self):
        board_image = "assets/board.png"
        board = pygame.image.load(board_image)
        board = pygame.transform.scale(board, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(board, (0, 0))

    def load_images(self):
        self.images = {}

        pieces = [
            "wp",
            "wr",
            "wb",
            "wn",
            "wq",
            "wk",
            "bp",
            "br",
            "bb",
            "bn",
            "bq",
            "bk",
        ]

        for piece in pieces:
            self.images[piece] = pygame.image.load(f"assets/{piece}.png")
            self.images[piece] = pygame.transform.scale(
                self.images[piece], (SQUARE_SIZE, SQUARE_SIZE)
            )

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != EMPTY_SQUARE:
                    self.screen.blit(
                        self.images[piece],
                        pygame.Rect(
                            col * SQUARE_SIZE,
                            row * SQUARE_SIZE,
                            SQUARE_SIZE,
                            SQUARE_SIZE,
                        ),
                    )

    def handle_click(self):
        x, y = (
            pygame.mouse.get_pos()[0] // SQUARE_SIZE,
            pygame.mouse.get_pos()[1] // SQUARE_SIZE,
        )

        if self.selected_pos == (x, y):
            self.selected_pos = (None, None)
            self.selected_piece = EMPTY_SQUARE
            self.generate_moves()
        elif (x, y) in self.valid_moves:
            self.target_square = (x, y)
            self.capture(start=self.selected_pos, end=self.target_square)
        else:
            self.selected_pos = (x, y)
            self.selected_piece = self.board[y][x]
            self.generate_moves()

    def capture(self, start, end):
        if self.board[start[1]][start[0]][0] != self.turn[0]:
            return False

        piece = self.board[start[1]][start[0]]
        captured_piece = self.board[end[1]][end[0]]

        self.board[end[1]][end[0]] = piece
        self.board[start[1]][start[0]] = EMPTY_SQUARE

        if self.is_in_check(self.turn[0]):
            self.board[start[1]][start[0]] = piece
            self.board[end[1]][end[0]] = captured_piece
            self.checked_king = EMPTY_POSITION
            return False

        opponent_color = "b" if self.turn[0] == "w" else "w"
        opponent_in_check = self.is_in_check(opponent_color)

        if opponent_in_check:
            print(f"{opponent_color} is in check!")

        self.swap_turns()
        return True

    def swap_turns(self):
        self.turn = "white" if self.turn == "black" else "black"

    def generate_moves(self):
        x, y = self.selected_pos
        self.valid_moves.clear()
        selected_piece = self.selected_piece[1].lower()

        if self.selected_piece != EMPTY_SQUARE:
            if selected_piece == "p":
                dir = -1 if self.turn == "white" else 1

                if (self.turn == "white" and y == 6) or (
                    self.turn == "black" and y == 1
                ):
                    if self.board[y + (dir * 2)][x] == EMPTY_SQUARE:
                        self.valid_moves.append((x, y + (dir * 2)))

                if self.board[y + (dir)][x] == EMPTY_SQUARE:
                    self.valid_moves.append((x, y + dir))

                if x + 1 <= 7:
                    target_square = self.board[y + dir][x + 1]
                    if (
                        target_square != EMPTY_SQUARE
                        and target_square[0] != self.turn[0]
                    ):
                        self.valid_moves.append((x + 1, y + dir))

                if x - 1 >= 0:
                    target_square = self.board[y + dir][x - 1]
                    if (
                        target_square != EMPTY_SQUARE
                        and target_square[0] != self.turn[0]
                    ):
                        self.valid_moves.append((x - 1, y + dir))

            if selected_piece == "n":
                knight_moves = (
                    (x + 2, y + 1),
                    (x + 2, y - 1),
                    (x - 2, y + 1),
                    (x - 2, y - 1),
                    (x + 1, y + 2),
                    (x + 1, y - 2),
                    (x - 1, y + 2),
                    (x - 1, y - 2),
                )

                for move in knight_moves:
                    if (move[0] < 0) or (move[0] > 7) or (move[1] < 0) or (move[1] > 7):
                        continue
                    if (
                        self.board[move[1]][move[0]] == EMPTY_SQUARE
                        or self.board[move[1]][move[0]][0] != self.turn[0]
                    ):
                        self.valid_moves.append(move)

            if selected_piece == "r":
                rook_directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

                for rook_x, rook_y in rook_directions:
                    current_x = x
                    current_y = y

                    while True:
                        current_y += rook_y
                        current_x += rook_x

                        if (
                            (current_x < 0)
                            or (current_x > 7)
                            or (current_y < 0)
                            or (current_y > 7)
                        ):
                            break

                        square = self.board[current_y][current_x]

                        if square == EMPTY_SQUARE:
                            self.valid_moves.append((current_x, current_y))
                            continue

                        if square[0] != self.turn[0]:
                            self.valid_moves.append((current_x, current_y))
                            break

                        if square[0] == self.turn[0]:
                            break

            if selected_piece == "b":
                bishop_directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))

                for dx, dy in bishop_directions:
                    current_x = x
                    current_y = y

                    while True:
                        current_y += dy
                        current_x += dx

                        if (
                            (current_x < 0)
                            or (current_x > 7)
                            or (current_y < 0)
                            or (current_y > 7)
                        ):
                            break

                        square = self.board[current_y][current_x]

                        if square == EMPTY_SQUARE:
                            self.valid_moves.append((current_x, current_y))
                            continue

                        if square[0] != self.turn[0]:
                            self.valid_moves.append((current_x, current_y))
                            break

                        if square[0] == self.turn[0]:
                            break

            if selected_piece == "k":
                king_moves = (
                    (x, y + 1),
                    (x, y - 1),
                    (x - 1, y),
                    (x + 1, y),
                    (x + 1, y + 1),
                    (x + 1, y - 1),
                    (x - 1, y + 1),
                    (x - 1, y - 1),
                )

                for move in king_moves:
                    if (move[0] < 0) or (move[0] > 7) or (move[1] < 0) or (move[1] > 7):
                        continue
                    if (
                        self.board[move[1]][move[0]] == EMPTY_SQUARE
                        or self.board[move[1]][move[0]][0] != self.turn[0]
                    ):
                        self.valid_moves.append(move)

            if selected_piece == "q":
                queen_directions = (
                    (1, 1),
                    (1, -1),
                    (-1, 1),
                    (-1, -1),
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1),
                )

                for dx, dy in queen_directions:
                    current_x = x
                    current_y = y

                    while True:
                        current_y += dy
                        current_x += dx

                        if (
                            (current_x < 0)
                            or (current_x > 7)
                            or (current_y < 0)
                            or (current_y > 7)
                        ):
                            break

                        square = self.board[current_y][current_x]

                        if square == EMPTY_SQUARE:
                            self.valid_moves.append((current_x, current_y))
                            continue

                        if square[0] != self.turn[0]:
                            self.valid_moves.append((current_x, current_y))
                            break

                        if square[0] == self.turn[0]:
                            break

        self.filter_illegal_moves()

    def draw_valid_moves(self):
        for move in self.valid_moves:
            move_highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            move_highlight.fill(with_alpha(WHITE, 0))

            if self.selected_piece[0] != self.turn[0]:
                return

            pygame.draw.circle(
                move_highlight,
                with_alpha(RED, 100),
                (SQUARE_SIZE // 2, SQUARE_SIZE // 2),
                10,
            )
            self.screen.blit(
                move_highlight, (move[0] * SQUARE_SIZE, move[1] * SQUARE_SIZE)
            )

    def get_rook_attacks(self, x, y, board=[]):
        rook_directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        board = self.board if board == [] else board
        attacks = []
        color = board[y][x][0]

        for dx, dy in rook_directions:
            cx, cy = x + dx, y + dy
            while 0 <= cx < 8 and 0 <= cy < 8:
                target = board[cy][cx]
                if target == EMPTY_SQUARE:
                    attacks.append((cx, cy))
                else:
                    if target[0] != color:
                        attacks.append((cx, cy))
                    break
                cx += dx
                cy += dy
        return attacks

    def get_knight_attacks(self, x, y):
        moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        attacks = []

        for dx, dy in moves:
            cx, cy = x + dx, y + dy
            if 0 <= cx <= 7 and 0 <= cy <= 7:
                attacks.append((cx, cy))

        return attacks

    def get_bishop_attacks(self, x, y, board=[]):
        board = self.board if board == [] else board
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        attacks = []
        color = board[y][x][0]

        for dx, dy in directions:
            cx, cy = x, y
            while True:
                cx += dx
                cy += dy
                if cx < 0 or cx > 7 or cy < 0 or cy > 7:
                    break

                square = board[cy][cx]

                if square == EMPTY_SQUARE:
                    attacks.append((cx, cy))
                    continue

                elif square[0] != color:
                    attacks.append((cx, cy))
                    break

        return attacks

    def get_queen_attacks(self, x, y):
        return self.get_rook_attacks(x, y) + self.get_bishop_attacks(x, y)

    def get_king_attacks(self, x, y, board=[]):

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        attacks = []

        for dx, dy in directions:
            cx, cy = x + dx, y + dy
            if 0 <= cx <= 7 and 0 <= cy <= 7:
                attacks.append((cx, cy))

        return attacks

    def get_pawn_attacks(self, x, y, board=[]):
        attacks = []
        board = self.board if board == [] else board
        color = board[y][x][0]
        direction = -1 if color == "w" else 1

        for dx in [-1, 1]:
            cx, cy = x + dx, y + direction

            if 0 <= cx < 8 and 0 <= cy < 8:
                attacks.append((cx, cy))

        return attacks

    def is_in_check(self, color, board=[]):
        king_position = EMPTY_POSITION
        board = self.board if board == [] else board
        king_piece = color + "k"
        opp_color = "b" if color == "w" else "w"
        opp_attacks = []

        for x in range(8):
            for y in range(8):
                if board[y][x] == king_piece:
                    king_position = (x, y)

                if board[y][x][0] == opp_color:
                    if board[y][x][1] == "r":
                        opp_attacks.append(self.get_rook_attacks(x, y))

                    if board[y][x][1] == "q":
                        opp_attacks.append(self.get_queen_attacks(x, y))

                    if board[y][x][1] == "p":
                        opp_attacks.append(self.get_pawn_attacks(x, y))

                    if board[y][x][1] == "b":
                        opp_attacks.append(self.get_bishop_attacks(x, y))

                    if board[y][x][1] == "k":
                        opp_attacks.append(self.get_king_attacks(x, y))

                    if board[y][x][1] == "n":
                        opp_attacks.append(self.get_knight_attacks(x, y))

        opp_attacks = [pos for sublist in opp_attacks for pos in sublist]

        is_checked = king_position in opp_attacks

        if is_checked:
            self.checked_king = king_position
        else:
            self.checked_king = EMPTY_POSITION

        return is_checked

    def highlight_check(self, pos):

        if pos == EMPTY_POSITION:
            return

        highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight_surface.fill(
            with_alpha(RED, 150),
        )

        self.screen.blit(
            highlight_surface, (pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE)
        )

    def filter_illegal_moves(self):
        if self.selected_piece == EMPTY_SQUARE or self.selected_pos == EMPTY_POSITION:
            return

        legal_moves = []
        original_board = copy.deepcopy(self.board)
        sx, sy = self.selected_pos

        for mx, my in self.valid_moves:
            self.board[my][mx] = self.board[sy][sx]
            self.board[sy][sx] = EMPTY_SQUARE

            if not self.is_in_check(self.turn[0]):
                legal_moves.append((mx, my))

            self.board = copy.deepcopy(original_board)

        self.valid_moves = legal_moves

    def is_checkmate(self, color):
        pass

    def run(self):
        self.load_images()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click()
            self.draw_board()

            if not self.checked_king == EMPTY_POSITION:
                self.highlight_check(self.checked_king)

            if (
                self.selected_pos != (None, None)
                and self.board[self.selected_pos[1]][self.selected_pos[0]]
                != EMPTY_SQUARE
            ):
                x, y = self.selected_pos
                highlight_surface = pygame.Surface(
                    (SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA
                )
                highlight_surface.fill(with_alpha(YELLOW, alpha=50))
                self.screen.blit(highlight_surface, (x * SQUARE_SIZE, y * SQUARE_SIZE))

            self.draw_pieces()

            self.draw_valid_moves()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
