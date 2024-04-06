import pygame, os
from animationAssets import screen, pixel_font

pygame.init()
clicked_statistics = False


class Statistics:
    # Initialize the Statistics object with position, size, path to the background image,
    # and optional text fields for displaying statistics.
    def __init__(self, x, y, width, height, path, text_lg=None, text_name=None, text_days=None):
        self.x = x
        self.y = y
        # Width of the statistics area
        self.width = width
        # Height of the statistics area
        self.height = height
        # Text for displaying a large score or statistic
        self.text_lg = text_lg
        self.text_name = text_name
        self.text_days = text_days
        # Load and scale the background image to the specified width and height
        self.image = pygame.transform.scale(pygame.image.load(path), (self.width, self.height))
        self.image_rect = self.image.get_rect(center=(self.x, self.y))
        # Load and scale the exit button image
        self.exit = pygame.transform.scale(pygame.image.load(('assets/cancel.png')), (40, 40))
        self.exit_rect = self.exit.get_rect(center=(715, 90))

        # Load and scale the logo image
        self.logo_image = pygame.transform.scale(pygame.image.load(('assets/logo.png')), (60, 60))

        # Render the score text with the specified font and color
        self.score_text = pixel_font.render(self.text_lg, True, (255, 255, 255))
        self.score_text_rect = self.score_text.get_rect(center=(430, 210))

        # Render the name text with the specified font and color
        self.name_text = pixel_font.render(self.text_name, True, (255, 255, 255))
        self.name_text_rect = self.name_text.get_rect(center=(400, 250))

        # Render the days text with the specified font and color
        self.days_text = pixel_font.render(self.text_days, True, (255, 255, 255))
        self.days_text_rect = self.days_text.get_rect(center=(400, 300))

    #Method for statistics on the screen if the clicked_statistics flag is True
    def blit_statistics(self):
        if clicked_statistics:
            screen.blit(self.image, self.image_rect)
            screen.blit(self.score_text, self.score_text_rect)
            screen.blit(self.name_text, self.name_text_rect)
            screen.blit(self.days_text, self.days_text_rect)
            screen.blit(self.exit, self.exit_rect)
            screen.blit(self.logo_image, (330, 170))
