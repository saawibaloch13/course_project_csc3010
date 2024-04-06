import pygame, os
from animationAssets import screen, pixel_font

pygame.init()
# A flag to determine if the help panel should be shown
clicked_help = False


class Panel:

    # Constructor initializes the panel with its position, size, background image, and up to four lines of text.
    def __init__(self, x, y, width, height, path, text_1=None, text_2=None, text_3=None,text_4=None):
        # Position and dimensions of the panel
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Texts to be displayed on the panel. Optional and can be None
        self.text_1 = text_1
        self.text_2 = text_2
        self.text_3 = text_3
        self.text_4 = text_4
        # Load the background image for the panel, scaling it to the desired size
        self.image = pygame.transform.scale(pygame.image.load(path), (self.width, self.height))
        # Get a rectangle for positioning the background image
        self.image_rect = self.image.get_rect(center=(self.x, self.y))
        self.exit = pygame.transform.scale(pygame.image.load(('assets/cancel.png')), (40, 40))
        self.exit_rect = self.exit.get_rect(center=(715, 90))

        # Render the texts using the specified font and color, centering them at specific positions on the panel
        self.first_text = pixel_font.render(self.text_1, True, (255, 255, 255))
        self.first_text_rect = self.first_text.get_rect(center=(400, 200))

        self.second_text = pixel_font.render(self.text_2, True, (255, 255, 255))
        self.second_text_rect = self.second_text.get_rect(center=(400, 250))

        self.third_text = pixel_font.render(self.text_3, True, (255, 255, 255))
        self.third_text_rect = self.third_text.get_rect(center=(400, 300))

        self.fourth_text = pixel_font.render(self.text_4, True, (255, 255, 255))
        self.fourth_text_rect = self.fourth_text.get_rect(center=(400, 400))

    # Method to display the panel and its contents on the screen when the help button is clicked
    def blit_panel(self):
        if clicked_help:
            screen.blit(self.image, self.image_rect)
            screen.blit(self.first_text, self.first_text_rect)
            screen.blit(self.second_text, self.second_text_rect)
            screen.blit(self.third_text, self.third_text_rect)
            screen.blit(self.fourth_text, self.fourth_text_rect)
            screen.blit(self.exit, self.exit_rect)
