# Rainbow ball 2022
# By Tomasz Golaszewski
# 12.2022

# Quick project to check metaballs and color palette behavior

import os
import pygame
import random
import math

# global settings
BUFFER_WIDTH, BUFFER_HEIGHT = 100, 70
SCALE = 10
FRAMERATE = 25
WIN_WIDTH, WIN_HEIGHT = BUFFER_WIDTH * SCALE, BUFFER_HEIGHT * SCALE

AMPLIFICATION = 1200 # 550
NUMBER_OF_BALLS = 3 # 6

# ball class
class Ball:
    def __init__(self, x, y, a, v=1):
        self.x = x
        self.y = y
        self.a = a
        self.v_x = v * math.cos(self.a)
        self.v_y = v * math.sin(self.a)

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), 2, 0)

    def move(self):
        self.x += self.v_x
        self.y += self.v_y

        if self.x < 0 or self.x > BUFFER_WIDTH:
            self.v_x = -self.v_x
        if self.y < 0 or self.y > BUFFER_HEIGHT:
            self.v_y = -self.v_y

    def metaball_dist(self, x, y):
        amplification = AMPLIFICATION
        dist_from_ball = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        if dist_from_ball < 1: 
            dist_from_ball = 1

        return amplification / dist_from_ball
        

def get_rand_color():
# return random RGB color
    red = random.randint(0,255)
    green = random.randint(0,255)
    blue = random.randint(0,255)
    return (red, green, blue)

def get_1D_color(x):
# return color from blue for 0 to red for 255
    x = int(x)
    if x < 0: 
        return (0, 0, 0)
    if x > 255: 
        return (255, 255, 255)
    
    red = x
    green = 0
    blue = 255 - x
    return (red, green, blue)

def get_2D_color(x, y):
# return color from blue for 0 to red for 255
    x = int(x)
    if x < 0 or x > 255: 
        return (0, 0, 0)
    y = int(y)
    if y < 0 or y > 255: 
        return (0, 0, 0)
    
    red = x
    green = y
    blue = 255 - x
    return (red, green, blue)

def run():
# main function - runs the game

# make balls
    LIST_WITH_BALLS = []
    for i in range(NUMBER_OF_BALLS):
        LIST_WITH_BALLS.append(Ball(random.randint(0, BUFFER_WIDTH), random.randint(0, BUFFER_HEIGHT), random.randint(0, 100) * math.pi / 50))

# initialize the pygame
    pygame.init()
    pygame.display.set_caption("Glowing Balls")
    ICON_IMGS = pygame.image.load(os.path.join("imgs", "icon.png"))
    pygame.display.set_icon(ICON_IMGS)
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    BUFFER = pygame.Surface((BUFFER_WIDTH, BUFFER_HEIGHT))
    BUFFER.convert()
    CLOCK = pygame.time.Clock()
    CURRENT_FRAME = 0

# main loop
    running = True
    while running:
        CLOCK.tick(FRAMERATE)
        CURRENT_FRAME += 1
        if CURRENT_FRAME == FRAMERATE:
            CURRENT_FRAME = 0

            # print infos about fps and time
            print("FPS: %.2f" % CLOCK.get_fps(), end="\t")
            print("TIME: " + str(pygame.time.get_ticks() // 1000))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

# keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # manual close
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False
                    pygame.quit()
                    quit()


# run the simulation
        for ball in LIST_WITH_BALLS:
            ball.move()  

# draw the screen

        # clear screen
        # WIN.fill(BLACK)

        # for x in range(WIN_WIDTH):
        #     for y in range(WIN_HEIGHT):
        #         BUFFER.set_at((x, y), get_1D_color(x))
        
        # pixel_array = pygame.PixelArray(BUFFER)
        # for x in range(WIN_WIDTH):
        #     pixel_array[x, 0:WIN_HEIGHT] = get_1D_color(x) 
        #     # for y in range(WIN_HEIGHT):
        #     #     pixel_array[x, y] = get_1D_color(x)              
        # pixel_array.close()

        pixel_array = pygame.PixelArray(BUFFER)
        for x in range(BUFFER_WIDTH):
            for y in range(BUFFER_HEIGHT):
                points = 0
                for ball in LIST_WITH_BALLS:
                    points += ball.metaball_dist(x, y)           
                pixel_array[x, y] = get_1D_color(points)
        pixel_array.close()

        # for ball in LIST_WITH_BALLS:
        #     ball.draw(BUFFER)

        SCALED_BUFFER = pygame.transform.scale(BUFFER, (WIN_WIDTH, WIN_HEIGHT))
        WIN.blit(SCALED_BUFFER, (0, 0))


# flip the screen
        pygame.display.update() # allows to update a portion of the screen, instead of the entire area of the screen; passing no arguments, updates the entire display
        # pygame.display.flip() # will update the contents of the entire display
    

if __name__ == "__main__":
    run()

