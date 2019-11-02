###########################
# Orbit
#   v0.2
#   Porter Libby 2019
###########################

import pygame
from pygame.locals import *
import random
import math
import os

# get random colors for satellites (choose colors that are light so they stand out)
def random_color():
    r = random.randint(150,255)
    g = random.randint(150,255)
    b = random.randint(150,255)
    return (r,g,b)

# initialize window
pygame.init()
pygame.display.set_caption('Orbit')
gameIcon = pygame.image.load('orbitIcon.png')
pygame.display.set_icon(gameIcon)

# some important constants
G = 6.67428e-11 # gravity
sun_mass = 20e7 # mass of main body
screen_width = 1920
screen_height = 1080

# list for objects (these will be drawn each frame)
sat_ls = [] 
stars_ls = []

for x in range(random.randint(100,200)):
    x_pos = random.randint(0,screen_width)
    y_pos = random.randint(0,screen_height)
    radius = random.randint(1,3)
    stars_ls.append([x_pos,y_pos,radius])


# DATA STRUCTURES
class Satellite:
    def __init__(self, x, y, v, r):
        self.x_pos = x
        self.y_pos = y
        self.velocity = v
        self.radius = r
        self.point_ls = []
        self.predictions = []
        self.mass = 0.5e7
        self.released = False
        self.dots = []
        self.dot_counter = 0
        self.color = random_color()

    def updatePosition(self):
        new_x = self.x_pos + self.velocity[0] / 2
        new_y = self.y_pos + self.velocity[1] / 2
        self.x_pos = new_x
        self.y_pos = new_y

    def updateVelocity(self,self_x,self_y, velocity, mass):
        # Compute the distance of the other body.
        sx, sy = self_x, self_y
        ox, oy = screen_width / 2, screen_height / 2
        dx = (ox-sx)
        dy = (oy-sy)
        d = math.sqrt(dx**2 + dy**2)
        if d == 0:
            raise ValueError("Collision")

        # Compute the force of attraction
        f = G * mass * sun_mass / (d**2)

        # Compute the direction of the force.
        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f
        velocity = ((velocity[0] + fx, velocity[1] + fy))
        return velocity

    def setVelocity(self, x_influence, y_influence):
        self.velocity = (x_influence/10, y_influence/10)
    
    def createDot(self):
        newdot = [int(self.x_pos), int(self.y_pos)]
        self.dots.append(newdot)
        if len(self.dots) > 100:
            self.dots.pop(0)

# VARS
running = True # when false game ends
sun_radius = 20 
count = 0 # counts how frequently to update satellites
dot_count = 0 # counts how frequently to update dots for tracers
draw_line = False # if the aiming line is being rendered
line_start = None # if the aiming line is on, where it starts from (position of sat)

# create game screen
screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)

# LOGIC LOOP
while running:

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # end loop
            running = False

        elif event.type == VIDEORESIZE: # update screen size, change gravity
            x,y = event.size
            if x>0 and y> 0:
                screen_width, screen_height = x,y

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            line_start = (x,y)
            draw_line = True
            sat_ls.append(Satellite(x,y,(0,0), 5))

        elif event.type == pygame.MOUSEBUTTONUP:
            x,y = event.pos
            sat_ls[-1].setVelocity(line_start[0] - x,line_start[1] - y)
            sat_ls[-1].released = True
            draw_line = False


    # DRAWING

    # draw background
    screen.fill((0,0,0))

    # draw mouse indicator line
    if draw_line == True:
        pygame.draw.line(screen, (255,0,0), line_start, pygame.mouse.get_pos(), 2)
        sat = sat_ls[-1]
        pre_x = sat.x_pos
        pre_y = sat.y_pos
        vel = ((sat.velocity[0] + (sat.x_pos - pygame.mouse.get_pos()[0]) / 10), (sat.velocity[1] + (sat.y_pos - pygame.mouse.get_pos()[1]) / 10))

        for x in range(20):
            vel = sat.updateVelocity(pre_x,pre_y,vel,sat.mass)
            new_x = pre_x + vel[0] / 2
            new_y = pre_y + vel[1] / 2
            pre_x = new_x
            pre_y = new_y

            if x % 1 == 0:
                pygame.draw.circle(screen, (255,0,0), (int(pre_x),int(pre_y)), 1)




    # draw stars
    for star in stars_ls:
        pygame.draw.circle(screen, (150,150,150), (star[0],star[1]), star[2])
    
    # draw sats
    if count < 3:
        count = count + 1
    else:
        count = 0

    for sat in sat_ls:
        # draw dots
        if sat.dot_counter == 3:
            sat.createDot()
            sat.dot_counter = 0
        else:
            sat.dot_counter = sat.dot_counter + 1
        if len(sat.dots) > 1:
            pygame.draw.lines(screen, sat.color, False, sat.dots, 1)

        # draw sat
        pygame.draw.circle(screen, sat.color, (int(sat.x_pos),int(sat.y_pos)), sat.radius)

        # update position every nth frame
        if sat.released == True:
            if count == 0:
                sat.updatePosition()
                sat.velocity = sat.updateVelocity(sat.x_pos,sat.y_pos, sat.velocity, sat.mass)

    # draw sun
    pygame.draw.circle(screen, (50,50,50), (screen_width // 2, screen_height // 2), sun_radius+(count % 10))
    pygame.draw.circle(screen, (150,150,150), (screen_width // 2, screen_height // 2), sun_radius+(count % 5))
    pygame.draw.circle(screen, (200,200,200), (screen_width // 2, screen_height // 2), sun_radius+(count % 2))
    pygame.draw.circle(screen, (255,255,255), (screen_width // 2, screen_height // 2), sun_radius)

    #Text through GUI
    if draw_line == True:
        myFont = pygame.font.SysFont("Times New Roman", 18)

        if pygame.mouse.get_pos() != line_start:
            x_len = (line_start[0] - pygame.mouse.get_pos()[0])
            y_len = (line_start[1] - pygame.mouse.get_pos()[1])
            angle_r = math.atan2(y_len,x_len)
            angle_d = math.degrees(angle_r)
            h_length = math.hypot(x_len, y_len)

            angleLabel = myFont.render("Input Angle: " +  str(round(angle_d)), 1, (255,0,0))
            screen.blit(angleLabel, (0, 0))

            velocityLabel = myFont.render("Input Velocity: " +  str(round(h_length)), 1, (255,0,0))
            screen.blit(velocityLabel, (0, 20))

    # Flip the display each frame
    pygame.display.flip()

# when while loop ends, exit game
pygame.quit()





