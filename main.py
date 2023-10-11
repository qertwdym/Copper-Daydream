import pygame
import pygame.font
import sys
import random
import math
import os
import time
import json 
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    """ Get absolute path to resource """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

player_name = ""
data_file_path = resource_path('game_data.json')
pygame.init()

# variables_used
game_in_progress = False
height = 675
width = 500
icon = pygame.image.load(resource_path("001-icon.png"))
background_image_1 = pygame.image.load(resource_path('bg.png'))
background_image_2 = pygame.image.load(resource_path('bg.png'))
cat_image = pygame.image.load(resource_path('001-main.png'))
y1 = 0
y2 = -675

track_speed = 1

cat_x = width / 2 - 25
cat_y = height - 100
cat_xc = 0
fishbone_y = height - 100
fishbone_x = cat_x + 20
fishbone_image = pygame.image.load(resource_path('001-fishbone.png'))
fishbone_yc = 0
fishbone_xc = 0

# ##### enemy #######
enemy_1x = random.randint(40, 410)
enemy_1y = -100
enemy_1xc = 0
enemy_1yc = 3
enemy_1_image = pygame.image.load(resource_path('002-enemy.png'))

enemy_2x = random.randint(40, 410)
enemy_2y = -20000
enemy_2xc = 0
enemy_2yc = 10
enemy_2_image = pygame.image.load(resource_path('002-bird.png'))

mine_x = random.randint(150, 300)
mine_y = -200
mine_xc = 0
mine_yc = track_speed
mine_image = pygame.image.load(resource_path('banana.png'))

mine_2x = random.randint(150, 300)
mine_2y = -400
mine_2xc = 0
mine_2yc = track_speed
mine_2image = pygame.image.load(resource_path('banana.png'))

boss_x = random.randint(120, 300)
boss_y = -3000
boss_xc = 4
boss_yc = 2
boss_image = pygame.image.load(resource_path('boss.png'))
boss_life = 30

# score
score = 0
highscores = []

# life
life = 100
life_image = pygame.image.load(resource_path('001-heart.png'))
life_x = random.randint(40, 410)
life_y = -1000
life_xc = 0
life_yc = track_speed

# Main
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Copper's Daydream")
pygame.display.set_icon(icon)

explosions = [pygame.image.load(resource_path('exp1.png')), pygame.image.load(resource_path('exp1.png')), pygame.image.load(resource_path('exp1.png')),
              pygame.image.load(resource_path('exp1.png')), pygame.image.load(resource_path('exp1.png'))]
clock = pygame.time.Clock()

run = True

# defining the functions.
def load_highscores():
    try:
        with open(data_file_path, 'r') as file:
            data = json.load(file)
            return data.get('highscores', [])
    except FileNotFoundError:
        return []

def save_highscores(current_score, current_player_name):
    highscore_data = []
    for (player_name, score) in highscores:
        highscore_data.append([player_name, score])
    highscore_data.append([current_player_name, current_score])
    data = {'highscores': highscore_data}
    print('check save high score data')
    print(data)
    with open(data_file_path, 'w') as file:
        json.dump(data, file)
        
def get_player_name():
    root = tk.Tk()
    root.title("Enter Your Username")
    root.geometry("400x200")

    player_name_var = tk.StringVar()  # Store the player's name

    def submit_username():
        player_name = entry.get()
        player_name_var.set(player_name)  # Set the StringVar with the player's name
        root.destroy()

    label = tk.Label(root, text="Enter your username:")
    label.pack(pady=10)

    entry = tk.Entry(root, textvariable=player_name_var)  # Use the StringVar
    entry.pack(pady=5)

    submit_button = tk.Button(root, text="Submit", command=submit_username)
    submit_button.pack(pady=10)

    root.mainloop()

    return player_name_var.get() 

    
def show_cat():
    screen.blit(cat_image, (cat_x, cat_y))

def show_fishbone():
    global cat_y
    global cat_x
    if fishbone_y < cat_y:
        screen.blit(fishbone_image, (fishbone_x, fishbone_y))

