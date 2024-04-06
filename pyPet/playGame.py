import pygame, os
import time
from animationAssets import action, pypetAction, pixel_font, screen

pygame.init()

# Initialize global variables for animation count, time count, score count, and time tracking
animCount = 0
timeCount = 30
scoreCount = 0
seconds = 1
# A flag to indicate if the play button has been clicked
clicked_play = False


class Play:
    # Constructor for the Play class initializes the play area and loads resources
    def __init__(self):
        self.x = 325
        self.y = 300
        self.width = 150
        self.height = 150
        self.background_anim = [pygame.transform.scale(pygame.image.load(('assets/background-0.png')), (800, 500)),
                                pygame.transform.scale(pygame.image.load(('assets/background-1.png')), (800, 500)),
                                pygame.transform.scale(pygame.image.load(('assets/background-2.png')), (800, 500)),
                                pygame.transform.scale(pygame.image.load(('assets/background-3.png')), (800, 500))]
       # exit button image
        self.exit = pygame.transform.scale(pygame.image.load(  ('assets/cancel.png')), (40, 40))
        self.exit_rect = self.exit.get_rect(center=(40, 40))

    # Method to draw the play area and its elements on the screen
    def blit_play(self):
        global animCount
        if clicked_play:
            if animCount + 1 >= len(self.background_anim) * 7:
                animCount = 0
                screen.blit(self.background_anim[0], (0, 0))
                screen.blit(pypetAction[0], (self.x, self.y))
            else:
                screen.blit(self.background_anim[animCount // 7], (0, 0))
                screen.blit(pypetAction[animCount // 7], (self.x, self.y))
                animCount += 1

        # Render and draw the time left and score on the screen
        time_left = pixel_font.render(f'Time Left: {timeCount}', True, (255, 255, 255))
        score = pixel_font.render(f'Score: {scoreCount}', True, (255, 255, 255))
        screen.blit(score, (600, 20))
        screen.blit(time_left, (600, 60))
        screen.blit(self.exit, self.exit_rect)

    # Method to manage the game timer and update the game state accordingly
    def check_time(self, game_time):
        global clicked_play, timeCount, scoreCount, seconds
        t_time = time.time() - game_time
        if seconds < t_time:
            timeCount -= 1
            seconds += 1
        if timeCount == 0:
            action['points'] += scoreCount // 2
            if action['happy'] + 15 > 100:
                score = 100 - action['happy']
                action['happy'] += score
            else:
                action['happy'] += 15
            action['satiety'] -= 2
            clicked_play = False
            timeCount = 60
            seconds = 1
            scoreCount = 0
            pygame.mixer.music.unload()
            pygame.mixer.music.load(  ('assets/backgroundMusic.ogg'))
            pygame.mixer.music.play(loops=-1)
       
    # Method to control player movement based on keyboard input
    def control(self, keys):
        if keys[pygame.K_LEFT] and self.x > 1:
            self.x -= 7
        if keys[pygame.K_RIGHT] and self.x < 800 - self.width:
            self.x += 7


class Basket(pygame.sprite.Sprite):
     # Constructor for the Basket class, initializes the basket sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.basket = pygame.transform.scale(pygame.image.load(('assets/basket.png')), (150 // 2, 150 // 3))
        self.rect = self.basket.get_rect(center=(400, 430))
    
    # Method to draw the basket on the screen
    def blit_basket(self):
        screen.blit(self.basket, self.rect)
   
    # Method to update basket position based on keyboard input, ensuring it stays within screen bounds
    def control(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 35:
            self.rect.x -= 7
        if keys[pygame.K_RIGHT] and self.rect.x < 690:
            self.rect.x += 7


class Cupcake(pygame.sprite.Sprite):
        # Constructor for the (cupcake sprite) class, initializes the sprite and adds it to a group
    def __init__(self, x, speed, filename, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(filename), (30, 30))
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.add(group)

    # Update method to move the cupcake downwards, and remove it when it goes off-screen
    def update(self, height):
        if self.rect.y < height - 20:
            self.rect.y += self.speed
        else:
            self.kill()
