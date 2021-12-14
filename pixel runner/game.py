import random
from random import choice
from sys import exit

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_1 = pygame.image.load("player_walk_1.png").convert_alpha()
        player_2 = pygame.image.load("player_walk_2.png").convert_alpha()
        self.player_walk = [player_1, player_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("jump.png").convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(bottomleft=(80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('jump.mp3')
        self.jump_sound.set_volume(0.2)
        # self.music = pygame.mixer.Sound('audio/music.wav')

    def Player_Input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def Gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300
        # self.music.play()

    def animation_player(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.Player_Input()
        self.Gravity()
        self.animation_player()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'snail':
            snail1 = pygame.image.load('snail1.png').convert_alpha()
            snail2 = pygame.image.load('snail2.png').convert_alpha()
            self.frame = [snail1, snail2]
            Y_pos = 300
        else:
            bird1 = pygame.image.load('Fly1.png').convert_alpha()
            bird2 = pygame.image.load('Fly2.png').convert_alpha()
            self.frame = [bird1, bird2]
            Y_pos = 200
        self.animation_index = 0
        self.image = self.frame[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), Y_pos))

    def animation_obstacle(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frame):
            self.animation_index = 0
        self.image = self.frame[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_obstacle()
        self.rect.x -= 6
        self.destroy()


# function display score


def display_score():
    current_time = pygame.time.get_ticks() // 1000 - start_time
    score_surf = font.render(f'{current_time}', False, 'blue')
    score_rec = score_surf.get_rect(center=(400, 60))
    screen.blit(score_surf, score_rec)
    return current_time


def timer_movement(timer_list):
    if timer_list:
        for timer_rec in timer_list:
            timer_rec.x -= 5
            if timer_rec.bottom == 300:
                screen.blit(snail_1, timer_rec)
            else:
                screen.blit(bird_1, timer_rec)

        timer_list = [Timer for Timer in timer_list if Timer.x > -100]

        return timer_list
    else:
        return []


def collision(player_run, obstacles):
    if obstacles:
        for obstacle_rec in obstacles:
            if player_run.colliderect(obstacle_rec):
                return False
    return True


def player_animation():
    # play walking animation when player is on floor
    # display the jump surface when player is not on floor
    global player_surf, player_index
    if player_rect.bottom > 300:  # jump
        player_surf = player_jump
    else:  # walk
        player_index += 0.1
        if player_index > len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


def Collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        obstacle.empty()
        return False
    else:
        return True

# Intro window


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
font = pygame.font.Font('font.ttf', 50)
sky_surface = pygame.image.load('Sky.png').convert()
ground_surface = pygame.image.load('ground.png').convert()
title_surface = font.render('Score', False, 'Blue')
title_rec = title_surface.get_rect(center=(400, 30))

background_music = pygame.mixer.Sound('wygz_kyfy_kdh.mp3')
# background_music = pygame.mixer.Sound('music.wav')
background_music.play(loops=-1)
# background_music.set_volume(0.5)

# snail
snail_1 = pygame.image.load('snail1.png').convert_alpha()
snail_2 = pygame.image.load('snail2.png').convert_alpha()
snail = [snail_1, snail_2]
snail_index = 0
snail_sur = snail[snail_index]
# snail_rec = snail_1.get_rect(bottomright=(800, 300))

bird_1 = pygame.image.load('Fly1.png').convert_alpha()
bird_2 = pygame.image.load('Fly2.png').convert_alpha()
bird = [bird_1, bird_2]
bird_index = 0
bird_sur = bird[bird_index]
# bird_rec = bird_1.get_rect(center=(400, 200))

obstacle_rec_list = []

# player
player_walk_1 = pygame.image.load('player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load('jump.png').convert_alpha()
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_walk_1.get_rect(bottomleft=(50, 300))

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

# Groups
obstacle = pygame.sprite.Group()
# obstacle.add(Obstacle(snail, bird))

# player_rec_2 = player_walk_2.get_rect(bottomleft=(50, 300))
# player_rect = [player_rect, player_rec_2]
player_gravity = 0
player_stand = pygame.image.load('player_stand.png').convert_alpha()
player_stand_scale = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rec = player_stand_scale.get_rect(center=(400, 220))

# game
character_name = font.render("wegz", False, '#caf450')
character_name_rec = character_name.get_rect(center=(400, 100))
game_message_start = font.render("press space to start", False, "lightgreen")
game_message_start_rec = game_message_start.get_rect(center=(400, 330))
game_message_start_2 = font.render("press space to start new game", False, "lightgreen")
game_message_start_rec_2 = game_message_start_2.get_rect(center=(400, 330))
game_active = False
start_time = 0
score = 0

player_timer = pygame.USEREVENT + 1
pygame.time.set_timer(player_timer, 1500)
snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)
bird_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bird_timer, 200)

while True:
    # draw all our elements
    # update everything
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # jump
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
            # new game
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rec.left = 800
                # player_rect.right = 0
                start_time = pygame.time.get_ticks() // 1000
        if game_active:
            if event.type == player_timer:
                obstacle.add(Obstacle(choice(['snail', 'bird', 'snail'])))
                # if randint(0, 2):
                #     obstacle_rec_list.append(snail_sur.get_rect(bottomright=(randint(900, 1100), 300)))
                # else:
                #     obstacle_rec_list.append(bird_sur.get_rect(bottomright=(randint(900, 1100), 200)))

            if event.type == snail_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_sur = snail[snail_index]

            if event.type == bird_timer:
                if bird_index == 0:
                    bird_index = 1
                else:
                    bird_index = 0
                bird_sur = bird[bird_index]

    if game_active:

        # image background
        screen.blit(sky_surface, (0, 0))  # (left, top)
        screen.blit(ground_surface, (0, 300))  # (left, top)
        screen.blit(title_surface, title_rec)
        score = display_score()
        # background_music = pygame.mixer.Sound('audio/music.wav')
        # background_music.play(loops=1)
        # background_music.set_volume(0.2)

        # snail
        # if snail_rec.right <= 0:
        #     snail_rec.left = 800
        # screen.blit(snail_1, snail_rec)
        # snail_rec.right -= 4

        # player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom > 300:
        #     player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()
        obstacle.draw(screen)
        obstacle.update()

        # if player_rect.left > 800:
        #     player_rect.right = 0
        # player_rect.left += 2

        # game_active = collision(player_rect, obstacle_rec_list)
        game_active = Collision_sprite()
        # if player_rect.colliderect(snail_rec):
        #     print("game over")
        #     game_active = False

        # obstacle_rec_list = timer_movement(obstacle_rec_list)

        # window start
    else:
        screen.fill('black')
        obstacle_rec_list.clear()
        player_rect.bottomleft = (50, 300)
        player_gravity = 0
        score_message = font.render(f'Your score= {score}', False, 'blue')
        score_message_rec = score_message.get_rect(center=(400, 50))
        if score:
            screen.blit(score_message, score_message_rec)
            screen.blit(game_message_start_2, game_message_start_rec_2)
        else:
            screen.blit(game_message_start, game_message_start_rec)
        screen.blit(player_stand_scale, player_stand_rec)
        screen.blit(character_name, character_name_rec)

    pygame.display.update()
    # level = 10
    # if level <= score:
    #     tick = level + 50
    #     level *= 1.5
    # else:
    #     tick = 60
    # print(tick)
    clock.tick(60)