def ready_fishbone():
    global fishbone_yc
    global fishbone_y
    global fishbone_x
    global cat_x
    global cat_y
    fishbone_yc = 0
    fishbone_y = cat_y
    fishbone_x = cat_x + 20

def fire_fishbone():
    global fishbone_yc
    global fishbone_y
    global fishbone_x
    global cat_x
    global cat_y
    fishbone_x = cat_x + 20
    fishbone_yc = -20

def show_enemy():
    screen.blit(enemy_1_image, (enemy_1x, enemy_1y))
    screen.blit(enemy_2_image, (enemy_2x, enemy_2y))
    screen.blit(boss_image, (boss_x, boss_y))

def show_mine():
    screen.blit(mine_image, (mine_x, mine_y))
    screen.blit(mine_image, (mine_2x, mine_2y))

def is_collision(a, b, x, y,d):
    dist_btw_fishbone_enemy = math.sqrt(math.pow(a - x, 2) + math.pow(b - y, 2))
    if dist_btw_fishbone_enemy <= d:
        return True

def explosion_animation(x, y):
    for explosion in explosions:
        screen.blit(explosion, (x, y))
        pygame.display.update()
        if explosion == explosions[4]:
            break

def score_display(x, y):
    font = pygame.font.Font(resource_path('FreeSansBold.ttf'), 32)

    score_display = font.render('SCORE:' + str(score), True, (230, 230, 230 ))
    screen.blit(score_display, (x, y))

def highscore_display(x, y, highscores):
    print('in function high display')
    print(highscores)
    if highscores:
        max_score = sorted(highscores, key=lambda x: x[1])
        print('max score after sort')
        max_score = max_score.pop()[1]
    else:
        max_score = 0
    
    font = pygame.font.Font(resource_path('FreeSansBold.ttf'), 25)
    highscore_display = font.render(
        'HIGH-SCORE:' + str(max_score), True, (230, 230, 230))
    screen.blit(highscore_display, (x, y))

def life_display(x, y):
    screen.blit(life_image, (life_x, life_y))
    font = pygame.font.Font(resource_path('FreeSansBold.ttf'), 25)

    life_display = font.render('LIFE:' + str(life), True, (250, 230, 230))
    screen.blit(life_display, (x, y))

def game_over(x, y, x1, y1):
    screen.blit(background_image_1, (0, 0))
    font = pygame.font.Font(resource_path('FreeSansBold.ttf'), 60)
    game_over_display = font.render('GAME  OVER', True, (255, 0, 0))
    screen.blit(game_over_display, (x, y))

    font_replay = pygame.font.Font(resource_path('FreeSansBold.ttf'), 25)
    replay = font_replay.render('press enter to play again.', True, (230, 230, 230))
    screen.blit(replay, (x1, y1))
    score_display(60, 320)
    highscore_display(60, 360, highscores)
    
def show_player_name(player_name, cat_x, cat_y):
    font = pygame.font.Font(resource_path('FreeSansBold.ttf'), 20)
    player_name_text = font.render("" + player_name, True, (255, 255, 255))
    text_rect = player_name_text.get_rect(center=(cat_x + 25, cat_y - 20))
    screen.blit(player_name_text, text_rect)

