import pygame, os
from animationAssets import action, screen, pixel_font

pygame.init()

#A flag to determine if the feed button has been clicked.
clicked_feed = False
#A flag to determine if the feed button has been clicked.
coin_sound = pygame.mixer.Sound(  ('assets/coin.ogg'))


class FoodMenu:
    # The constructor initializes and loads the necessary graphical components for the food menu.
    def __init__(self, x, y, width, height, panel_path, box_path, food_1_path, food_2_path, food_3_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Load and scale the panel (background) for the food menu.
        self.panel = pygame.transform.scale(pygame.image.load(panel_path), (self.width, self.height))
        self.panel_rect = self.panel.get_rect(center=(self.x, self.y))

        # Load and scale boxes that will hold food items. Three boxes are prepared.
        self.box_1 = pygame.transform.scale(pygame.image.load(box_path), (150, 150))
        self.box_2 = pygame.transform.scale(pygame.image.load(box_path), (150, 150))
        self.box_3 = pygame.transform.scale(pygame.image.load(box_path), (150, 150))

        # Store the normal image state for later reference (to reset on hover out).
        self.normal_image = self.box_1

        # Define positions for the boxes.
        self.box_1_rect = self.box_1.get_rect(center=(self.x - 250, self.y))
        self.box_2_rect = self.box_2.get_rect(center=(self.x, self.y))
        self.box_3_rect = self.box_3.get_rect(center=(self.x + 250, self.y))
        
        # Load and scale food images, positioning them within the corresponding boxes.
        self.food_1 = pygame.transform.scale(pygame.image.load(food_1_path), (100, 100))
        self.food_2 = pygame.transform.scale(pygame.image.load(food_2_path), (75, 100))
        self.food_3 = pygame.transform.scale(pygame.image.load(food_3_path), (100, 100))

        self.food_1_rect = self.food_1.get_rect(center=(self.x - 250, self.y))
        self.food_2_rect = self.food_2.get_rect(center=(self.x, self.y - 10))
        self.food_3_rect = self.food_3.get_rect(center=(self.x + 250, self.y))

        # Load and scale the exit button
        self.exit = pygame.transform.scale(pygame.image.load(  ('assets/cancel.png')), (40, 40))
        self.exit_rect = self.exit.get_rect(center=(715, 90))

    # Method to display the food menu. It checks if the feed button has been clicked.
    def blit_food_menu(self):
        if clicked_feed:
            screen.blit(self.panel, self.panel_rect)

            screen.blit(self.box_1, self.box_1_rect)
            screen.blit(self.box_2, self.box_2_rect)
            screen.blit(self.box_3, self.box_3_rect)

            screen.blit(self.food_1, self.food_1_rect)
            screen.blit(self.food_2, self.food_2_rect)
            screen.blit(self.food_3, self.food_3_rect)

            screen.blit(self.exit, self.exit_rect)
    # Method to handle hover effects over the food boxes.
    def hover(self, x, y):
    # For each box, check if the mouse is hovering over it. If so, change its image and display points.
        if self.box_1_rect.collidepoint((x, y)):
            text = pixel_font.render('Points +3', True, (255, 255, 255))
            screen.blit(text, (20, 120))
            self.box_1 = pygame.transform.scale(pygame.image.load(  ('assets/buttonSquare_blue.png')), (150, 150))
        else:
            self.box_1 = self.normal_image
        if self.box_2_rect.collidepoint((x, y)):
            text = pixel_font.render('Points +6', True, (255, 255, 255))
            screen.blit(text, (270, 120))
            self.box_2 = pygame.transform.scale(pygame.image.load(  ('assets/buttonSquare_blue.png')), (150, 150))
        else:
            self.box_2 = self.normal_image
        if self.box_3_rect.collidepoint((x, y)):
            text = pixel_font.render('Points +10', True, (255, 255, 255))
            screen.blit(text, (480, 120))
            self.box_3 = pygame.transform.scale(pygame.image.load(  ('assets/buttonSquare_blue.png')), (150, 150))
        else:
            self.box_3 = self.normal_image
    
    # Method to handle mouse click events on the food boxes
    def pressed(self, x, y, event):
         # Check each box for a click event and update the game state
        if self.box_1_rect.collidepoint((x, y)) and event.type == pygame.MOUSEBUTTONDOWN:
            if action['satiety'] + 3 <= 100 and action['points'] - 5 >= 0:
                coin_sound.play()
                action['satiety'] += 3
                action['toilet'] -= 3
                action['points'] -= 5
        if self.box_2_rect.collidepoint((x, y)) and event.type == pygame.MOUSEBUTTONDOWN:
            if action['satiety'] + 6 <= 100 and action['points'] - 10 >= 0:
                coin_sound.play()
                action['satiety'] += 6
                action['toilet'] -= 6
                action['points'] -= 10
        if self.box_3_rect.collidepoint((x, y)) and event.type == pygame.MOUSEBUTTONDOWN:
            if action['satiety'] + 10 <= 100 and action['points'] - 15 >= 0:
                coin_sound.play()
                action['satiety'] += 10
                action['toilet'] -= 10
                action['points'] -= 15
