# colors.py

# Basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Chess-related colors
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT = (255, 255, 0)  # solid yellow
HIGHLIGHT_TRANSPARENT = (
    255,
    255,
    0,
    100,
)  # yellow with alpha (if used on SRCALPHA surface)

# Custom shades
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)
NAVY = (0, 0, 128)


# Function to generate color with alpha (optional helper)
def with_alpha(color, alpha):
    return (color[0], color[1], color[2], alpha)