#GUI for start game
def start_menu():
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    highscore_display(width // 2 - 100, height // 2 + 100, highscores)

        # Display the start menu background
        screen.blit(background_image_1, (0, 0))

        # Text at start menu
        font = pygame.font.Font(resource_path('FreeSansBold.ttf'), 40)
        start_text = font.render('Press ENTER to Play', True, (255, 255, 255))
        esc_text = font.render('ESC to Exit', True, (255, 255, 255))

        # Display the start menu text in the center of the screen
        text_rect = start_text.get_rect(center=(width // 2, height // 2))
        screen.blit(start_text, text_rect)
        esc_rect = esc_text.get_rect(center=(width // 2, (height // 2) + 50))
        screen.blit(esc_text, esc_rect)

        pygame.display.update()

def main():
    start_menu()
    player_name = get_player_name()
    global score
    global life
    global fishbone_yc
    global fishbone_y
    global fishbone_x
    global cat_x
    global cat_y
    global cat_xc
    global y1
    global y2
    global track_speed
    global enemy_1x
    global enemy_1y
    global enemy_2x
    global enemy_2y
    global enemy_2yc
    global enemy_2xc
    global enemy_1xc
    global enemy_1yc
    global boss_x
    global boss_y
    global boss_yc
    global boss_xc
    global boss_life
    global mine_y
    global mine_x
    global mine_2x
    global mine_yc
    global mine_2xc
    global mine_2y
    global life_x
    global life_y
    global life_yc
    global life_xc
    global run

    # resetting variables to initial value
    run = True
    y1 = 0
    y2 = -675
    track_speed = 1
    cat_x = width / 2 - 25
    cat_y = height - 100
    cat_xc = 0
    fishbone_y = height - 100
    fishbone_x = cat_x + 20
    fishbone_yc = 0

    # ##### enemy #######
    enemy_1x = random.randint(40, 410)
    enemy_1y = -100
    enemy_1xc = 0
    enemy_1yc = 3
    enemy_2x = random.randint(40, 410)
    enemy_2y = -20000
    enemy_2xc = 0
    enemy_2yc = 10
    mine_x = random.randint(150, 300)
    mine_y = -200
    mine_yc = track_speed
    mine_2x = random.randint(150, 300)
    mine_2y = -400
    mine_2xc = 0
    boss_x = random.randint(120, 300)
    boss_y = -5000
    boss_xc = 4
    boss_yc = 2
    boss_life = 5

    # score
    score = 0
    highscores = load_highscores()
    life = 100
    life_x = random.randint(120, 300)
    life_y = -1000
    life_xc = 4
    life_yc = 6

# If highscores is empty, set it to a default value (e.g., 0)
    if not highscores:
        highscores = [0]
    
    # making the infinite loop.
    while run:
        pygame.time.delay(20)
        screen.blit(background_image_1, (0, y1))
        screen.blit(background_image_2, (0, y2))
        for event in pygame.event.get():
            # exit event
            if event.type == pygame.QUIT:
                sys.exit()

            # moving cat and firing the fishbone
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    cat_xc = 10

                if event.key == pygame.K_LEFT:
                    cat_xc = -10
                if event.key == pygame.K_UP:
                    track_speed = 4
                    enemy_1yc = 6
                    enemy_2yc = 20
                    boss_yc = 2 * 2
                    life_yc = 6
                if event.key == pygame.K_SPACE:
                    if fishbone_y == cat_y:
                        fire_fishbone()
                if event.key == pygame.K_RETURN:
                    run = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    cat_xc = 0
                if event.key == pygame.K_UP:
                    track_speed = 1
                    enemy_1yc = 3
                    enemy_2yc = 10
                    boss_yc = 2
                    life_yc = 3
                    
            # #### collision ######
            collision1= is_collision(enemy_1x+40, enemy_1y+40, fishbone_x, fishbone_y,100) #enemy
            if collision1 == True:
                explosion_animation(enemy_1x, enemy_1y)
                enemy_1x = random.randint(40, 410)
                enemy_1y = -200
                ready_fishbone()
                score += 1
            collision2 = is_collision(enemy_2x+40, enemy_2y+40, fishbone_x,fishbone_y,100) #bird
            if collision2 == True:
                explosion_animation(enemy_2x, enemy_2y)
                enemy_2x = random.randint(40, 410)
                enemy_2y = -6000
                ready_fishbone()
                score += 10
            collision3 = is_collision(boss_x+80, boss_y+60, fishbone_x, fishbone_y,100) #boss
            if collision3 == True:
                explosion_animation(boss_x+30, boss_y)
                ready_fishbone()
                boss_life -= 1
                if boss_life <= 0:
                    boss_x = random.randint(40, 410)
                    boss_y = -3000
                    explosion_animation(boss_x, boss_y)
                    boss_life = 30
                    score += 50
            collision4 = is_collision(mine_x+25, mine_y+25, x=cat_x, y=cat_y,d=50) #mine
            if collision4 == True:
                explosion_animation(mine_x, mine_y)
                ready_fishbone()
                mine_x = random.randint(40, 410)
                mine_y = random.randint(300, 450)
                explosion_animation(mine_x, mine_y)
                life -= 20
            collision5 = is_collision(mine_2x+25, mine_2y+25, x=cat_x, y=cat_y,d=50) #mine2
            if collision5 == True:
                explosion_animation(mine_2x, mine_2y)
                ready_fishbone()
                mine_2x = random.randint(40, 410)
                mine_2y = random.randint(0, 100)
                explosion_animation(mine_2x, mine_2y)
                life -= 20
            collision6 = is_collision(life_x, life_y, x=cat_x, y=cat_y,d=50) #powerup
            if collision6 == True:
                life_x = random.randint(40, 410)
                life_y = random.randint(-4000, -1000)
                life += 10

        y1 += track_speed
        y2 += track_speed

        # making the fishbone to move seperately.
        if y1 >= 675:
            y1 = -675
        if y2 >= 675:
            y2 = -675
        fishbone_y += fishbone_yc
        if fishbone_y < 0:
            ready_fishbone()

        if cat_x <= 40:
            cat_x = 40
        if cat_x >= 410:
            cat_x = 410
        cat_x += cat_xc

        show_fishbone()
        if fishbone_y == cat_y:
            fishbone_x = cat_x + 20

        # ##### respawning enemy1 #######
        if enemy_1y >= 675:
            enemy_1x = random.randint(40, 410)
            enemy_1y = 0
            life-=10

        enemy_1y += enemy_1yc

        # ##### respawning enemy2 ########
        if enemy_2y >= 675:
            enemy_2x = random.randint(40, 410)
            enemy_2y = -2000
            life-=10

        enemy_2y += enemy_2yc

        # ##### respawning the boss ######
        if boss_y >= 675:
            boss_x = random.randint(120, 300)
            boss_y = -3000
            boss_life = 30
            life-=30

        # moving the boss on x axis
        if boss_x >= 300:
            boss_x = 300
            boss_xc = -4

        if boss_x <= 120:
            boss_x = 120
            boss_xc = 4
        # life #####

        if life_y >= 675:
            life_x = random.randint(120, 300)
            life_y = -4000
            # moving the boss on x axis
        if life_x >= 300:
            life_x = 300
            life_xc = -8

        if life_x <= 120:
            life_x = 120
            life_xc = 8
            
        # when boss is in nobody is allowed.
        if boss_y >= -300 and boss_y <= 675:

            enemy_1yc = 0
            enemy_2yc = 0
            enemy_1y = -100
            enemy_2y = -1000
        elif boss_y >= 675:
            enemy_1yc = 3
            enemy_2yc = 15

        boss_y += boss_yc
        boss_x += boss_xc

        # ##### respawning the mine #######
        if mine_y >= 675:
            mine_y = random.randint(300, 450)
            mine_x = random.randint(40, 380)

        mine_y += track_speed

        if mine_2y >= 675:
            mine_2y = random.randint(0, 100)
            mine_2x = random.randint(40, 380)

        mine_2y += track_speed

        show_mine()
        show_player_name(player_name, cat_x, cat_y)
        show_cat()
        show_enemy()
        score_display(10, 10)

        if enemy_1y >= 530 and enemy_1y <= 600:
            life -= 1
        if enemy_2y >= 530 and enemy_2y <= 600:
            life -= 1
        if boss_y >= 530 and boss_y <= 600:
            life -= 2

        life_x += life_xc
        life_y += life_yc

        life_display(10, 50)
        if life <= 0:
            print('score')
            print(score)
            print('player name')
            print(player_name)
            save_highscores(score, player_name)
            highscores = load_highscores()
            game_over(60, 250, 10, 10)

        pygame.display.update()

    main()
    
main()
