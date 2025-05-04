import pygame

from colors import BLACK, WHITE, YELLOW, with_alpha

pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60
SQUARE_SIZE = SCREEN_WIDTH // 8
EMPTY_SQUARE = "--"


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("uChess")
        self.clock = pygame.time.Clock()
        self.selected_pos = (None, None)
        self.selected_piece = None
        self.turn = "white"
        self.valid_moves = []

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

        self.selected_pos = (x, y)
        print(x, y)
        self.selected_piece = self.board[y][x]
        self.generate_moves()

    def validate_move(self, start, end):
        pass

    def generate_moves(self):
        x, y = self.selected_pos
        self.valid_moves.clear()

        if self.selected_piece != EMPTY_SQUARE:
            if self.selected_piece[1].lower() == "p":
                dir = -1 if self.turn == "white" else 1
                if y == 6 or y == 1:
                    if self.board[y + (dir)][x] == EMPTY_SQUARE:
                        self.valid_moves.append((x, y + (dir)))
                        if self.board[y + (dir * 2)][x] == EMPTY_SQUARE:
                            self.valid_moves.append((x, y + (dir * 2)))

    def draw_valid_moves(self):
        for move in self.valid_moves:
            move_highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            move_highlight.fill(with_alpha(WHITE, 0))
            pygame.draw.circle(
                move_highlight,
                with_alpha(BLACK, 100),
                (SQUARE_SIZE // 2, SQUARE_SIZE // 2),
                10,
            )
            self.screen.blit(
                move_highlight, (move[0] * SQUARE_SIZE, move[1] * SQUARE_SIZE)
            )

    def is_in_check(self, color):
        pass

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

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
