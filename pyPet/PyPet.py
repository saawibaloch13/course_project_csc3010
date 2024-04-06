import random
import os
import time
import pygame
import allFood
import mainPanel
import playGame
import viewStats
from allButtons import Button
from animationAssets import action, pypetAction, pixel_font, pixel_font2,screen


pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)

# Define time constants and create another timer for day-night cycle
day = 90000
daysCount = 0
daysEvent = pygame.USEREVENT + 1
pygame.time.set_timer(daysEvent, day)

# Set screen dimensions and game parameters
screen_width = 800
screen_height = 500
FPS = 45 # Frames per second
timeout = 15 
animCount = 0
text_timer = 0
night_timer = 0

# Flags for game state management
endMenu = False
endGame = False
isSleep = False
cantClear = False
cantHelp = False

# Set up the Pygame window and clock
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PyPet')
pygame.display.set_icon(pygame.image.load(('assets/logo.ico')))
clock = pygame.time.Clock()
start_time = None
game_time = None

# Load and configure game assets (images, cursor, backgrounds)
cursor = pygame.image.load(('assets/cursor.png'))
pygame.mouse.set_visible(False)
# Load menu and game background images
background_menu = [pygame.transform.scale(pygame.image.load(('assets/gifMenu-0.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(('assets/gifMenu-1.png')), (screen_width, screen_height))]
background = pygame.transform.scale(pygame.image.load(('assets/background.jpg')), (screen_width, screen_height))
gameover_img = pygame.transform.scale(pygame.image.load(('assets/gameover_1.png')), (screen_width, screen_height))
sleep_image = pygame.transform.scale(pygame.image.load(('assets//sleep.png')), (50, 50))
day_image = pygame.transform.scale(pygame.image.load(('assets/day.png')), (50, 50))
night_image = pygame.transform.scale(pygame.image.load(('assets/night.png')), (50, 50))
gameover_text = pixel_font.render('If you want play one more time, you have to restart game', True, (75, 255, 255))

# Animation function for the pet
def PyPetAnimation(x, y):
    global animCount
    if not isSleep:
        if animCount + 1 >= len(pypetAction) * 6:
            animCount = 0
            screen.blit(pypetAction[0], (x, y))
        else:
            screen.blit(pypetAction[animCount // 6], (x, y))
            animCount += 1

        screen.blit(day_image, (735, 70))
    else:
        screen.blit(pypetAction[0], (x, y))

# Function to decrement pet stats periodically
def scoreTick():
    global start_time, timeout
    t_time = time.time() - start_time
    if t_time > timeout:
        action['satiety'] -= 3
        action['toilet'] -= 2
        action['happy'] -= 3
        action['health'] -= random.randint(0, 5)
        start_time = time.time()

# Functions to handle pet care actions (clearAfter, medicine)
def clearAfter():
    global cantClear
    if action['toilet'] + 16 <= 100:
        action['toilet'] += 16
        toilet_sound = pygame.mixer.Sound(('assets/toilet.ogg'))
        toilet_sound.play()
    else:
        cantClear = True

# Functio for health
def medicine():
    global cantHelp
    if action['points'] - 3 >= 0:
        if action['health'] + 10 <= 100:
            action['health'] += 10
            action['points'] -= 3
            medicine_sound = pygame.mixer.Sound(('assets/medicine.ogg'))
            medicine_sound.play()
        else:
            cantHelp = True

# Function to check and handle game over state
def gameOver():
    if action['satiety'] <= 0 or action['toilet'] <= 0 or action['happy'] <= 0 or action['health'] <= 0:
        pygame.mixer.music.stop()
        screen.blit(gameover_img, (0, 0))
        screen.blit(gameover_text, (35, 450))


# Function to spawn cupcakes during the 'Play' game state
def spawn_cupcakes(group):
    return playGame.Cupcake(random.randint(40, 760), random.randint(3, 5), ('assets/cupcake.png'), group)

cupcakes = pygame.sprite.Group()

help_menu = mainPanel.Panel(400, 250, 750, 450, ('assets/window.png'), ' The gaol of the game is to keep your pet alive.',
                             'If any one ofthe stats level is equal to zero,','your pet will die and you will lose','Good Luck!!')

# Buttons for main menu, gameplay actions, and pet stats
logo_label = Button(200, 230, 200, 200, ('assets//logo.png'))
start_btn = Button(570, 150, 200, 50, ('assets/pink_button.png'), 'Start')
rule_btn = Button(570, 250, 200, 50, ('assets/pink_button.png'), 'Help')
exit_btn = Button(570, 350, 200, 50, ('assets/pink_button.png'), 'Exit')


info_satiety = Button(20, 30, 25, 50, ('assets/lightning.png'))
info_toilet = Button(150, 30, 50, 50, ('assets/toilet.png'))
info_happy = Button(270, 30, 50, 50, ('assets/smile.png'))
info_health = Button(400, 30, 60, 60, ('assets/health.png'))

btn_statistic = Button(715, 40, 150, 50, ('assets/pink_button.png'), 'Statistic')

btn_satiety = Button(85, 467, 150, 50, ('assets/pink_button.png'), 'Feed')
btn_toilet = Button(285, 467, 150, 50, ('assets/pink_button.png'), 'Toilet')
btn_play = Button(515, 467, 150, 50, ('assets/pink_button.png'), 'Play')
btn_health = Button(715, 467, 150, 50, ('assets/pink_button.png'), 'Medicine')

food = allFood.FoodMenu(400, 250, 750, 450, ('assets/window.png'),
                          ('assets/buttonSquare_beige_pressed.png'),
                          ('assets/food_1.png'), ('assets/food_2.png'), ('assets/food_3.png'))

play = playGame.Play()
basket = playGame.Basket()


button_sound = pygame.mixer.Sound(('assets/button.ogg'))
button_sound.set_volume(0.05)

# Main game loop function
def game():
    # global variables that control game states and track game progress
    global endGame, isSleep, daysCount, night_timer, text_timer, cantClear, cantHelp, game_time, start_time
    start_time = time.time()
    # Load and play background music for the game environment.
    pygame.mixer.music.load(('assets/backgroundMusic.ogg'))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)

    # Main game loop that runs until 'endGame' is flagged True
    while not endGame:
        screen.blit(background, (0, 0))
        info_satiety.blit_btn()
        satiety_text = pixel_font.render(str(action['satiety']), False, (255, 20, 147))
        screen.blit(satiety_text, (40, 15))
        info_toilet.blit_btn()
        toilet_text = pixel_font.render(str(action['toilet']), False, (255, 20, 147))
        screen.blit(toilet_text, (180, 15))
        info_happy.blit_btn()
        smile_text = pixel_font.render(str(action['happy']), False, (255, 20, 147))
        screen.blit(smile_text, (300, 15))
        health_text = pixel_font.render(str(action['health']), False, (255, 20, 147))
        screen.blit(health_text, (440, 15))
        info_health.blit_btn()

        # Animation for the pet, placed at specific coordinates
        PyPetAnimation(330, 250)

        # Display buttons for various game actions statistics, feeding, playing, and toilet 
        btn_statistic.blit_btn()
        statistics = viewStats.Statistics(400, 250, 750, 450, ('assets/window.png'),
                                                str(action['points']) + ' P', 'Name: PyPet', f'Days: {daysCount}')
        btn_satiety.blit_btn()
        btn_toilet.blit_btn()
        btn_play.blit_btn()
        btn_health.blit_btn()

        pos_x, pos_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                endGame = True
                pygame.quit()
            if event.type == daysEvent:
                isSleep = True
            # Display day or night image based on whether the pet is asleep.
            if not isSleep:
                if btn_statistic.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    viewStats.clicked_statistics = True
                    button_sound.play()
                if btn_satiety.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    allFood.clicked_feed = True
                    button_sound.play()
                if action['points'] >= 0:
                    food.pressed(pos_x, pos_y, event)
                if btn_toilet.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    clearAfter()
                if btn_play.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    game_time = time.time()
                    playGame.clicked_play = True
                    button_sound.play()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(('assets/game.ogg'))
                    pygame.mixer.music.set_volume(0.7)
                    pygame.mixer.music.play()
                if event.type == pygame.USEREVENT:
                    if playGame.clicked_play:
                        spawn_cupcakes(cupcakes)
                if btn_health.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    medicine()
            if statistics.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                viewStats.clicked_statistics = False
                button_sound.play()
            if food.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                allFood.clicked_feed = False
                button_sound.play()
            if play.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                playGame.clicked_play = False
                playGame.scoreCount = 0
                playGame.timeCount = 60
                playGame.seconds = 1
                button_sound.play()
                pygame.mixer.music.unload()
                pygame.mixer.music.load(('assets/backgroundMusic.ogg'))
                pygame.mixer.music.play(loops=-1)

        btn_statistic.hover(pos_x, pos_y)
        btn_satiety.hover(pos_x, pos_y)
        btn_toilet.hover(pos_x, pos_y)
        btn_play.hover(pos_x, pos_y)
        btn_health.hover(pos_x, pos_y)

        if isSleep:
            screen.blit(night_image, (735, 70))
            screen.blit(sleep_image, (430, 350))
            if night_timer > 700:
                isSleep = False
                night_timer = 0
                daysCount += 1
            night_timer += 1

        # Display messages when certain actions can't be performed
        if cantClear:
            text = pixel_font.render('I am good for now!', True, (255, 255, 255))
            screen.blit(text, (230, 400))
            if text_timer > 75:
                cantClear = False
                text_timer = 0
            text_timer += 1

        if cantHelp:
            text = pixel_font.render('I am good for now!', True, (255, 255, 255))
            screen.blit(text, (660, 400))
            if text_timer > 75:
                cantHelp = False
                text_timer = 0
            text_timer += 1

        if viewStats.clicked_statistics:
            statistics.blit_statistics()
        if allFood.clicked_feed:
            food.blit_food_menu()
            food.hover(pos_x, pos_y)
        if playGame.clicked_play:
            play.blit_play()
            basket.blit_basket()
            play.check_time(game_time)
            cupcakes.draw(screen)
            cupcakes.update(screen_height)
            if pygame.sprite.spritecollide(basket, cupcakes, True):
                playGame.scoreCount += 1

        keys = pygame.key.get_pressed()
        play.control(keys)
        basket.control(keys)

        gameOver()

        if pygame.mouse.get_focused():
            screen.blit(cursor, (pos_x, pos_y))

        scoreTick()
        clock.tick(FPS)
        pygame.display.update()

# Main menu loop function
def menu():
    global endMenu, animCount, start_time
    pygame.mixer.music.load(('assets/menu.ogg'))
    pygame.mixer.music.play(loops=-1)
    while not endMenu:
        if animCount + 1 >= len(background_menu) * 9:
            animCount = 0
            screen.blit(background_menu[0], (0, 0))
        else:
            screen.blit(background_menu[animCount // 9], (0, 0))
            animCount += 1

        logo_label.blit_btn()
        start_btn.blit_btn()
        rule_btn.blit_btn()
        exit_btn.blit_btn()

        pos_x, pos_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                endMenu = True
                pygame.quit()
            if start_btn.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                endMenu = True
                game()
            if rule_btn.rect.collidepoint(pos_x, pos_y) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                mainPanel.clicked_help = True
            if help_menu.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                mainPanel.clicked_help = False
            if exit_btn.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                pygame.mouse.set_visible(True)
                endMenu = True
                pygame.quit()

        welcome_text = pixel_font2.render("Welcome to PyPet!", True, (139, 0, 139)) 
        screen.blit(welcome_text, (70, 320)) 


        start_btn.hover(pos_x, pos_y)
        rule_btn.hover(pos_x, pos_y)
        exit_btn.hover(pos_x, pos_y)

        if mainPanel.clicked_help:
            help_menu.blit_panel()

        if pygame.mouse.get_focused():
            screen.blit(cursor, (pos_x, pos_y))

        clock.tick(FPS)
        pygame.display.update()

# Entry point of the script to start the game menu  
if __name__ == '__main__':       
    menu()
