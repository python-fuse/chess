import pygame
import typing

from colors import BLACK, RED, WHITE, YELLOW, with_alpha

pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60
SQUARE_SIZE = SCREEN_WIDTH // 8
EMPTY_SQUARE = "--"
EMPTY_POSITION = (None, None)


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

        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp"] * 8,
            [EMPTY_SQUARE] * 8,
            [EMPTY_SQUARE] * 8,
            [EMPTY_SQUARE] * 8,
            [EMPTY_SQUARE] * 8,
            ["wp"] * 8,
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
            print(x, y)
            self.selected_piece = self.board[y][x]
            self.generate_moves()

    def capture(self, start, end):
        if self.board[start[1]][start[0]][0] != self.turn[0]:
            return
        if (self.board[end[1]][end[0]] == EMPTY_SQUARE) or (
            self.board[end[1]][end[0]][0] != self.turn[0]
        ):
            self.board[end[1]][end[0]] = self.board[start[1]][start[0]]
            self.board[start[1]][start[0]] = EMPTY_SQUARE
            self.selected_piece = EMPTY_SQUARE
            self.selected_pos = (None, None)
            self.generate_moves()
            self.is_in_check(self.turn[0])
            self.swap_turns()

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
                            break

                        if square[0] == self.turn[0]:
                            break

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

    # TODO: Make sure only enemy pieces are added to attacks, Do this after eating, cus am so hungry RN

    def get_rook_attacks(self, x, y):
        rook_directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        attacks = []

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

                if self.board[current_y][current_x] != EMPTY_SQUARE:
                    break

                attacks.append((current_x, current_y))

        return attacks

    def get_knight_attacks(self, x, y):
        moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        attacks = []

        for dx, dy in moves:
            cx, cy = x + dx, y + dy
            if 0 <= cx <= 7 and 0 <= cy <= 7:
                attacks.append((cx, cy))

        return attacks

    def get_bishop_attacks(self, x, y):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        attacks = []

        for dx, dy in directions:
            cx, cy = x, y
            while True:
                cx += dx
                cy += dy
                if cx < 0 or cx > 7 or cy < 0 or cy > 7:
                    break
                attacks.append((cx, cy))
                if self.board[cy][cx] != EMPTY_SQUARE:
                    break

        return attacks

    def get_queen_attacks(self, x, y):
        return self.get_rook_attacks(x, y) + self.get_bishop_attacks(x, y)

    def get_king_attacks(self, x, y):
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

    def get_pawn_attacks(self, x, y, color):
        attacks = []
        direction = -1 if color == "white" else 1
        for dx in [-1, 1]:
            cx, cy = x + dx, y + direction
            if 0 <= cx <= 7 and 0 <= cy <= 7:
                attacks.append((cx, cy))
        return attacks

    def is_in_check(self, color):
        king_position = EMPTY_POSITION
        king_piece = color + "k"

        for x in range(8):
            for y in range(8):
                if self.board[y][x] == king_piece:
                    king_position = (x, y)
                    print(f"{king_piece} found at {king_position}")

                if self.board[y][x].startswith(color) and self.board[y][x][1] == "r":
                    rook_atts = self.get_rook_attacks(x, y)
                    print(rook_atts)

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
            self.draw_pieces()

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
            self.draw_valid_moves()

            # if (
            #     self.selected_pos != (None, None)
            #     and self.board[self.selected_pos[1]][self.selected_pos[0]]
            #     == EMPTY_SQUARE
            # ):

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
