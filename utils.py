import pygame

from colors import BLACK

pygame.init()
font = pygame.font.SysFont("comic sans", 20)


class Button:
    def __init__(
        self,
        bg_color,
        surface,
        btn_pos=(0, 0),
        text_color=BLACK,
        btn_size=(100, 50),
        text="",
        on_pressed=lambda: print("Clicked!"),
    ):
        self.btn_pos = btn_pos
        self.surface = surface
        self.on_pressed = on_pressed
        self.btn_size = btn_size

        self.button = pygame.Surface(btn_size)
        self.button.fill(bg_color)

        self.text = font.render(text, True, text_color)
        self.text_rect = self.text.get_rect(center=(btn_size[0] // 2, btn_size[1] // 2))

        self.button.blit(self.text, self.text_rect)
        self.rect = pygame.Rect(btn_pos, btn_size)

    def render(self):
        self.surface.blit(self.button, self.btn_pos)

    def is_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.on_pressed()
