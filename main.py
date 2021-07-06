import pygame
import random
import math
from pygame import mixer

# intializing pygame

pygame.init()

game_status = "play"

screen = pygame.display.set_mode((1200, 650))
pygame.display.set_caption("Shubham_In_Space")
icon = pygame.image.load('images/galaxy.png')
pygame.display.set_icon(icon)

# Background sound
mixer.music.load('sounds/adventure.wav')
mixer.music.play(-1)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over
game_over = pygame.font.Font('freesansbold.ttf', 65)

# Background Image
background = pygame.image.load('images/back.png')

# Player
playerImg = pygame.image.load('images/spaceship.png')
playerX = 600
playerY = 600
playerX_change = 0
playerY_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/octopus.png'))
    enemyX.append(random.randint(0, 1136))
    enemyY.append(random.randint(0, 230))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"


def show_score(x, y):
    score = font.render("score : " + str(score_value), True, (100, 220, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False


def game_over_text():
    over_text = game_over.render('GAME OVER', True, (255, 46, 10))
    screen.blit(over_text, (400, 300))


running = True
while running:
    screen.fill((15, 10, 20))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            running = False


        # If keystroke is pressed check wheather it is right or left or up an down.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_UP:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN:
                playerY_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('sounds/bullet.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    # Creating boundries for spaceship
    if playerX <= 0:
        playerX = 0
    if playerX >= 1136:
        playerX = 1136
    elif playerY >= 636:
        playerY = 636

    for i in range(num_of_enemies):
        if enemyY[i] > 550:
            for j in range(num_of_enemies):
                enemyY[i] = 2000

            game_over_text()

            game_status = "stop"
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 1136:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        elif enemyY[i] >= 636:
            enemyY[i] = 636
        if game_status == "stop":
            break

        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collide_sound = mixer.Sound('sounds/Splat2.wav')
            collide_sound.play()
            bulletY = 600
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 1136)
            enemyY[i] = random.randint(0, 230)

        enemy(enemyX[i], enemyY[i], i)
    # Bullet movement
    if bulletY <= 0:
        bulletY = 0
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
