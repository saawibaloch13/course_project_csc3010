import pygame, os
from animationAssets import screen, pixel_font

pygame.init()


class Button:
    # constructor initializes the button with its position, size, image path, and optional text.
    def __init__(self, x, y, width, height, path, text=None):
        # Button's center position on the screen
        self.x = x
        self.y = y
        # Dimensions of the button
        self.width = width
        self.height = height
        # text to display on the button
        self.text = text
        # Load the button's image from the given path and scale it to the specified dimensions.
        self.image = pygame.transform.scale(pygame.image.load(path), (self.width, self.height))
        self.normal_image = self.image
        # Get a rectangle object for the button image, used for positioning and collision detection
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Render the button's text with the given font and color, then position it at the button's center.
        self.btn_text = pixel_font.render(self.text, True, (255, 255, 255))
        self.btn_text_rect = self.btn_text.get_rect()
        self.btn_text_rect.center = self.rect.center

    # Method to draw the button and its text onto the screen
    def blit_btn(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.btn_text, self.btn_text_rect)

    # Method to change the button's image when hovering over it.
    def hover(self, x, y):
        if self.rect.collidepoint((x, y)):
            self.image = pygame.transform.scale(pygame.image.load(('assets/grey_button.png')), (self.width, self.height))
        else:
            self.image = self.normal_image
