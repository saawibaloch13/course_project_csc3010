import pygame, os

pygame.init()

# Set the dimensions for the pet animations.
width = 150
height = 150

# Initialize a dictionary to keep track of the pet's stats such as satiety, toilet needs, happiness, health, and points.
action = {'satiety': 100, 'toilet': 100, 'happy': 100, 'health': 100, 'points': 50}
# Initialize a dictionary to keep track of the pet's stats such as satiety, toilet needs, happiness, health, and points.
screen = pygame.display.set_mode((800, 500))
# Load and set the fonts from the assets folder for displaying text in the game.
# 'pixel_font' is used for regular text, and 'pixel_font2' is slightly larger for headings or important text.
pixel_font = pygame.font.Font(('assets/FatPix-SVG.ttf'), 23)
pixel_font2= pygame.font.Font(('assets/FatPix-SVG.ttf'), 30)
# Load and scale the pet's animation frames to fit the specified width and height
pypetAction = [pygame.transform.scale(pygame.image.load(('assets/petanimation/pet-0.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(('assets/petanimation/pet-1.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(('assets/petanimation/pet-2.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(('assets/petanimation/pet-3.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(('assets/petanimation/pet-4.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(('assets/petanimation/pet-5.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(('assets/petanimation/pet-6.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(('assets/petanimation/pet-7.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(('assets/petanimation/pet-8.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(('assets/petanimation/pet-9.png')), (width, height))]
